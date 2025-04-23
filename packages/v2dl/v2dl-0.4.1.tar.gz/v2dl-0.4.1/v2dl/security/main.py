import os
import sys
import atexit
import base64
import ctypes
import random
import secrets
import threading
from dataclasses import dataclass
from datetime import datetime, timedelta
from logging import Logger
from typing import Any, Literal, overload

import yaml
from dotenv import load_dotenv, set_key
from nacl.public import PrivateKey, PublicKey, SealedBox
from nacl.pwhash import argon2id
from nacl.secret import SecretBox
from nacl.utils import EncryptedMessage, random as nacl_random

from v2dl.common import ConfigManager, EncryptionConfig, SecurityError


@dataclass
class KeyPair:
    private_key: PrivateKey
    public_key: PublicKey


class Encryptor:
    """Managing encryption and decryption operations."""

    def __init__(self, logger: Logger, encrypt_config: EncryptionConfig) -> None:
        self.logger = logger
        self.encrypt_config = encrypt_config

    def encrypt_master_key(self, master_key: bytes) -> tuple[bytes, bytes, bytes]:
        salt = secrets.token_bytes(self.encrypt_config.salt_bytes)
        encryption_key = secrets.token_bytes(self.encrypt_config.key_bytes)
        derived_key = self.derive_key(encryption_key, salt)

        box = SecretBox(derived_key)
        nonce = nacl_random(self.encrypt_config.nonce_bytes)
        encrypted_master_key = box.encrypt(master_key, nonce)

        derived_key = bytearray(len(derived_key))
        self.logger.info("Master key encryption successful")
        return encrypted_master_key, salt, encryption_key

    def decrypt_master_key(
        self,
        encrypted_master_key: bytes,
        salt: str,
        encryption_key: str,
    ) -> bytes:
        salt_b64 = base64.b64decode(salt)
        enc_key_b64 = base64.b64decode(encryption_key)
        derived_key = self.derive_key(enc_key_b64, salt_b64)
        box = SecretBox(derived_key)

        master_key = box.decrypt(encrypted_master_key)

        self.logger.info("Master key decryption successful")
        return master_key

    def encrypt_private_key(self, private_key: PrivateKey, master_key: bytes) -> EncryptedMessage:
        box = SecretBox(master_key)
        nonce = nacl_random(self.encrypt_config.nonce_bytes)
        return box.encrypt(private_key.encode(), nonce)

    def decrypt_private_key(self, encrypted_private_key: bytes, master_key: bytes) -> PrivateKey:
        box = SecretBox(master_key)
        private_key_bytes = box.decrypt(encrypted_private_key)
        private_key = PrivateKey(private_key_bytes)
        cleanup([private_key_bytes])
        return private_key

    def encrypt_password(self, password: str, public_key: PublicKey) -> str:
        sealed_box = SealedBox(public_key)
        encrypted = sealed_box.encrypt(password.encode())
        self.logger.info("Password encryption successful")
        return base64.b64encode(encrypted).decode("utf-8")

    def decrypt_password(self, encrypted_password: str, private_key: PrivateKey) -> str:
        try:
            encrypted = base64.b64decode(encrypted_password)
            sealed_box = SealedBox(private_key)
            decrypted = sealed_box.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            self.logger.error("Password decryption failed: %s", str(e))
            raise SecurityError from e

    def derive_key(self, encryption_key: bytes, salt: bytes) -> bytes:
        return argon2id.kdf(
            self.encrypt_config.key_bytes,
            encryption_key,
            salt,
            opslimit=self.encrypt_config.kdf_ops_limit,
            memlimit=self.encrypt_config.kdf_mem_limit,
        )

    def validate_keypair(self, private_key: PrivateKey, public_key: PublicKey) -> None:
        try:
            test_data = b"test"
            sealed_box = SealedBox(public_key)
            sealed_box_priv = SealedBox(private_key)

            encrypted = sealed_box.encrypt(test_data)
            decrypted = sealed_box_priv.decrypt(encrypted)

            if decrypted != test_data:
                raise SecurityError
        except Exception as e:
            self.logger.error("Key pair validation failed: %s", str(e))
            raise SecurityError from e


class KeyIOHelper(Encryptor):
    """Manage the loading, saving, and validation of cryptographic keys."""

    def __init__(
        self,
        logger: Logger,
        static_config: dict[str, str] | None,
        encrypt_config: EncryptionConfig,
    ) -> None:
        super().__init__(logger, encrypt_config)
        self.logger = logger
        self.static_config = self.init_conf(static_config)

    def init_conf(self, static_config: dict[str, str] | None) -> dict[str, str]:
        if static_config is None:
            base_dir = ConfigManager.get_system_config_dir()
            self.logger.debug("Initializing config with base directory: %s", base_dir)
            return {
                "key_folder": os.path.join(base_dir, ".keys"),
                "env_path": os.path.join(base_dir, ".env"),
                "master_key_file": os.path.join(base_dir, ".keys", "master_key.enc"),
                "private_key_file": os.path.join(base_dir, ".keys", "private_key.pem"),
                "public_key_file": os.path.join(base_dir, ".keys", "public_key.pem"),
            }
        else:
            return static_config

    def load_keys(self) -> KeyPair:
        self.logger.debug("Loading and validating keys")
        master_key = self.load_master_key()
        private_key = self.load_private_key(master_key)
        public_key = self.load_public_key()

        self.validate_keypair(private_key, public_key)
        cleanup([master_key])

        self.logger.info("Keys loaded and validated successfully")
        return KeyPair(private_key, public_key)

    def load_secret(self, env_path: str) -> tuple[str, str]:
        """Load and validate salt and encryption_key from .env file."""
        load_dotenv(env_path)
        salt_base64 = SecureFileHandler.read_env("SALT")
        encryption_key_base64 = SecureFileHandler.read_env("ENCRYPTION_KEY")
        return salt_base64, encryption_key_base64

    def load_master_key(self, path: str | None = None) -> bytes:
        _path = self.static_config["master_key_file"] if path is None else path
        encrypted_master_key = SecureFileHandler.read_file(_path, False)
        salt, encryption_key = self.load_secret(self.static_config["env_path"])
        return self.decrypt_master_key(encrypted_master_key, salt, encryption_key)

    def load_public_key(self, path: str | None = None) -> PublicKey:
        _path = self.static_config["public_key_file"] if path is None else path
        public_key_bytes = SecureFileHandler.read_file(_path, False)
        return PublicKey(public_key_bytes)

    def load_private_key(self, master_key: bytes, path: str | None = None) -> PrivateKey:
        _path = self.static_config["private_key_file"] if path is None else path
        encrypted_private_key = SecureFileHandler.read_file(_path, False)
        return self.decrypt_private_key(encrypted_private_key, master_key)

    def save_keys(self, keys: tuple[bytes, bytes, PublicKey, bytes, bytes]) -> None:
        SecureFileHandler.write_file(self.static_config["master_key_file"], keys[0])
        SecureFileHandler.write_file(self.static_config["private_key_file"], keys[1])
        SecureFileHandler.write_file(self.static_config["public_key_file"], keys[2].encode(), 0o644)
        SecureFileHandler.write_env(self.static_config["env_path"], "SALT", keys[3])
        SecureFileHandler.write_env(self.static_config["env_path"], "ENCRYPTION_KEY", keys[4])

    def check_folder(self) -> None:
        folder_path = self.static_config["key_folder"]
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, mode=0o700)
            self.logger.info("Secure folder created at %s", folder_path)
        else:
            current_permissions = os.stat(folder_path).st_mode & 0o777
            if current_permissions != 0o700:
                os.chmod(folder_path, 0o700)
                self.logger.info("Permissions updated for folder at %s", folder_path)

    def check_permission(self, folder_path: str) -> bool:
        folder_permission = 0o700
        current_permissions = os.stat(folder_path).st_mode & 0o777
        return current_permissions == folder_permission


class KeyManager(KeyIOHelper):
    """Top level class managing key generation."""

    def __init__(
        self,
        logger: Logger,
        encrypt_config: EncryptionConfig,
        path_dict: dict[str, str] | None = None,
    ) -> None:
        super().__init__(logger, path_dict, encrypt_config)
        self.check_folder()

        keys = self._init_keys()
        if keys is not None:
            self.save_keys(keys)

    def _init_keys(self) -> tuple[bytes, bytes, PublicKey, bytes, bytes] | None:
        if self._keys_exist():
            self.logger.info("Key pair already exists")
            return None

        return self._generate_and_encrypt_keys()

    def _keys_exist(self) -> bool:
        return os.path.exists(self.static_config["private_key_file"]) and os.path.exists(
            self.static_config["public_key_file"],
        )

    def _generate_and_encrypt_keys(self) -> tuple[bytes, bytes, PublicKey, bytes, bytes]:
        keys = self._generate_key_pair()
        master_key = secrets.token_bytes(self.encrypt_config.key_bytes)
        encrypted_master_key, salt, encryption_key = self.encrypt_master_key(master_key)
        encrypted_private_key = self.encrypt_private_key(keys.private_key, master_key)

        cleanup([master_key])
        self.logger.info("Key pair has been successfully generated")
        return (
            encrypted_master_key,
            encrypted_private_key,
            keys.public_key,
            salt,
            encryption_key,
        )

    def _generate_key_pair(self) -> KeyPair:
        private_key = PrivateKey.generate()
        return KeyPair(private_key, private_key.public_key)


class AccountManager:
    MAX_QUOTA = 16
    DEFAULT_RUNTIME_STATUS = {
        "cookies_valid": True,
        "password_valid": True,
        "exceed_quota": False,
    }

    def __init__(self, logger: Logger, key_manager: KeyManager, yaml_path: str = ""):
        self.logger = logger
        self.yaml_path = (
            yaml_path
            if yaml_path
            else os.path.join(ConfigManager.get_system_config_dir(), "accounts.yaml")
        )
        self.key_manager = key_manager
        self.lock = threading.RLock()
        self.accounts, self.runtime_state = self._load_yaml()
        self.check()
        atexit.register(self._save_yaml)

    def create(self, username: str, password: str, cookies: str, public_key: PublicKey) -> None:
        """Create persistent account in yaml file"""
        with self.lock:
            encrypted_password = self.key_manager.encrypt_password(password, public_key)
            self.accounts[username] = {
                "encrypted_password": encrypted_password,
                "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "exceed_quota": False,
                "exceed_time": "",
                "cookies": cookies,
            }
        self.logger.info("Account %s has been created.", username)
        self._save_yaml()

    def delete(self, username: str) -> None:
        """Delete persistent account in yaml file"""
        with self.lock:
            if username in self.accounts:
                del self.accounts[username]
                self.logger.info("Account %s has been deleted.", username)
            else:
                self.logger.error("Account %s not found.", username)
            self._save_yaml()

    def read(self, username: str) -> dict[str, Any] | None:
        """Read persistent account in yaml file"""
        return self.accounts.get(username)

    def edit(
        self,
        public_key: PublicKey,
        old_username: str,
        new_username: str | None,
        new_password: str | None,
        new_cookies: str | None,
    ) -> None:
        """Edit persistent account name/password in yaml file"""
        with self.lock:
            if old_username in self.accounts:
                if new_username:
                    self.accounts[new_username] = self.accounts.pop(old_username)
                if new_password:
                    encrypted_password = self.key_manager.encrypt_password(new_password, public_key)
                    self.accounts[new_username or old_username]["encrypted_password"] = (
                        encrypted_password
                    )
                if new_cookies:
                    self.accounts[new_username or old_username]["cookies"] = new_cookies
                self.logger.info("Account %s has been updated.", old_username)
            else:
                self.logger.error("Account not found.")

    def update_account(self, account: str, field: str, value: Any) -> None:
        """Update persistent account status in yaml file

        Args:
            account (str): The account to update
            field (str): The field to update
            value (Any): The new value of the field
        """
        with self.lock:
            account_info = self.accounts.get(account)
            if account_info:
                if field in account_info:
                    account_info[field] = value
                    self.logger.debug("Updated yaml %s for account %s.", field, account)
                    self._save_yaml()
                else:
                    self.logger.error(
                        "Field '%s' does not exist in account '%s'.", field, account_info
                    )
            else:
                self.logger.error("Account %s not found.", account)

    def verify_password(self, account: str, password: str, private_key: PrivateKey) -> bool:
        account_info = self.accounts.get(account)
        if not account_info:
            self.logger.error("Account does not exist.")
            return False

        encrypted_password = account_info.get("encrypted_password")
        decrypted_password = self.key_manager.decrypt_password(encrypted_password, private_key)
        if decrypted_password == password:
            print("*----------------*")
            print("|Password correct|")
            print("*----------------*")
            return True
        else:
            print("*------------------*")
            print("|Incorrect password|")
            print("*------------------*")
            return False

    def check(self) -> None:
        """檢查所有帳號的 exceed_time 是否超過 12 小時，若超過則清除 exceed_time 並將重置 exceed_quota.

        Note: yaml 存檔中的 exceed_time/exceed_quota 即將被廢棄，因為 v2ph 並不明確指出冷卻時間，以及用戶
        可能需要重複下載卻會被 exceed_quota 阻擋，現在他只會紀錄而不會被真正用於判斷，判斷改成每次運行時紀錄帳號
        額度避免重複挑選。
        """
        now = datetime.now()
        update = False

        for _, account in self.accounts.items():
            if exceed_time := account["exceed_time"]:  # 如果不是空字串就進入檢查
                exceed_time_ = datetime.strptime(exceed_time, "%Y-%m-%dT%H:%M:%S")
                if now - exceed_time_ > timedelta(hours=12):
                    account["exceed_time"] = ""
                    account["exceed_quota"] = False
                    update = True

        if update:
            self._save_yaml()

    def update_runtime_state(self, account: str, field: str, value: Any) -> None:
        """Update the runtime status for each account"""
        account_info = self.runtime_state.get(account)
        if account_info:
            if field in account_info:
                account_info[field] = value
                self.logger.debug("Updated runtime status %s for account %s.", field, account)
            else:
                self.logger.error("Field '%s' does not exist in the account.", field)
        else:
            self.logger.error("Account %s not found.", account)

    def add_runtime_account(self, account: str, password: str, cookies: str) -> None:
        self.accounts.update({account: {"password": password, "cookies": cookies}})
        self.runtime_state.update({account: self.DEFAULT_RUNTIME_STATUS})

    def random_pick(self) -> str:
        accounts = {k: v for k, v in self.accounts.items() if self.is_valid_account(k)}
        if not accounts:
            self.logger.info("No eligible accounts available for login. Existing.")
            sys.exit(0)

        account, _ = random.choice(list(accounts.items()))
        return account

    def get_pw(self, account: str, private_key: PrivateKey) -> str:
        account_info = self.accounts[account]
        enc_pw = account_info["encrypted_password"]
        return self.key_manager.decrypt_password(enc_pw, private_key)

    def is_valid_account(self, account: str) -> bool:
        """filter invalid account during runtime based on cookies, password and quota"""
        state = self.runtime_state[account]
        return (state["cookies_valid"] or state["password_valid"]) and not state["exceed_quota"]

    def _save_yaml(self) -> None:
        with self.lock:
            with open(self.yaml_path, "w") as file:
                yaml.dump(self.accounts, file, default_flow_style=False)
        # self.logger.info("Successfully update accounts information.")

    def _load_yaml(self) -> tuple[dict[str, Any], dict[str, Any]]:
        try:
            with open(self.yaml_path) as file:
                account = yaml.safe_load(file) or {}
            runtime_state = self._login_state(account)
            return account, runtime_state
        except FileNotFoundError:
            return {}, {}

    def _login_state(self, accounts: dict[str, Any]) -> dict[str, Any]:
        """Store login status. Use an individual variable for not storing back to file"""
        return {account: self.DEFAULT_RUNTIME_STATUS for account in accounts}


class SecureFileHandler:
    @staticmethod
    def write_file(path: str, data: str | bytes, permissions: int = 0o400) -> None:
        if isinstance(data, str):
            data = data.encode("utf-8")

        with open(path, "wb") as f:
            f.write(data)
        os.chmod(path, permissions)

    @staticmethod
    @overload
    def read_file(path: str, decode: Literal[True]) -> str: ...

    @staticmethod
    @overload
    def read_file(path: str, decode: Literal[False]) -> bytes: ...

    @staticmethod
    def read_file(path: str, decode: bool = False) -> str | bytes:
        with open(path, "rb") as f:
            _data = f.read()

        return _data.decode("utf-8") if decode else _data

    @staticmethod
    def write_env(env_path: str, key: str, value: str | bytes) -> None:
        if isinstance(value, bytes):
            value = base64.b64encode(value).decode("utf-8")

        load_dotenv(env_path)
        set_key(env_path, key, value)

    @staticmethod
    def read_env(key: str) -> str:
        value = os.getenv(key)
        if value is None:
            raise SecurityError(
                f"Missing required environment variable: {key}, please check your key files"
            )
        return value


def cleanup(sensitive_data: list[bytes]) -> None:
    for data in sensitive_data:
        length = len(data)
        buffer = ctypes.create_string_buffer(length)
        ctypes.memmove(ctypes.addressof(buffer), data, length)
        ctypes.memset(ctypes.addressof(buffer), 0, length)
        del buffer

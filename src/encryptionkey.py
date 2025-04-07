
import os.path
from cryptography.fernet import Fernet


class InfoEncrypter:
    def __init__(self, key_file):
        self.key_file = key_file
        self.encryption_key = None
        self.fernet = None

        self._set_fernet()

    def _set_fernet(self):
        if self._check_existing_key():
            self.encryption_key = self._read_key()
            self.fernet = Fernet(self.encryption_key)
        else:
            self.encryption_key = self._generate_new_key()
            self.fernet = Fernet(self.encryption_key)

    def _check_existing_key(self):
        return os.path.exists(self.key_file)

    def _generate_new_key(self):
        self.encryption_key = Fernet.generate_key()
        with open(self.key_file, 'wb') as user_file:
            user_file.write(self.encryption_key)
        return self.encryption_key

    def _read_key(self):
        with open(self.key_file, 'rb') as user_file:
            self.encryption_key = user_file.readline()
            return self.encryption_key

    def encrypt_info(self, new_account_datum: str) -> str:
        return self.fernet.encrypt(new_account_datum.encode())

    def decrypt_info(self, delete_account_datum: str) -> str:
        return self.fernet.decrypt(delete_account_datum).decode()

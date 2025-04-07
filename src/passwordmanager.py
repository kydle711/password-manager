import os.path
from passlib.hash import pbkdf2_sha256

from passwordfilehandler import PasswordFileHandler
from utils import _is_int

REL_PATH = os.path.join('..', 'data')


class PasswordManager:
    def __init__(self):
        self.pfh = PasswordFileHandler
        self.active_account = None
        self.account_database = None
        self.key_file = None
        self.window = None

    def set_window(self, window):
        self.window = window

    """ Create account methods """

    @staticmethod
    def _check_unique_local_account(new_account_name: str) -> bool:
        return not os.path.exists(os.path.join(REL_PATH, new_account_name + '.acct'))

    """ NOT CURRENTLY IN USE """
    @staticmethod
    def _check_username_length(new_username: str) -> bool:
        return len(new_username) > 6

    @staticmethod
    def _verify_password_length(new_password: str) -> bool:
        return len(new_password) > 6

    @staticmethod
    def _verify_matching_passwords(pass1: str, pass2: str) -> bool:
        return pass1 == pass2

    def create_new_local_account(self, new_username, pass1, pass2):
        if not PasswordManager._verify_password_length(pass1):
            self.window.current_frame.password_too_short_error()
            return

        if not PasswordManager._verify_matching_passwords(pass1, pass2):
            self.window.current_frame.passwords_not_matching_error()
            return

        if not PasswordManager._check_unique_local_account(new_username):
            self.window.current_frame.account_exists_error()
            return

        hashed_password = pbkdf2_sha256.hash(pass1)
        new_account_file = os.path.join(REL_PATH, new_username + ".acct")
        with open(new_account_file, 'w') as af:
            af.write(hashed_password)
        self.window.current_frame.account_created_message()

    """ Login methods """

    def login(self, username, password):
        if not self._validate_account_name(username):
            self.window.current_frame.account_does_not_exist_error()
            return
        if not self._validate_login_info(username, password):
            self.window.current_frame.invalid_login_error()
            return
        self._set_active_account(username)
        self.window.set_user_account_frame(username)

    @staticmethod
    def _validate_account_name(username:str) -> bool:
        return os.path.exists(os.path.join(REL_PATH, username + ".acct"))

    @staticmethod
    def _validate_login_info(username: str, password: str) -> bool:
        account_file = os.path.join(REL_PATH, username + ".acct")
        with open(account_file, 'r') as password_file:
            stored_password = password_file.readline()
            return pbkdf2_sha256.verify(password, stored_password)

    def _set_active_account(self, username):
        self.active_account = username
        self.account_database = os.path.join(REL_PATH, username + ".db")
        self.key_file = os.path.join(REL_PATH, username + ".key")

    """ user account methods """

    def logout(self):
        self._reset()
        self.window.set_login_frame()

    def _reset(self):
        self.active_account = None
        self.account_database = None
        self.key_file = None

    def read_account_data(self) -> list[list]:
        with self.pfh(self.account_database, self.key_file) as file_handler:
            account_info = file_handler.read_accounts()
            return account_info

    def _check_unique_account_name(self, account_info: list) -> bool:
        with self.pfh(self.account_database, self.key_file) as file_handler:
            for account in file_handler.read_accounts():
                if account_info[0] in account:
                    self.window.current_frame.duplicate_account_error()
                    return False
        return True

    def _check_complete_fields(self, account_info: list) -> bool:
        if "" not in account_info:
            return True
        self.window.current_frame.invalid_account_info_error()
        return False

    def add_account_info(self, account_info: list) -> bool:
        if not self._check_complete_fields(account_info):
            return False

        if not self._check_unique_account_name(account_info):
            return False

        with self.pfh(self.account_database, self.key_file) as file_handler:
            file_handler.add_account_info(account_info)
        self.window.current_frame.account_info_saved_message()
        return True

    def delete_account_info(self, index: str):
        if not self._confirm_index_is_num(index):
            return
        index = int(index)
        account_to_delete = self._read_delete_index(index)
        if self._confirm_deletion(account_to_delete):
            with self.pfh(self.account_database, self.key_file) as file_handler:
                file_handler.delete_account_info(index)
            self.window.current_frame.account_info_deleted_message()
            self.window.current_frame.clear_fields()
        else:
            self.window.current_frame.deletion_canceled_message()

    def _confirm_index_is_num(self, index_string: str) -> bool:
        if not _is_int(index_string):
            self.window.current_frame.invalid_deletion_error()
            return False
        return True

    def _read_delete_index(self, index: int) -> list:
        with self.pfh(self.account_database, self.key_file) as file_handler:
            account_to_delete = file_handler.find_account_from_index(index)
            return account_to_delete

    def _confirm_deletion(self, account_info) -> bool:
        account, username, password = account_info
        return self.window.current_frame.account_info_delete_confirmation(account, username, password)
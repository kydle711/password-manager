
import sqlite3
from encryptionkey import InfoEncrypter


class PasswordFileHandler:
    """ This context manager class handles all the functions of the unique user
    files for the UserAccountFrame
    """
    HEADERS = ['account', 'username', 'password']

    def __init__(self, account_database, key_file):
        self.account_database = account_database
        self.key_file = key_file
        self.con = None  # SQLite connection
        self.cursor = None  # SQLite cursor
        self.encryption_key = InfoEncrypter(self.key_file)

    def __enter__(self):
        self.con = sqlite3.connect(self.account_database)
        self.cursor = self.con.cursor()
        title = self.cursor.execute("SELECT name FROM sqlite_master;")
        if title.fetchone() is None:  # If table doesn't exist, make one
            self.cursor.execute(f"CREATE TABLE accounts({self._format_headers(self.HEADERS)});")
        return self

    @staticmethod
    def _format_headers(headers_list) -> str:
        headers_string = ""
        for header in headers_list:
            headers_string += header
        return headers_string

    def read_accounts(self) -> list[list]:
        self.cursor.execute("SELECT ROWID, * FROM accounts;")
        account_data = self.cursor.fetchall()
        decrypted_account_list = []
        for account in account_data:
            new_list = [account[0]]
            for item in account[1:]:
                new_list.append(self.encryption_key.decrypt_info(item))
            decrypted_account_list.append(new_list)

        return decrypted_account_list

    def add_account_info(self, account_info: list):
        encrypted_info = [self.encryption_key.encrypt_info(item) for item in account_info]
        self.cursor.execute("INSERT INTO accounts values(?, ?, ?);", encrypted_info)
        self.con.commit()

    def delete_account_info(self, index_to_delete: int):
        self.cursor.execute(f"DELETE FROM accounts WHERE ROWID = {index_to_delete};")
        self.con.commit()
        self.cursor.execute("VACUUM accounts;")
        self.con.commit()

    def find_account_from_index(self, index: int) -> list:
        self.cursor.execute(f"SELECT * FROM accounts WHERE ROWID = {index};")
        account_info = self.cursor.fetchone()
        decrypted_account = [self.encryption_key.decrypt_info(item) for item in account_info]
        return decrypted_account

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is not None:
            print(f"Exception type: {exc_type}\n Exception value: {exc_value}\n "
                  f"Exception traceback: {exc_tb}")
        self.con.close()

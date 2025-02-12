import os.path
import sqlite3
from cryptography.fernet import Fernet


class PasswordFileHandler:
    """ This class handles all the functions of the unique user file for the
    UserAccountFrame
    """

    def __init__(self, user):
        self.account_file = user + ".db"
        self.key_file = user + ".key"
        self.con = None  # SQLite connection
        self.cursor = None  # SQLite cursor
        self.key = None  # Fernet key

        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as kf:
                self.key = kf.readline()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as kf:
                kf.write(self.key)

        self.fernet = Fernet(self.key)

    def __enter__(self):
        self.con = sqlite3.connect(self.account_file)
        self.cursor = self.con.cursor()
        title = self.cursor.execute("SELECT name FROM sqlite_master;")
        if title.fetchone() is None:  # If table doesn't exist, make one
            self.cursor.execute("CREATE TABLE accounts(account, username, password);")
        return self

    def read_accounts(self):
        account_data = self.cursor.execute("SELECT ROWID, * FROM accounts;")
        encrypted_account_list = []
        decrypted_account_list = []
        for account in account_data:
            encrypted_account_list.append(account)

        for account in encrypted_account_list:
            new_list = [account[0]]
            for item in account[1:]:
                new_list.append(self.fernet.decrypt(item).decode())
            decrypted_account_list.append(new_list)

        return decrypted_account_list


    def add_password_info(self, new_account: str, new_username: str, new_password: str):
        account = self.fernet.encrypt(new_account.encode())
        username = self.fernet.encrypt(new_username.encode())
        password = self.fernet.encrypt(new_password.encode())
        self.cursor.execute("INSERT INTO accounts values(?, ?, ?);", (account, username, password))
        self.con.commit()

    def delete_password_info(self, index_to_delete):
        self.cursor.execute(f"DELETE FROM accounts WHERE ROWID = {index_to_delete};")
        self.con.commit()
        self.cursor.execute("VACUUM accounts;")
        self.con.commit()

    def find_account_from_index(self, index):
        return self.cursor.execute(f"SELECT * FROM accounts WHERE ROWID = {index};")

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is not None:
            print(f"Exception type: {exc_type}\n Exception value: {exc_value}\n "
                  f"Exception traceback: {exc_tb}")
        self.con.close()

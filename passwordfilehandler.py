import sqlite3


class PasswordFileHandler:
    """ This class handles all the functions of the unique user file for the
    UserAccountFrame
    """

    def __init__(self, user):
        self.account_file = user + ".db"
        self.con = None                # SQLite connection
        self.cursor = None             # SQLite cursor

    def __enter__(self):
        self.con = sqlite3.connect(self.account_file)
        self.cursor = self.con.cursor()
        title = self.cursor.execute("SELECT name FROM sqlite_master;")
        if title.fetchone() is None:          # If table doesn't exist, make one
            self.cursor.execute("CREATE TABLE accounts(account, username, password);")
        return self

    def read_accounts(self):
        """ This function takes the contents of the user's account file and writes
        it to the scrolling label on the UserAccountFrame.
        """
        acct_info = self.cursor.execute("SELECT ROWID, * FROM accounts;")
        return acct_info

    def add_password_info(self, new_account: str, new_username: str, new_password: str):
        account = new_account
        username = new_username
        password = new_password
        self.cursor.execute("INSERT INTO accounts values(?, ?, ?);", (account, username, password))
        self.con.commit()

    def delete_password_info(self):
        """ This function only deletes based off of an account name. This is to
        prevent a user from deleting multiple accounts that may have the same password.
        """
        pass

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is not None:
            print(f"Exception type: {exc_type}\n Exception value: {exc_value}\n Exception traceback: {exc_tb}")
        self.con.close()


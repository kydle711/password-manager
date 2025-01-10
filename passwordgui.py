import os.path
import customtkinter as ctk
from passwordmanagerframe import PasswordManagerFrame
from passwordfilehandler import PasswordFileHandler
from passlib.hash import pbkdf2_sha256
from background import BackgroundFrame


class UserAccountFrame(PasswordManagerFrame):
    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.INTERFACE_WIDTH = 170
        self.INTERFACE_HEIGHT = 30
        self.FONT_SIZE = 16

        self.COLUMN_WIDTH = 160
        self.INDEX_COL_X = 0.38
        self.ACCOUNT_NAME_COL_X = 0.55
        self.USERNAME_COL_X = 0.7
        self.PASSWORD_COL_X = 0.85
        self.INTERFACE_COL_X = 0.14
        self.COLUMN_LABEL_Y = 0.12
        self.COLUMN_BOX_Y = 0.58

        self.title_label = ctk.CTkLabel(
            master=self, width=400, height=40, font=("Arial", 24))

        self.index_label = ctk.CTkLabel(master=self, width=self.COLUMN_WIDTH, height=100, font=('normal', self.FONT_SIZE), text='Index')
        self.account_name_label = ctk.CTkLabel(master=self, width=self.COLUMN_WIDTH, height=100, font=('normal', self.FONT_SIZE), text='Account Name')
        self.username_label = ctk.CTkLabel(master=self, width=self.COLUMN_WIDTH, height=100, font=('normal', self.FONT_SIZE), text='Username')
        self.password_label = ctk.CTkLabel(master=self, width=self.COLUMN_WIDTH, height=100, font=('normal', self.FONT_SIZE), text='Password')

        self.index_box = ctk.CTkTextbox(master=self, width=self.COLUMN_WIDTH, height=450, font=('normal', self.FONT_SIZE))
        self.account_name_box = ctk.CTkTextbox(master=self, width=self.COLUMN_WIDTH, height=450, font=('normal', self.FONT_SIZE))
        self.username_box = ctk.CTkTextbox(master=self, width=self.COLUMN_WIDTH, height=450, font=('normal', self.FONT_SIZE))
        self.password_box = ctk.CTkTextbox(master=self, width=self.COLUMN_WIDTH, height=450, font=('normal', self.FONT_SIZE))

        self.new_account_name_entry = ctk.CTkEntry(
            master=self, width=self.INTERFACE_WIDTH, height=self.INTERFACE_HEIGHT, placeholder_text='Account Name',
            font=("Arial", self.FONT_SIZE))

        self.new_username_entry = ctk.CTkEntry(
            master=self, width=self.INTERFACE_WIDTH, height=self.INTERFACE_HEIGHT, placeholder_text='Username or Email',
            font=("Arial", self.FONT_SIZE))

        self.new_password_entry = ctk.CTkEntry(
            master=self, width=self.INTERFACE_WIDTH, height=self.INTERFACE_HEIGHT, placeholder_text='Password',
            font=("Arial", self.FONT_SIZE))

        self.delete_index_entry = ctk.CTkEntry(
            master=self, width=self.INTERFACE_WIDTH, height=self.INTERFACE_HEIGHT, placeholder_text='Index to delete',
            font=("Arial", self.FONT_SIZE))

        self.delete_button = ctk.CTkButton(
            master=self, width=self.INTERFACE_WIDTH, height=self.INTERFACE_HEIGHT, text='DELETE', fg_color='dark red',
            text_color='black', font=("Arial", self.FONT_SIZE), command=self.delete_account_info)

        self.add_button = ctk.CTkButton(
            master=self, width=self.INTERFACE_WIDTH, height=self.INTERFACE_HEIGHT, text='ADD', fg_color='dark green',
            text_color='black', font=("Arial", self.FONT_SIZE), command=self.add_account_info)

        self.title_label.place(relx=0.5, rely=0.08, anchor='center')

        self.index_label.place(relx=self.INDEX_COL_X, rely=self.COLUMN_LABEL_Y)  # place text box header labels
        self.account_name_label.place(relx=self.ACCOUNT_NAME_COL_X, rely=self.COLUMN_LABEL_Y)
        self.username_label.place(relx=self.USERNAME_COL_X, rely=self.COLUMN_LABEL_Y)
        self.password_label.place(relx=self.PASSWORD_COL_X, rely=self.COLUMN_LABEL_Y)

        self.index_box.place(relx=self.INDEX_COL_X, rely=self.COLUMN_BOX_Y, anchor='center')  # place text boxes
        self.account_name_box.place(relx=self.ACCOUNT_NAME_COL_X, rely=self.COLUMN_BOX_Y, anchor='center')
        self.username_box.place(relx=self.USERNAME_COL_X, rely=self.COLUMN_BOX_Y, anchor='center')
        self.password_box.place(relx=self.PASSWORD_COL_X, rely=self.COLUMN_BOX_Y, anchor='center')

        self.new_account_name_entry.place(relx=self.INTERFACE_COL_X, rely=0.24, anchor='center')  # place entries
        self.new_username_entry.place(relx=self.INTERFACE_COL_X, rely=0.32, anchor='center')
        self.new_password_entry.place(relx=self.INTERFACE_COL_X, rely=0.40, anchor='center')
        self.delete_index_entry.place(relx=self.INTERFACE_COL_X, rely=0.75, anchor='center')

        self.add_button.place(relx=self.INTERFACE_COL_X, rely=0.48, anchor='center')  # place buttons
        self.delete_button.place(relx=self.INTERFACE_COL_X, rely=0.83, anchor='center')

    def display(self):
        """ This method displays the UserAccountFrame and creates a unique file
        handler object to manage the functions of a particular user's info.
        """
        super().display()
        self.configure(width=740)
        self.title_label.configure(text="Password Manager")

    def print_account_list(self):
        """ Takes the user's account info read by the file handler
        and displays it to the corresponding CtkTextBox in the User_Account_Frame.
        """
        self.index_box.configure(state='normal')  # configure boxes for editing and delete previous contents
        self.index_box.delete("0.0", "end")
        self.account_name_box.configure(state='normal')
        self.account_name_box.delete("0.0", "end")
        self.username_box.configure(state='normal')
        self.username_box.delete("0.0", "end")
        self.password_box.configure(state='normal')
        self.password_box.delete("0.0", "end")

        with PasswordFileHandler(self.username) as pfh:
            account_info_object = pfh.read_accounts()
            i = 1
            for item in account_info_object:
                self.index_box.insert(f"{i}.0", f"{item[0]}\n")
                self.account_name_box.insert(f"{i}.0", f"{item[1]}\n")
                self.username_box.insert(f"{i}.0", f"{item[2]}\n")
                self.password_box.insert(f"{i}.0", f"{item[3]}\n")
                i += 1

            self.index_box.configure(state='disabled')  # reconfigure boxes so they can't be edited by user
            self.account_name_box.configure(state='disabled')
            self.username_box.configure(state='disabled')
            self.password_box.configure(state='disabled')

    def add_account_info(self):
        """ If 'username' and 'password' entry boxes aren't empty, add them to the
        user's database file.
        """
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        new_account = self.new_account_name_entry.get()
        if new_password != "" and new_username != "" and new_account != "":
            with PasswordFileHandler(self.username) as pfh:
                pfh.add_password_info(new_account, new_username, new_password)
            self.account_info_saved_message()
        else:
            self.invalid_account_info_error_message()
        self.print_account_list()

    def delete_account_info(self):
        """ Checks for a username to delete, then checks if that
        username exists in the user's account list, then gets user confirmation,
        then deletes the info from the account list. It also tells the file handler
        to update the file.
        """
        removed_username = self.new_username_entry.get()
        found_account = False
        for account_line in self.file_handler.account_list:
            if removed_username == account_line[0]:
                found_account = True
                confirmation = self.account_info_delete_confirmation_request()
                if confirmation:
                    self.file_handler.account_list.remove(account_line)
                    self.account_info_deleted_message()
                    break
                else:
                    self.deletion_canceled_message()
        if not found_account:
            self.invalid_deletion_error_message()


class LoginFrame(PasswordManagerFrame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.username_field = ctk.CTkEntry(
            master=self, width=340, height=60, corner_radius=10, font=("Arial", 20),
            placeholder_text='Enter your username')

        self.password_field = ctk.CTkEntry(
            master=self, width=340, height=60, corner_radius=10, font=("Arial", 20),
            placeholder_text='Enter your password')

        self.login_button = ctk.CTkButton(
            master=self, width=200, height=60, corner_radius=10, text='LOG IN',
            text_color='black', fg_color='gray', border_color='dark blue',
            border_width=2, font=("Arial", 25), command=self.log_in)

        self.new_account_button = ctk.CTkButton(
            master=self, width=160, height=40, corner_radius=4, text='Create new account',
            text_color='black', fg_color='gray', border_color='dark blue',
            border_width=1, font=("Arial", 14), command=master.set_new_account_frame)

        self.login_button.place(relx=0.5, rely=0.7, anchor='center')
        self.new_account_button.place(relx=0.83, rely=0.93, anchor='center')
        self.username_field.place(relx=0.5, rely=0.3, anchor='center')
        self.password_field.place(relx=0.5, rely=0.5, anchor='center')

    def log_in(self):
        master = self.master
        username = self.username_field.get()
        password = self.password_field.get()
        account_file = username + '.acct'
        try:
            with open(account_file, 'r') as password_file:
                stored_password = password_file.readline()
            if pbkdf2_sha256.verify(password, stored_password):
                self.logging_in_message()
                master.set_user_account_frame(username)
            else:
                self.invalid_login_error_message()
        except FileNotFoundError:
            self.account_does_not_exist_error_message()


class NewAccountFrame(PasswordManagerFrame):
    def __init__(self, master):
        super().__init__()
        self.title_label = ctk.CTkLabel(
            master=self, width=450, height=80, font=("Arial", 20),
            text='CREATE A NEW ACCOUNT')

        self.username_field = ctk.CTkEntry(
            master=self, width=340, height=60, corner_radius=10,
            font=("Arial", 20), placeholder_text='Enter your username')

        self.password_field_1 = ctk.CTkEntry(
            master=self, width=340, height=60, corner_radius=10, font=("Arial", 20),
            placeholder_text='Enter your password')

        self.password_field_2 = ctk.CTkEntry(
            master=self, width=340, height=60, corner_radius=10, font=("Arial", 20),
            placeholder_text='Verify your password')

        self.create_account_button = ctk.CTkButton(
            master=self, width=220, height=60, corner_radius=10, text='CREATE ACCOUNT',
            text_color='black', fg_color='gray', border_color='dark blue',
            border_width=2, font=("Arial", 25), command=self.save_account_info)

        self.back_button = ctk.CTkButton(
            master=self, width=100, height=40, corner_radius=4, text='back',
            text_color='black', fg_color='gray', border_color='dark blue',
            border_width=1, font=("Arial", 14), command=master.set_login_frame)

        self.title_label.place(relx=0.5, rely=0.1, anchor='center')
        self.create_account_button.place(relx=0.5, rely=0.85, anchor='center')
        self.username_field.place(relx=0.5, rely=0.2, anchor='center')
        self.password_field_1.place(relx=0.5, rely=0.35, anchor='center')
        self.password_field_2.place(relx=0.5, rely=0.50, anchor='center')
        self.back_button.place(relx=0.88, rely=0.92, anchor='center')

    def save_account_info(self):
        username = self.username_field.get()
        pass1 = self.password_field_1.get()
        pass2 = self.password_field_2.get()
        new_filename = username + ".acct"

        if len(username) < 6:
            return self.username_too_short_error()
        elif pass1 != pass2:
            return self.nonmatching_password_error_message()
        elif os.path.exists(new_filename):
            return self.account_exists_error_message()
        try:
            hashed_password = pbkdf2_sha256.hash(pass1)
            with open(new_filename, 'w') as new_password_file:
                new_password_file.write(hashed_password)
            self.account_created_message()
            self.master.set_login_frame()
        except Exception:
            self.generic_error_message(Exception)


class PasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('950x800')
        self.title("Password Manager")
        self.background_frame = BackgroundFrame(self)
        self.current_frame = LoginFrame(self)
        self.current_frame.display()
        #self.resizable(width=False, height=False)

    def set_login_frame(self):
        self.current_frame = LoginFrame(self)
        self.current_frame.display()

    def set_new_account_frame(self):
        self.current_frame = NewAccountFrame(self)
        self.current_frame.display()

    def set_user_account_frame(self, username):
        self.current_frame = UserAccountFrame(self)
        self.current_frame.username = username
        self.current_frame.print_account_list()
        self.current_frame.display()


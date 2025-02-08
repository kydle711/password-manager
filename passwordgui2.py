import os.path
import customtkinter as ctk

from passwordfilehandler import PasswordFileHandler
from passwordmanagerframe import PasswordManagerFrame
from passlib.hash import pbkdf2_sha256

ctk.set_default_color_theme("green")


class UserAccountFrame(PasswordManagerFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.username = username
        self.text_box_list = []

        self.title_label = ctk.CTkLabel(master=self, width=400, height=40,
                                        font=("Arial", 24))

        self.index_label = ctk.CTkLabel(master=self, text='Index')
        self.account_name_label = ctk.CTkLabel(master=self, text='Account')
        self.username_label = ctk.CTkLabel(master=self, text='Username')
        self.password_label = ctk.CTkLabel(master=self, text='Password')

        self.index_box = ctk.CTkTextbox(master=self, height=450)
        self.account_name_box = ctk.CTkTextbox(master=self, height=450)
        self.username_box = ctk.CTkTextbox(master=self)
        self.password_box = ctk.CTkTextbox(master=self)

        self.text_box_list.append(self.index_box)
        self.text_box_list.append(self.account_name_box)
        self.text_box_list.append(self.username_box)
        self.text_box_list.append(self.password_box)

        for box in self.text_box_list:
            box.configure(state='disabled')

        self.new_account_name_entry = ctk.CTkEntry(master=self, placeholder_text='Account Name')
        self.new_username_entry = ctk.CTkEntry(master=self, placeholder_text='Username or Email')
        self.new_password_entry = ctk.CTkEntry(master=self, placeholder_text='Password')
        self.delete_index_entry = ctk.CTkEntry(master=self, placeholder_text='Index to delete')

        self.delete_button = ctk.CTkButton(master=self, text='DELETE', command=self.delete_account_info)
        self.add_button = ctk.CTkButton(master=self, text='ADD', command=self.add_account_info)
        self.logout_button = ctk.CTkButton(master=self, text="LOGOUT", command=self.logout)

        self.title_label.grid(row=0, column=2, sticky='n')

        self.index_label.grid(row=1, column=0, sticky='s')
        self.account_name_label.grid(row=1, column=1, sticky='s')
        self.username_label.grid(row=1, column=2, sticky='s')
        self.password_label.grid(row=1, column=3, sticky='s')

        self.index_box.grid(row=2, column=0, sticky='ns')
        self.account_name_box.grid(row=2, column=1, sticky='ns')
        self.username_box.grid(row=2, column=2, sticky='ns')
        self.password_box.grid(row=2, column=3, sticky='ns')

        """self.new_account_name_entry.place(relx=self.INTERFACE_COL_X, rely=0.28, anchor='center')  # place entries
        self.new_username_entry.place(relx=self.INTERFACE_COL_X, rely=0.36, anchor='center')
        self.new_password_entry.place(relx=self.INTERFACE_COL_X, rely=0.44, anchor='center')
        self.add_button.place(relx=self.INTERFACE_COL_X, rely=0.52, anchor='center')

        self.delete_index_entry.place(relx=self.INTERFACE_COL_X, rely=0.74, anchor='center')
        self.delete_button.place(relx=self.INTERFACE_COL_X, rely=0.82, anchor='center')
        self.logout_button.place(relx=0.9, rely=0.1, anchor='center')"""

    def display(self):
        """ This method displays the UserAccountFrame and creates a unique file
        handler object to manage the functions of a particular user's info.
        """
        super().display()
        self.title_label.configure(text=f"{self.username}'s Accounts")
        self.print_account_list()

    def print_account_list(self):
        """ Takes the user's account info read by the file handler
        and displays it to the corresponding CtkTextBox in the User_Account_Frame.
        """
        for box in self.text_box_list:
            box.delete("0.0", "end")

        with PasswordFileHandler(self.username) as pfh:
            account_info_object = pfh.read_accounts()
            i = 1
            for item in account_info_object:
                self.index_box.insert(f"{i}.0", f"{item[0]}\n")
                self.account_name_box.insert(f"{i}.0", f"{item[1]}\n")
                self.username_box.insert(f"{i}.0", f"{item[2]}\n")
                self.password_box.insert(f"{i}.0", f"{item[3]}\n")
                i += 1

    def add_account_info(self):
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

        def _is_int(int_input):
            try:
                int(int_input)
                return True
            except ValueError:
                return False

        index_input = self.delete_index_entry.get()

        if _is_int(index_input):
            index_to_remove = int(index_input)
            with PasswordFileHandler(self.username) as pfh:
                account_to_delete = pfh.find_account_from_index(index_to_remove)
                print(account_to_delete)

                for item in account_to_delete:
                    account_name = item[0]
                    username = item[1]
                    password = item[2]

            if self.account_info_delete_confirmation(account_name, username, password):
                with PasswordFileHandler(self.username) as pfh:
                    pfh.delete_password_info(index_to_remove)
                self.account_info_deleted_message()
                self.print_account_list()
            else:
                self.deletion_canceled_message()

        else:
            self.invalid_deletion_error_message()

    def logout(self):
        self.master.set_login_frame()


class LoginFrame(PasswordManagerFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(3, weight=1)
        self.username_field = ctk.CTkEntry(
            master=self, width=340, height=60, corner_radius=5, font=("Arial", 20),
            placeholder_text='Enter your username')

        self.password_field = ctk.CTkEntry(
            master=self, width=340, height=60, corner_radius=5, font=("Arial", 20),
            placeholder_text='Enter your password')

        self.login_button = ctk.CTkButton(
            master=self, width=200, height=60, corner_radius=5, text='LOG IN',
            font=("Arial", 25), command=self.log_in)

        self.new_account_button = ctk.CTkButton(
            master=self, width=160, height=40, corner_radius=5, text='Create new account',
            font=("Arial", 14), command=master.set_new_account_frame)

        self.username_field.grid(row=0, column=0, pady=10)
        self.password_field.grid(row=1, column=0, pady=10)
        self.login_button.grid(row=2, column=0, pady=10)
        self.new_account_button.grid(row=3, column=0, pady=10, padx=10, sticky='e')

    def log_in(self):
        username = self.username_field.get()
        password = self.password_field.get()
        account_file = username + '.acct'
        try:
            with open(account_file, 'r') as password_file:
                stored_password = password_file.readline()
            if pbkdf2_sha256.verify(password, stored_password):
                self.logging_in_message()
                self.master.set_user_account_frame(username)
            else:
                self.invalid_login_error_message()
        except FileNotFoundError:
            self.account_does_not_exist_error_message()


class NewAccountFrame(PasswordManagerFrame):
    def __init__(self, master):
        super().__init__(master)
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
            font=("Arial", 25), command=self.save_account_info)

        self.back_button = ctk.CTkButton(
            master=self, width=100, height=40, corner_radius=4, text='back',
            font=("Arial", 14), command=master.set_login_frame)

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
        self.current_frame = LoginFrame(self)
        self.current_frame.display()

    def set_login_frame(self):
        self.current_frame.destroy()
        self.current_frame = LoginFrame(self)
        self.current_frame.display()

    def set_new_account_frame(self):
        self.current_frame.destroy()
        self.current_frame = NewAccountFrame(self)
        self.current_frame.display()

    def set_user_account_frame(self, username):
        self.current_frame.destroy()
        self.current_frame = UserAccountFrame(self, username)
        self.current_frame.display()

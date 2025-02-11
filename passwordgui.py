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
        self.master.geometry("900x700")
        self.width = 700
        self.height = 650
        self.username = username
        self.text_box_list = []

        self.title_label = ctk.CTkLabel(master=self, font=("Arial", 28),
                                        text=f"{self.username}'s Accounts")

        self.index_label = ctk.CTkLabel(master=self, text='Index', font=self.font)
        self.account_name_label = ctk.CTkLabel(master=self, text='Account', font=self.font)
        self.username_label = ctk.CTkLabel(master=self, text='Username', font=self.font)
        self.password_label = ctk.CTkLabel(master=self, text='Password', font=self.font)

        self.index_box = ctk.CTkTextbox(master=self, width=25, height=400,
                                        wrap='none', font=self.font)
        self.account_name_box = ctk.CTkTextbox(master=self, width=250, height=400,
                                               wrap='none', font=self.font)
        self.username_box = ctk.CTkTextbox(master=self, width=250, height=400,
                                           wrap='none', font=self.font)
        self.password_box = ctk.CTkTextbox(master=self, width=250, height=400,
                                           wrap='none', font=self.font)

        self.text_box_list.append(self.index_box)
        self.text_box_list.append(self.account_name_box)
        self.text_box_list.append(self.username_box)
        self.text_box_list.append(self.password_box)

        self.new_account_name_entry = ctk.CTkEntry(master=self, font=self.font,
                                                   placeholder_text='Account Name')
        self.new_username_entry = ctk.CTkEntry(master=self, font=self.font,
                                               placeholder_text='Username or Email')
        self.new_password_entry = ctk.CTkEntry(master=self, font=self.font,
                                               placeholder_text='Password')
        self.delete_index_entry = ctk.CTkEntry(master=self, font=self.font,
                                               placeholder_text='Index to delete')

        self.delete_button = ctk.CTkButton(master=self, width=100, text='DELETE',
                                           font=self.font, fg_color='dark red',
                                           command=self.delete_account_info)

        self.add_button = ctk.CTkButton(master=self, width=100, text='ADD',
                                        font=self.font, fg_color='dark green',
                                        command=self.add_account_info)

        self.logout_button = ctk.CTkButton(master=self, width=130, text="LOG OUT",
                                           font=self.font, command=self.logout)

        self._configure_grid()  # config weights of columns and rows

        self.title_label.grid(row=0, column=1, columnspan=3, pady=20)

        self.index_label.grid(row=1, column=0, sticky='e')
        self.account_name_label.grid(row=1, column=1)
        self.username_label.grid(row=1, column=2)
        self.password_label.grid(row=1, column=3)

        self.index_box.grid(row=2, column=0, sticky='nse', padx=(30, 4))
        self.account_name_box.grid(row=2, column=1, sticky='nsew', padx=4)
        self.username_box.grid(row=2, column=2, sticky='nsew', padx=4)
        self.password_box.grid(row=2, column=3, sticky='nsew', padx=(4, 30))

        self.add_button.grid(row=3, column=0, sticky='new', pady=20, padx=10)
        self.new_account_name_entry.grid(row=3, column=1, sticky='new', pady=20, padx=10)
        self.new_username_entry.grid(row=3, column=2, sticky='new', pady=20, padx=10)
        self.new_password_entry.grid(row=3, column=3, sticky='new', pady=20, padx=10)

        self.delete_button.grid(row=4, column=0, pady=20, padx=10)
        self.delete_index_entry.grid(row=4, column=1, pady=20, padx=10, sticky='w')
        self.logout_button.grid(row=4, column=3, pady=20)

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
            box.configure(state='normal')
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

        for box in self.text_box_list:
            box.configure(state='disabled')

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

        self.new_username_entry.delete(0,999)
        self.new_account_name_entry.delete(0,999)
        self.new_password_entry.delete(0,999)

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

    def _configure_grid(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=5, uniform='a')
        self.grid_columnconfigure(2, weight=5, uniform='a')
        self.grid_columnconfigure(3, weight=5, uniform='a')

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)


class LoginFrame(PasswordManagerFrame):
    def __init__(self, master):
        super().__init__(master)
        self._configure_grid()
        self.username_field = ctk.CTkEntry(master=self, font=self.font,
                                           width=self.entry_width,
                                           height=self.widget_height,
                                           placeholder_text='Enter your username')

        self.password_field = ctk.CTkEntry(master=self, font=self.font,
                                           width=self.entry_width,
                                           height=self.widget_height,
                                           placeholder_text='Enter your password')

        self.login_button = ctk.CTkButton(master=self, text='LOG IN',
                                          width=self.button_width,
                                          height=self.widget_height,
                                          font=self.font, command=self.log_in)

        self.new_account_button = ctk.CTkButton(master=self, text='Create new account',
                                                width=self.button_width,
                                                height=self.widget_height,
                                                font=self.font,
                                                command=master.set_new_account_frame)

        self.username_field.grid(row=0, column=0, pady=10)
        self.password_field.grid(row=1, column=0, pady=10)
        self.login_button.grid(row=2, column=0, pady=10)
        self.new_account_button.grid(row=3, column=0, pady=10, padx=10, sticky='e')

    def _configure_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

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
        self._configure_grid()
        self.title_label = ctk.CTkLabel(
            master=self, font=('Arial', 26),
            text='CREATE A NEW ACCOUNT')

        self.username_field = ctk.CTkEntry(
            master=self, width=self.entry_width, height=self.widget_height,
            font=self.font, placeholder_text='Enter your username')

        self.password_field_1 = ctk.CTkEntry(
            master=self, width=self.entry_width, height=self.widget_height,
            font=self.font, placeholder_text='Enter your password')

        self.password_field_2 = ctk.CTkEntry(
            master=self, width=self.entry_width, height=self.widget_height,
            font=self.font, placeholder_text='Verify your password')

        self.create_account_button = ctk.CTkButton(
            master=self, width=self.button_width, height=self.widget_height,
            font=self.font, text='CREATE ACCOUNT', command=self.create_account)

        self.back_button = ctk.CTkButton(
            master=self, width=self.button_width, height=self.widget_height,
            font=self.font, text='back', command=master.set_login_frame)

        self.title_label.grid(row=0)
        self.username_field.grid(row=1, pady=10)
        self.password_field_1.grid(row=2, pady=10)
        self.password_field_2.grid(row=3, pady=10)
        self.create_account_button.grid(row=4, pady=10)
        self.back_button.grid(row=5, sticky='se', padx=10, pady=10)

    def create_account(self):
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

    def _configure_grid(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)


class PasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.size = (500, 450)
        self.geometry(f"{self.size[0]}x{self.size[1]}")
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

import customtkinter as ctk
import tkinter as tk

from passwordmanagerframe import PasswordManagerFrame
from passlib.hash import pbkdf2_sha256
from background import BackgroundFrame


logged_in = False
user_acct = None





class UserAccountFrame(PasswordManagerFrame):
    def __init__(self, username=None):
        super().__init__()
        self.username = username

        self.title_label = ctk.CTkLabel(master=self, width=450, height=80,
                                        font=("Arial", 20),
                                        text=str(self.username) + "'S ACCOUNTS")


class LoginFrame(PasswordManagerFrame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.username_field = ctk.CTkEntry(master=self, width=340, height=60,
                                           corner_radius=10, font=("Arial", 20),
                                           placeholder_text='Enter your username'
                                           )

        self.password_field = ctk.CTkEntry(master=self, width=340, height=60,
                                           corner_radius=10, font=("Arial", 20),
                                           placeholder_text='Enter your password')

        self.login_button = ctk.CTkButton(master=self, width=200, height=60,
                                          corner_radius=10, text='LOG IN',
                                          text_color='black', fg_color='gray',
                                          border_color='dark blue',
                                          border_width=2, font=("Arial", 25),
                                          command=self.log_in)

        self.new_account_button = ctk.CTkButton(master=self, width=160, height=40,
                                                corner_radius=4, text='Create new account',
                                                text_color='black', fg_color='gray',
                                                border_color='dark blue',
                                                border_width=1, font=("Arial", 14),
                                                command=master.set_new_acct_frame)

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
                master.set_user_acct_frame()
            else:
                self.invalid_login_error_message()
        except FileNotFoundError:
            self.account_does_not_exist_error_message()
        except Exception:
            self.generic_error_message()


class NewAccountFrame(PasswordManagerFrame):
    def __init__(self, master):
        super().__init__()
        self.title_label = ctk.CTkLabel(master=self, width=450, height=80,
                                        font=("Arial", 20),
                                        text='CREATE A NEW ACCOUNT')

        self.username_field = ctk.CTkEntry(master=self, width=340, height=60,
                                           corner_radius=10, font=("Arial", 20),
                                           placeholder_text='Enter your username'
                                           )

        self.password_field_1 = ctk.CTkEntry(master=self, width=340, height=60,
                                             corner_radius=10, font=("Arial", 20),
                                             placeholder_text='Enter your password')

        self.password_field_2 = ctk.CTkEntry(master=self, width=340, height=60,
                                             corner_radius=10, font=("Arial", 20),
                                             placeholder_text='Verify your password')

        self.create_account_button = ctk.CTkButton(master=self, width=220, height=60,
                                                   corner_radius=10, text='CREATE ACCOUNT',
                                                   text_color='black', fg_color='gray',
                                                   border_color='dark blue',
                                                   border_width=2, font=("Arial", 25),
                                                   command=self.save_account_info)

        self.back_button = ctk.CTkButton(master=self, width=100, height=40,
                                         corner_radius=4, text='back', text_color='black',
                                         fg_color='gray', border_color='dark blue',
                                         border_width=1, font=("Arial", 14),
                                         command=master.set_login_frame)

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

        try:
            with open(new_filename, 'r') as check_file:
                self.account_exists_error_message()
        except FileNotFoundError:
            if pass1 == pass2:
                hashed_password = pbkdf2_sha256.hash(pass1)
                with open(new_filename, 'w') as new_password_file:
                    new_password_file.write(hashed_password)
                self.account_created_message()
            else:
                self.nonmatching_password_error_message()
        except Exception:
            self.generic_error_message()


class PasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('850x850')
        self.title("Kyle's Passwords")

        my_background_frame = BackgroundFrame(self)

        self.login_frame = LoginFrame(self)
        self.new_acct_frame = NewAccountFrame(self)
        self.user_frame = UserAccountFrame(self)
        self.login_frame.display()

    def set_login_frame(self):
        self.new_acct_frame.place_forget()
        self.login_frame.display()

    def set_new_acct_frame(self):
        self.login_frame.place_forget()
        self.new_acct_frame.display()

    def set_user_acct_frame(self):
        self.login_frame.place_forget()
        self.user_frame.display()

import os.path

import customtkinter as ctk
import tkinter as tk
# from os.path import exists

from passwordmanagerframe import PasswordManagerFrame
from passlib.hash import pbkdf2_sha256
from background import BackgroundFrame


class UserAccountFrame(PasswordManagerFrame):
    def __init__(self, username=None):
        super().__init__()
        self.username = username

        self.title_label = ctk.CTkLabel(
            master=self, width=100, height=40, font=("Arial", 24), )

        self.display_box = ctk.CTkScrollableFrame(master=self, width=450, height=450)
        self.new_username_entry = ctk.CTkEntry(
            master=self, width=140, height=50, placeholder_text='Username',
            font=("Arial", 20))

        self.new_password_entry = ctk.CTkEntry(
            master=self, width=140, height=50, placeholder_text='Password',
            font=("Arial", 20))

        self.delete_button = ctk.CTkButton(
            master=self, width=140, height=50, text='DELETE', fg_color='dark red',
            text_color='black', font=("Arial", 20))

        self.add_button = ctk.CTkButton(
            master=self, width=140, height=50, text='ADD', fg_color='dark green',
            text_color='black', font=("Arial", 20))

        self.title_label.place(relx=0.5, rely=0.08, anchor='center')
        self.display_box.place(relx=0.6, rely=0.58, anchor='center')
        self.new_username_entry.place(relx=0.15, rely=0.25, anchor='center')
        self.new_password_entry.place(relx=0.15, rely=0.4, anchor='center')
        self.add_button.place(relx=0.15, rely=0.55, anchor='center')
        self.delete_button.place(relx=0.15, rely=0.7, anchor='center')

    def display(self):
        super().display()
        self.title_label.configure(text=self.username + "'s Passwords")


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
        #except Exception as e:
            #self.generic_error_message(e)


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
        self.geometry('800x800')
        self.title("Kyle's Passwords")

        self.background_frame = BackgroundFrame(self)
        self.login_frame = LoginFrame(self)
        self.new_account_frame = NewAccountFrame(self)
        self.user_account_frame = UserAccountFrame(self)
        self.login_frame.display()
        self.resizable(width=False, height=False)

    def set_login_frame(self):
        self.new_account_frame.place_forget()
        self.new_account_frame.clear_entries()
        self.login_frame.display()

    def set_new_account_frame(self):
        self.login_frame.place_forget()
        self.login_frame.clear_entries()
        self.new_account_frame.display()

    def set_user_account_frame(self, username):
        self.user_account_frame.username = username
        self.login_frame.place_forget()
        self.login_frame.clear_entries()
        self.user_account_frame.display()

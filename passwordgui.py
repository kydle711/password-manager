import customtkinter as ctk
import tkinter as tk

from tkinter import messagebox
from PIL import Image
from passlib.hash import pbkdf2_sha256

logged_in = False
user_acct = None

class BackgroundLabel(ctk.CTkLabel):
    def __init__(self, master):
        super().__init__(master)
        self.image = ctk.CTkImage(dark_image=Image.open('images/circuitboard.jpeg'),
                                  size=(850, 850))
        self.configure(text="", image=self.image, anchor='center')
        self.pack(expand=1, fill='both')


class BackgroundFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()


class UserAccountFrame(tk.Frame):
    def __init__(self, username=None):
        super().__init__()
        self.username = username

        self.title_label = ctk.CTkLabel(master=self, width=450, height=80,
                                        font=("Arial", 20),
                                        text=self.username + "'S ACCOUNTS")



class LoginFrame(tk.Frame):
    def log_in(self, username_field, password_field):
        username = username_field.get()
        password = password_field.get()
        account_file = username + '.acct'
        try:
            with open(account_file, 'r') as password_file:
                stored_password = password_file.readline()
            if pbkdf2_sha256.verify(password, stored_password):
                logged_in = True
                user_acct = username
                self.logging_in_message()
                return logged_in, user_acct
            else:
                self.invalid_login_error_message()
        except FileNotFoundError:
            self.account_does_not_exist_error_message()
        except Exception:
            self.generic_error_message()

    def __init__(self, master):
        super().__init__()
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
                                          command=lambda: self.log_in(
                                              self.username_field,
                                              self.password_field)
                                          )

        self.new_account_button = ctk.CTkButton(master=self, width=160, height=40,
                                                corner_radius=4, text='Create new account',
                                                text_color='black', fg_color='gray',
                                                border_color='dark blue',
                                                border_width=1, font=("Arial", 14),
                                                command=lambda: master.set_new_acct_frame())

        self.message_popup = tk.messagebox

        self.login_button.place(relx=0.5, rely=0.7, anchor='center')
        self.new_account_button.place(relx=0.83, rely=0.93, anchor='center')
        self.username_field.place(relx=0.5, rely=0.3, anchor='center')
        self.password_field.place(relx=0.5, rely=0.5, anchor='center')

    def display(self):
        self.configure(width=650, height=650)
        self.place(relx=0.5, rely=0.5, anchor='center')

    def account_does_not_exist_error_message(self):
        self.message_popup.showerror(title="ERROR", message="Account does not exist!",
                                     parent=self)

    def invalid_login_error_message(self):
        self.message_popup.showerror(title="ERROR", message="Login info invalid!",
                                     parent=self)

    def generic_error_message(self):
        self.message_popup.showerror(title="ERROR", message="Something went wrong!",
                                     parent=self)

    def logging_in_message(self):
        self.message_popup.showinfo(title='LOGGING IN', message="Logging in...",
                                    parent=self)


class NewAccountFrame(tk.Frame):
    def save_account_info(self, username_field, pass_field_1, pass_field_2):
        username = username_field.get()
        pass1 = pass_field_1.get()
        pass2 = pass_field_2.get()
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
                                                   command=lambda: self.save_account_info(
                                                       username_field=self.username_field,
                                                       pass_field_1=self.password_field_1,
                                                       pass_field_2=self.password_field_2
                                                   ))

        self.back_button = ctk.CTkButton(master=self, width=100, height=40,
                                         corner_radius=4, text='back', text_color='black',
                                         fg_color='gray', border_color='dark blue',
                                         border_width=1, font=("Arial", 14),
                                         command=lambda: master.set_login_frame())

        self.message_popup = tk.messagebox

        self.title_label.place(relx=0.5, rely=0.1, anchor='center')
        self.create_account_button.place(relx=0.5, rely=0.85, anchor='center')
        self.username_field.place(relx=0.5, rely=0.2, anchor='center')
        self.password_field_1.place(relx=0.5, rely=0.35, anchor='center')
        self.password_field_2.place(relx=0.5, rely=0.50, anchor='center')
        self.back_button.place(relx=0.88, rely=0.92, anchor='center')

    def display(self):
        self.configure(width=650, height=650)
        self.place(relx=0.5, rely=0.5, anchor='center')

    def nonmatching_password_error_message(self):
        self.message_popup.showerror(title="ERROR", message="Passwords do not match!",
                                   parent=self)

    def account_exists_error_message(self):
        self.message_popup.showerror(title="ERROR", message="Account already exists!",
                                   parent=self)

    def generic_error_message(self):
        self.message_popup.showerror(title="ERROR", message="Something went wrong!",
                                   parent=self)

    def account_created_message(self):
        self.message_popup.showinfo(title="ACCOUNT CREATED", message="Account \n"
                                    "successfully created", parent=self)


class PasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('850x850')
        self.title("Kyle's Passwords")

        my_background_frame = BackgroundFrame(self)
        my_background = BackgroundLabel(my_background_frame)

        self.login_frame = LoginFrame(self)
        self.new_acct_frame = NewAccountFrame(self)
        self.login_frame.display()

    def set_login_frame(self):
        self.new_acct_frame.place_forget()
        self.login_frame.display()

    def set_new_acct_frame(self):
        self.login_frame.place_forget()
        self.new_acct_frame.display()

    def set_user_acct_frame(self):
        pass

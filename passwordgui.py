import customtkinter as ctk
import tkinter as tk

from PIL import Image


class BackgroundLabel(ctk.CTkLabel):
    def __init__(self, master):
        super().__init__(master)
        self.image = ctk.CTkImage(dark_image=Image.open('images/circuitboard.jpeg'),
                                  size=(850, 850))
        self.configure(text="", image=self.image, anchor='center')
        self.pack(expand=1, fill='both')


class BackgroundFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()


class LoginFrame(tk.Frame):
    def log_in(self, username_field, password_field):
        username = username_field.get()
        password = password_field.get()
        account_file = username + '.txt'
        try:
            with open(account_file, 'r') as password_file:
                if password_file.readline() == password:
                    print("Logging in...")
                else:
                    print("invalid login info")
        except FileNotFoundError:
            print("Account file does not exist")

    def display_new_account_frame(self):
        pass

    def __init__(self, master):
        super().__init__()
        self.username_field = ctk.CTkEntry(master=self, width=340, height=80,
                                           corner_radius=10, font=("Arial", 20),
                                           placeholder_text='Enter your username'
                                           )

        self.password_field = ctk.CTkEntry(master=self, width=340, height=80,
                                           corner_radius=10, font=("Arial", 20),
                                           placeholder_text='Enter your password')

        self.login_button = ctk.CTkButton(master=self, width=200, height=80,
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

        self.login_button.place(relx=0.5, rely=0.7, anchor='center')
        self.new_account_button.place(relx=0.83, rely=0.93, anchor='center')
        self.username_field.place(relx=0.5, rely=0.3, anchor='center')
        self.password_field.place(relx=0.5, rely=0.5, anchor='center')

    def display(self):
        self.configure(width=650, height=650)
        self.place(relx=0.5, rely=0.5, anchor='center')


class NewAccountFrame(tk.Frame):
    def save_account_info(self, username_field, pass_field_1, pass_field_2):
        pass

    def __init__(self, master):
        super().__init__()
        self.title_label = ctk.CTkLabel(master=self, width=450, height=80,
                                        font=("Arial", 20),
                                        text='CREATE A NEW ACCOUNT')

        self.username_field = ctk.CTkEntry(master=self, width=340, height=80,
                                           corner_radius=10, font=("Arial", 20),
                                           placeholder_text='Enter your username'
                                           )

        self.password_field_1 = ctk.CTkEntry(master=self, width=340, height=80,
                                             corner_radius=10, font=("Arial", 20),
                                             placeholder_text='Enter your password')

        self.password_field_2 = ctk.CTkEntry(master=self, width=340, height=80,
                                             corner_radius=10, font=("Arial", 20),
                                             placeholder_text='Verify your password')

        self.create_account_button = ctk.CTkButton(master=self, width=220, height=80,
                                                   corner_radius=10, text='CREATE ACCOUNT',
                                                   text_color='black', fg_color='gray',
                                                   border_color='dark blue',
                                                   border_width=2, font=("Arial", 25),
                                                   command=None)

        self.back_button = ctk.CTkButton(master=self, width=100, height=40,
                                         corner_radius=10, text='back', text_color='black',
                                         fg_color='gray', border_color='dark blue',
                                         border_width=1, font=("Arial",14),
                                         command=lambda: master.set_login_frame())

        self.title_label.place(relx=0.5, rely=0.1, anchor='center')
        self.create_account_button.place(relx=0.5, rely=0.85, anchor='center')
        self.username_field.place(relx=0.5, rely=0.25, anchor='center')
        self.password_field_1.place(relx=0.5, rely=0.45, anchor='center')
        self.password_field_2.place(relx=0.5, rely=0.65, anchor='center')
        self.back_button.place(relx=0.88, rely=0.92, anchor='center')

    def display(self):
        self.configure(width=650, height=650)
        self.place(relx=0.5, rely=0.5, anchor='center')



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

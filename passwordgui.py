import customtkinter as ctk

from PIL import Image


class BackgroundLabel(ctk.CTkLabel):
    def __init__(self, master):
        super().__init__(master)
        self.image = ctk.CTkImage(dark_image=Image.open('images/circuitboard.jpeg'),
                                  size=(850,850))
        self.configure(text="", image=self.image, anchor='center')
        self.pack(expand=1, fill='both')


class BackgroundFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

class LoginFrame(ctk.CTkFrame):
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

        #print("Username: ", username)
        #print("Password: ", password)

    def __init__(self, master):
        super().__init__(master)
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
                                           border_width=2, font=("Arial",25),
                                          command=lambda: self.log_in(
                                              self.username_field,
                                              self.password_field)
                                           )


        self.login_button.place(relx=0.5, rely=0.8, anchor='center')
        self.username_field.place(relx=0.5, rely=0.3, anchor='center')
        self.password_field.place(relx=0.5, rely=0.5, anchor='center')
        self.place(relx=0.5, rely=0.5, anchor='center')


class PasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('850x850')
        self.title("Kyle's Passwords")

        my_background_frame = BackgroundFrame(self)
        my_background = BackgroundLabel(my_background_frame)

        my_login_frame = LoginFrame(self)
        my_login_frame.configure(width=650, height=650)

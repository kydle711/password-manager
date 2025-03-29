import customtkinter as ctk

from loginframe import LoginFrame
from newaccountframe import NewAccountFrame
from useraccountframe import UserAccountFrame

ctk.set_default_color_theme("green")


class PasswordManagerWindow(ctk.CTk):
    def __init__(self, password_manager):
        super().__init__()
        self.set_size()
        self.title("Password Manager")
        self.current_frame = LoginFrame(self)
        self.current_frame.display()
        self.password_manager = password_manager

    def set_size(self, size=('500', '450')):
        self.geometry('x'.join(size))

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

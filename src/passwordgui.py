import os

import tkinter
import customtkinter as ctk
import json

from loginframe import LoginFrame
from newaccountframe import NewAccountFrame
from useraccountframe import UserAccountFrame
from usermenuframe import UserMenuFrame


CONFIG_FILE_PATH = os.path.join('..', 'settings', 'config.json')
ICON_FILE_PATH = os.path.join('..', 'assets', 'lock.png')


class PasswordManagerWindow(ctk.CTk):
    def __init__(self, password_manager):
        super().__init__()

        self._load_config_settings()
        self.set_size()
        self.title("Password Manager")
        self.iconphoto(True, tkinter.PhotoImage(file=ICON_FILE_PATH))
        self.current_frame = LoginFrame(self)
        self.current_frame.display()
        self.password_manager = password_manager

    """ Config methods """

    @staticmethod
    def _read_config_file() -> dict:
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            return json.load(config_file)

    @staticmethod
    def _load_config_settings():
        settings = PasswordManagerWindow._read_config_file()
        ctk.set_appearance_mode(settings["appearance mode"])
        if settings['internal theme'] is not None:
            ctk.set_default_color_theme(settings['internal theme'])
        else:
            ctk.set_default_color_theme(os.path.join(*settings['external theme']))

    def set_size(self, size=('500', '450')):
        self.geometry('x'.join(size))

    @staticmethod
    def rewrite_config_file(new_settings: dict):
        current_settings = PasswordManagerWindow._read_config_file()
        for option in new_settings:
            if option in current_settings:
                current_settings[option] = new_settings[option]

        with open(CONFIG_FILE_PATH, 'w') as config_file:
            json.dump(current_settings, config_file, indent='\t')

    """ Change frame methods """

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

    def set_user_menu_frame(self, username):
        self.current_frame.destroy()
        self.current_frame = UserMenuFrame(self, username)
        self.current_frame.display()

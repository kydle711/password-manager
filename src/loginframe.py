import customtkinter as ctk

from passwordmanagerframe import PasswordManagerFrame


class LoginFrame(PasswordManagerFrame):
    """ The LoginFrame is the opening page of the app. Interfaces with the
    PasswordManager(master) through the PasswordManagerWindow to make is function calls.
    """
    def __init__(self, master):
        super().__init__(master)
        self._configure_grid()
        master.set_size(min_height=350, min_width=300)

        self.title_label = ctk.CTkLabel(master=self, font=self.title_font,
                                        text="LOG IN")
        self.username_field = ctk.CTkEntry(master=self, font=self.font,
                                           width=self.entry_width,
                                           height=self.widget_height,
                                           placeholder_text='Enter username')

        self.password_field = ctk.CTkEntry(master=self, font=self.font,
                                           width=self.entry_width, show='*',
                                           height=self.widget_height,
                                           placeholder_text='Enter password')

        self.login_button = ctk.CTkButton(master=self, text='LOG IN',
                                          width=self.button_width,
                                          height=self.widget_height,
                                          font=self.font, command=self.request_login)

        self.new_account_button = ctk.CTkButton(master=self, text='CREATE ACCOUNT',
                                                width=self.button_width,
                                                height=self.widget_height,
                                                font=self.font,
                                                command=self.set_new_account_frame)

        self.title_label.grid(row=0, column=0, pady=10, sticky='s')
        self.username_field.grid(row=1, column=0, pady=10)
        self.password_field.grid(row=2, column=0, pady=10)
        self.login_button.grid(row=3, column=0, pady=10)
        self.new_account_button.grid(row=4, column=0, pady=10, padx=10, sticky='e')

    def request_login(self):
        username, password = self._get_login_info()
        self.master.password_manager.login(username, password)

    def _configure_grid(self):
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)

    def _get_login_info(self):
        username = self.username_field.get()
        password = self.password_field.get()
        return username, password

    def set_new_account_frame(self):
        self.master.set_new_account_frame()

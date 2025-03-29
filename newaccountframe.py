import customtkinter as ctk

from passwordmanagerframe import PasswordManagerFrame


class NewAccountFrame(PasswordManagerFrame):
    def __init__(self, master):
        super().__init__(master)
        self.text_entry_list = []
        master.set_size()
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

        self.text_entry_list.append(self.username_field)
        self.text_entry_list.append(self.password_field_1)
        self.text_entry_list.append(self.password_field_2)

        self.create_account_button = ctk.CTkButton(
            master=self, width=self.button_width, height=self.widget_height,
            font=self.font, text='CREATE ACCOUNT', command=self.request_new_account)

        self.back_button = ctk.CTkButton(
            master=self, width=self.button_width, height=self.widget_height,
            font=self.font, text='back', command=self.go_back)

        self.title_label.grid(row=0)
        self.username_field.grid(row=1, pady=10)
        self.password_field_1.grid(row=2, pady=10)
        self.password_field_2.grid(row=3, pady=10)
        self.create_account_button.grid(row=4, pady=10)
        self.back_button.grid(row=5, sticky='se', padx=10, pady=10)

    def _get_new_account_info(self):
        username = self.username_field.get()
        pass1 = self.password_field_1.get()
        pass2 = self.password_field_2.get()
        return username, pass1, pass2

    def _configure_grid(self):
        for i in range(5):
            self.rowconfigure(i, weight=1)

    def _clear_fields(self):
        for field in self.text_entry_list:
            field.delete(0, 999)

    def request_new_account(self):
        username, pass1, pass2 = self._get_new_account_info()
        self.master.password_manager.create_new_local_account(username, pass1, pass2)
        self._clear_fields()

    def go_back(self):
        self.master.set_login_frame()
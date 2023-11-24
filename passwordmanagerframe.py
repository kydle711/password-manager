import tkinter as tk
from tkinter import messagebox


class PasswordManagerFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self.message_popup = tk.messagebox

    def display(self):
        self.configure(width=650, height=650)
        self.place(relx=0.5, rely=0.5, anchor='center')

    def clear_entries(self):
        for widget in self.winfo_children():
            if 'entry' in widget.winfo_name():
                widget.delete(0, tk.END)

    def account_does_not_exist_error_message(self):
        self.message_popup.showerror(
            title="ERROR", message="Account does not exist!", parent=self)

    def invalid_login_error_message(self):
        self.message_popup.showerror(
            title="ERROR", message="Login info invalid!", parent=self)

    def generic_error_message(self, error_name):
        self.message_popup.showerror(
            title=f"ERROR: {error_name}", message=f"Something went wrong!:\n{error_name}",
            parent=self)

    def logging_in_message(self):
        self.message_popup.showinfo(
            title='LOGGING IN', message="Logging in...", parent=self)

    def nonmatching_password_error_message(self):
        self.message_popup.showerror(
            title="ERROR", message="Passwords do not match!", parent=self)

    def account_exists_error_message(self):
        self.message_popup.showerror(
            title="ERROR", message="Account already exists!", parent=self)

    def account_created_message(self):
        self.message_popup.showinfo(
            title="ACCOUNT CREATED", message="Account successfully created",
            parent=self)

    def username_too_short_error(self):
        self.message_popup.showerror(
            title="USERNAME TOO SHORT", message="Username should be 6 characters or more",
            parent=self
        )

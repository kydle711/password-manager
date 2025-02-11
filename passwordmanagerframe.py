import tkinter as tk
from customtkinter import CTkFrame
from tkinter import messagebox


class PasswordManagerFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.message_popup = tk.messagebox

    def display(self):
        self.pack(expand=True, fill='both', padx=30, pady=30)

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

    def account_info_saved_message(self):
        self.message_popup.showinfo(
            title="ACCOUNT INFO SAVED", message="Account info successfully saved!",
            parent=self)

    def account_info_delete_confirmation(self, account_name, username, password):
        return self.message_popup.askyesno(
            title="CONFIRM DELETION",
            message="Are you sure you would like to delete this account?\n"
                    f"{account_name, username, password}",
            parent=self)

    def deletion_canceled_message(self):
        self.message_popup.showinfo(
            title="DELETION CANCELED", message="Deletion request has been canceled",
            parent=self)

    def invalid_deletion_error_message(self):
        self.message_popup.showerror(title="UNABLE TO DELETE",
                                     message="Please enter the index number of the account to delete",
                                     parent=self)

    def account_info_deleted_message(self):
        self.message_popup.showinfo(
            title="ACCOUNT INFO DELETED", message="Account info successfully deleted!",
            parent=self)

    def invalid_account_info_error_message(self):
        self.message_popup.showerror(
            title="INCOMPLETE ACCOUNT DATA",
            message="Fill in all account info fields",
            parent=self)

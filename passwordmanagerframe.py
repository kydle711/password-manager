import tkinter as tk
from tkinter import messagebox


class PasswordManagerFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self.message_popup = tk.messagebox

    def display(self):
        self.configure(width=850, height=650)
        self.place(relx=0.5, rely=0.5, anchor='center')

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

    def account_info_delete_confirmation_request(self):
        return self.message_popup.askyesno(
            title="CONFIRM DELETION",
            message="Are you sure you would like to delete this account?",
            parent=self)

    def deletion_canceled_message(self):
        self.message_popup.showinfo(
            title="DELETION CANCELED", message="Deletion request has been canceled",
            parent=self)

    def invalid_deletion_error_message(self):
        self.message_popup.showerror(title="UNABLE TO DELETE",
                                     message="Invalid deletion request. Enter the account info you would\n"
                                             " like to delete", parent=self)

    def account_info_deleted_message(self):
        self.message_popup.showinfo(
            title="ACCOUNT INFO DELETED", message="Account info successfully deleted!",
            parent=self)

    def invalid_account_info_error_message(self):
        self.message_popup.showerror(
            title="USERNAME OR PASSWORD NOT ACCEPTED",
            message="Verify no fields are left blank",
            parent=self)

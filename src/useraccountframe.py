import customtkinter as ctk

from passwordmanagerframe import PasswordManagerFrame


class UserAccountFrame(PasswordManagerFrame):
    def __init__(self, master, username):
        super().__init__(master)
        master.set_size(('900', '700'))
        self.width = 700
        self.height = 650
        self.username = username
        self.text_box_list = []
        self.entry_box_list = []

        self._configure_labels()  # config all elements
        self._configure_boxes()
        self._configure_entries()
        self._configure_buttons()

        self._configure_grid()  # config weights of columns and rows

        self._grid_labels()  # Place all elements
        self._grid_boxes()
        self._grid_entries()
        self._grid_buttons()

    def display(self):
        super().display()
        self.title_label.configure(text=f"{self.username}'s Accounts")
        self._print_account_list()

    def clear_fields(self):
        for field in self.entry_box_list:
            field.delete(0, 999)

    def _config_write_text_boxes(self):
        for box in self.text_box_list:
            box.configure(state='normal')
            box.delete("0.0", "end")

    def _config_read_text_boxes(self):
        for box in self.text_box_list:
            box.configure(state='disabled')

    def _get_delete_index(self) -> str:
        return self.delete_index_entry.get()

    def _get_new_account_info(self) -> tuple:
        new_account = self.new_account_name_entry.get()
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        return new_account, new_username, new_password

    def _print_account_list(self,):
        self._config_write_text_boxes()
        account_data = self.master.password_manager.read_account_data()

        i = 1
        for item in account_data:
            self.index_box.insert(f"{i}.0", f"{item[0]}\n")
            self.account_name_box.insert(f"{i}.0", f"{item[1]}\n")
            self.username_box.insert(f"{i}.0", f"{item[2]}\n")
            self.password_box.insert(f"{i}.0", f"{item[3]}\n")
            i += 1

        self._config_read_text_boxes()

    def request_add_account(self):
        account_info = self._get_new_account_info()
        confirmation = self.master.password_manager.add_account_info(account_info)
        if confirmation:
            self.clear_fields()
            self._print_account_list()

    def request_delete_account(self):
        delete_index = self._get_delete_index()
        self.master.password_manager.delete_account_info(delete_index)
        self._print_account_list()

    def logout(self):
        self.master.password_manager.logout()

    def open_user_menu(self):
        self.master.password_manager.open_menu()

    def scroll_boxes(self, *args):
        for box in self.text_box_list:
            box.yview(*args)

    def _configure_grid(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=5, uniform='a')
        self.grid_columnconfigure(2, weight=5, uniform='a')
        self.grid_columnconfigure(3, weight=5, uniform='a')

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)

    def _configure_labels(self):
        self.title_label = ctk.CTkLabel(master=self, font=("Arial", 28),
                                        text=f"{self.username}'s Accounts")

        self.index_label = ctk.CTkLabel(master=self, text='Index', font=self.font)
        self.account_name_label = ctk.CTkLabel(master=self, text='Account', font=self.font)
        self.username_label = ctk.CTkLabel(master=self, text='Username', font=self.font)
        self.password_label = ctk.CTkLabel(master=self, text='Password', font=self.font)

    def _configure_entries(self):
        self.new_account_name_entry = ctk.CTkEntry(master=self, font=self.font,
                                                   placeholder_text='Account Name')
        self.new_username_entry = ctk.CTkEntry(master=self, font=self.font,
                                               placeholder_text='Username or Email')
        self.new_password_entry = ctk.CTkEntry(master=self, font=self.font,
                                               placeholder_text='Password')
        self.delete_index_entry = ctk.CTkEntry(master=self, font=self.font,
                                               placeholder_text='Index')

        self.entry_box_list.append(self.new_account_name_entry)
        self.entry_box_list.append(self.new_username_entry)
        self.entry_box_list.append(self.new_password_entry)
        self.entry_box_list.append(self.delete_index_entry)

    def _configure_boxes(self):
        self.index_box = ctk.CTkTextbox(master=self, width=40, height=400,
                                        wrap='none', font=self.font,
                                        activate_scrollbars=False)
        self.account_name_box = ctk.CTkTextbox(master=self, width=250, height=400,
                                               wrap='none', font=self.font,
                                               activate_scrollbars=False)
        self.username_box = ctk.CTkTextbox(master=self, width=250, height=400,
                                           wrap='none', font=self.font,
                                           activate_scrollbars=False)
        self.password_box = ctk.CTkTextbox(master=self, width=250, height=400,
                                           wrap='none', font=self.font,
                                           activate_scrollbars=False)
        self.scrollbar = ctk.CTkScrollbar(master=self, command=self.scroll_boxes)

        self.text_box_list.append(self.index_box)
        self.text_box_list.append(self.account_name_box)
        self.text_box_list.append(self.username_box)
        self.text_box_list.append(self.password_box)

        # Connect boxes in list to my scrollbar
        for box in self.text_box_list:
            box.configure(yscrollcommand=self.scrollbar.set)

    def _configure_buttons(self):
        self.delete_button = ctk.CTkButton(master=self, width=100, text='DELETE',
                                           font=self.font, fg_color='dark red',
                                           command=self.request_delete_account)

        self.add_button = ctk.CTkButton(master=self, width=100, text='ADD',
                                        font=self.font, fg_color='dark green',
                                        command=self.request_add_account)

        self.logout_button = ctk.CTkButton(master=self, width=130, text="LOG OUT",
                                           font=self.font, command=self.logout)

        self.menu_button = ctk.CTkButton(master=self, width=40, text='MENU',
                                         font=self.font, command=self.open_user_menu)

    def _grid_labels(self):
        self.title_label.grid(row=0, column=1, columnspan=3, pady=20)

        self.index_label.grid(row=1, column=0, sticky='e')
        self.account_name_label.grid(row=1, column=1)
        self.username_label.grid(row=1, column=2)
        self.password_label.grid(row=1, column=3)

    def _grid_entries(self):
        self.new_account_name_entry.grid(row=3, column=1, sticky='new', pady=20, padx=10)
        self.new_username_entry.grid(row=3, column=2, sticky='new', pady=20, padx=10)
        self.new_password_entry.grid(row=3, column=3, sticky='new', pady=20, padx=10)
        self.delete_index_entry.grid(row=4, column=1, pady=20, padx=10, sticky='w')

    def _grid_boxes(self):
        self.index_box.grid(row=2, column=0, sticky='nse', padx=(30, 4))
        self.account_name_box.grid(row=2, column=1, sticky='nsew', padx=4)
        self.username_box.grid(row=2, column=2, sticky='nsew', padx=4)
        self.password_box.grid(row=2, column=3, sticky='nsew', padx=4)
        self.scrollbar.grid(row=2, column=4, sticky='ns', padx=(4,30))

    def _grid_buttons(self):
        self.add_button.grid(row=3, column=0, sticky='new', pady=20, padx=10)
        self.delete_button.grid(row=4, column=0, pady=20, padx=10)
        self.logout_button.grid(row=4, column=2, padx=10, sticky='e')
        self.menu_button.grid(row=4, column=3, padx=20, sticky='w')

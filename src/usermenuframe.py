import customtkinter as ctk

from passwordmanagerframe import PasswordManagerFrame


class UserMenuFrame(PasswordManagerFrame):
    def __init__(self, master, username):
        super().__init__(master)
        master.set_size(('900', '700'))
        self.width = 700
        self.height = 650
        self.username = username
        self.tabs = ['Appearance', 'Export', 'Change Password', 'Other']

        self._configure_grid()
        self._configure_labels()
        self._configure_buttons()

        self._configure_export_tab()

        self._grid_labels()
        self._grid_buttons()

    def go_back_to_user_frame(self):
        self.master.password_manager.return_to_user_frame()

    def _configure_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=1)

    def _configure_labels(self):
        self.title_label = ctk.CTkLabel(master=self, font=('Arial', 28), text='Settings')
        self.tabview = ctk.CTkTabview(master=self)
        for tab in self.tabs:
            self.tabview.add(tab)

    def _configure_appearance_tab(self):
        pass

    def _configure_export_tab(self):
        local_parent = self.tabview.tab("Export")
        self.export_button = ctk.CTkButton(master=local_parent, font=self.font,
                                           text="EXPORT", width=100,
                                           command=self.master.password_manager.export_data)

        self.export_button.grid()


    def _configure_password_tab(self):
        pass

    def _configure_buttons(self):
        self.back_button = ctk.CTkButton(master=self, width=100, font=self.font,
                                         text="BACK", command=self.go_back_to_user_frame)

    def _configure_submenu(self):
        pass

    def _grid_labels(self):
        self.title_label.grid(row=0, column=0, sticky='nsew', pady=10)
        self.tabview.grid(row=1, column=0, sticky='nsew', pady=10)

    def _grid_buttons(self):
        self.back_button.grid(row=2, column=0, sticky='e')



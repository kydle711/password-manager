import os
import customtkinter as ctk

from passwordmanagerframe import PasswordManagerFrame


class UserMenuFrame(PasswordManagerFrame):
    def __init__(self, master, username):
        super().__init__(master)
        master.set_size(('900', '700'))
        self.width = 700
        self.height = 650
        self.username = username
        self.tabs = ['Appearance', 'Export', 'Change Password']

        self._config_main_grid()
        self._config_main_labels()
        self._config_main_buttons()

        self._config_export_tab()
        self._config_appearance_tab()

        self._grid_main_labels()
        self._grid_main_buttons()

    """ Base user menu frame methods """

    def go_back_to_user_frame(self):
        self.master.password_manager.return_to_user_frame()

    def _config_main_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=1)

    def _config_main_labels(self):
        self.title_label = ctk.CTkLabel(master=self, font=('Arial', 28), text='Settings')
        self.tabview = ctk.CTkTabview(master=self)
        for tab in self.tabs:
            self.tabview.add(tab)

    def _config_main_buttons(self):
        self.back_button = ctk.CTkButton(master=self, width=100, font=self.font,
                                         text="BACK", command=self.go_back_to_user_frame)

    def _grid_main_labels(self):
        self.title_label.grid(row=0, column=0, sticky='nsew', pady=10)
        self.tabview.grid(row=1, column=0, sticky='nsew', pady=10)

    def _grid_main_buttons(self):
        self.back_button.grid(row=2, column=0, sticky='e')

    """ Appearance tab methods """

    def _config_appearance_tab(self):
        appearance_tab = self.tabview.tab("Appearance")
        self._config_appearance_tab_grid(master=appearance_tab)
        self._config_theme_dropdown(master=appearance_tab)

    @staticmethod
    def _config_appearance_tab_grid(master):
        for i in range(3):
            master.grid_columnconfigure(i, weight=1)
            master.grid_rowconfigure(i, weight=1)

    def _config_theme_dropdown(self, master):
        theme_selection_label = ctk.CTkLabel(master=master, text="Select Theme",
                                             font=self.font)
        theme_selection_menu = ctk.CTkOptionMenu(master=master, font=self.font)
        theme_options = [item.rstrip('.json') for item in os.listdir(os.path.join("..", "themes"))]
        theme_selection_menu.configure(values=theme_options)

        theme_selection_label.grid(row=0, column=0)
        theme_selection_menu.grid(row=1, column=0)

    """ Export tab methods """

    def _config_export_tab(self):
        local_parent = self.tabview.tab("Export")
        self.export_button = ctk.CTkButton(master=local_parent, font=self.font,
                                           text="EXPORT", width=100,
                                           command=self.master.password_manager.export_data)
        self.export_button.grid()

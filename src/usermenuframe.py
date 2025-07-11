import os
import customtkinter as ctk

from passwordmanagerframe import PasswordManagerFrame


class UserMenuFrame(PasswordManagerFrame):
    """ UserMenuFrame is capable of exporting data, so it can only be reached
    after logging in to UserAccountFrame. Allows user to export data as a CSV file,
    change theme and font size, and reset password. Other functions are in the works.
    Interfaces with PasswordManager for reading, decrypting account info, and writing
    to CSV file though PasswordManagerWindow(master)."""
    def __init__(self, master, username):
        super().__init__(master)
        master.set_size(min_width=450, min_height=450, size=('600', '700'))
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
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)

    def _config_main_labels(self):
        self.title_label = ctk.CTkLabel(master=self, font=self.title_font, text='SETTINGS')
        self.tabview = ctk.CTkTabview(master=self)
        for tab in self.tabs:
            self.tabview.add(tab)
        self.apply_font_to_tabs(self.tabview, self.font)

    @staticmethod
    def apply_font_to_tabs(tabs, font):
        """ Workaround for adjusting tabview font size since they don't have built-in
        font size attribute. """
        tabs._segmented_button.configure(font=font)  # My IDE says this is a no-no ¯\_(ツ)_/¯

    def _config_main_buttons(self):
        self.back_button = ctk.CTkButton(master=self, width=100, font=self.font,
                                         text="BACK", command=self.go_back_to_user_frame)

    def _grid_main_labels(self):
        self.title_label.grid(row=0, column=0, sticky='nsew', pady=15, padx=10)
        self.tabview.grid(row=1, column=0, sticky='nsew', pady=5, padx=10)

    def _grid_main_buttons(self):
        self.back_button.grid(row=2, column=0, sticky='e', pady=15, padx=30)

    """ Appearance tab methods """

    def update_config_request(self):
        font_size = int(self.font_size_menu.get())
        appearance_mode = self.appearance_menu.get()
        theme = self.theme_select_menu.get()
        new_settings = {"font size": font_size, "title font size": font_size+4,
                        "appearance mode": appearance_mode, "external theme": theme + ".json"}
        self.master.rewrite_config_file(new_settings)

    def _config_appearance_tab(self):
        appearance_tab = self.tabview.tab("Appearance")
        self._config_appearance_tab_grid(master=appearance_tab)
        self._config_theme_menu(master=appearance_tab)
        self._config_appearance_menu(master=appearance_tab)
        self._config_appearance_tab_buttons(master=appearance_tab)
        self._config_font_size_menu(master=appearance_tab)

    @staticmethod
    def _config_appearance_tab_grid(master):
        for i in range(3):
            master.grid_rowconfigure(i, weight=1)
            master.grid_columnconfigure(i, weight=1)

    def _config_theme_menu(self, master):
        self.theme_select_label = ctk.CTkLabel(master=master, text="THEME",
                                               font=self.font)
        self.theme_select_label.grid(row=0, column=0, pady=10, sticky='s')

        self.theme_select_menu = ctk.CTkOptionMenu(master=master, font=self.font,
                                                   dropdown_font=self.font)
        theme_options = [item.removesuffix('.json') for item in os.listdir(os.path.join("..", "themes"))]
        self.theme_select_menu.configure(values=theme_options)
        self.theme_select_menu.set(self.master.theme)  # set dropdown list to current theme
        self.theme_select_menu.grid(row=1, column=0, pady=10, sticky='n')

    def _config_appearance_menu(self, master):
        self.appearance_label = ctk.CTkLabel(master=master, text="APPEARANCE",
                                             font=self.font)
        self.appearance_label.grid(row=0, column=1, pady=10, sticky='s')

        self.appearance_menu = ctk.CTkOptionMenu(master=master, font=self.font,
                                                 dropdown_font=self.font)
        self.appearance_menu.configure(values=["Light", "Dark", "System"])
        self.appearance_menu.set(ctk.get_appearance_mode())  # Set the dropdown list to the current setting
        self.appearance_menu.grid(row=1, column=1, pady=10, sticky='n')

    def _config_font_size_menu(self, master):
        self.font_size_label = ctk.CTkLabel(master=master, text='FONT SIZE', font=self.font)
        self.font_size_label.grid(row=0, column=2, pady=10, sticky='s')

        self.font_size_menu = ctk.CTkOptionMenu(master=master, font=self.font,
                                                dropdown_font=self.font)
        self.font_size_menu.configure(values=[f"{num}" for num in range(10, 37, 2)])
        self.font_size_menu.set(self.font[1])  # parent CTks current font size
        self.font_size_menu.grid(row=1, column=2, pady=10, sticky='n')

    def _config_appearance_tab_buttons(self, master):
        self.apply_button = ctk.CTkButton(master=master, text="APPLY", font=self.font,
                                          command=self.update_config_request)
        self.apply_button.grid(row=3, column=0, padx=10, pady=10)

    """ Export tab methods """

    def _config_export_tab(self):
        local_parent = self.tabview.tab("Export")
        self.export_button = ctk.CTkButton(master=local_parent, font=self.font,
                                           text="EXPORT", width=100,
                                           command=self.master.password_manager.export_data)
        self.export_button.grid()

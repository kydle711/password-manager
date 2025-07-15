# TODO
# build app package
# unittests
# add keylisteners for buttons
# add recovery function?
# improve security?
# add change password menu
# add auto-logout
# obfuscate encryption key and hashed password

import os.path
from passwordgui import PasswordManagerWindow
from passwordmanager import PasswordManager

REL_PATH = os.path.join('..', 'data')

if __name__ == '__main__':
    password_manager = PasswordManager(data_dir = REL_PATH)  # main logic in manager
    app = PasswordManagerWindow(password_manager)  # app GUI with reference to manager
    password_manager.set_window(app)  # Link manager back to GUI to allow function calls from buttons
    app.mainloop()

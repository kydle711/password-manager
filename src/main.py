# TODO
# build app package
# unittests
# add keylisteners for buttons
# add export function?
# add recovery function?
# improve security?
# add change password menu
# add customizable settings
# add auto-logout
# obfuscate encryption key and hashed password


from passwordgui import PasswordManagerWindow
from passwordmanager import PasswordManager

if __name__ == '__main__':
    password_manager = PasswordManager()  # main logic in manager
    app = PasswordManagerWindow(password_manager)  # app GUI with reference to manager
    password_manager.set_window(app)  # Link manager back to GUI to allow function calls from buttons
    password_manager.login(username="person", password="test123")
    app.mainloop()

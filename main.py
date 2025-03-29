# TODO
# hide login password
# encrypt saved passwords
# unittests
# add keylisteners for buttons


from passwordgui import PasswordManagerWindow
from passwordmanager import PasswordManager
from passwordfilehandler import PasswordFileHandler
from encryptionkey import InfoEncrypter

if __name__ == '__main__':

    password_manager = PasswordManager()  # main logic in manager
    app = PasswordManagerWindow(password_manager)  # app GUI with reference to manager
    password_manager.set_window(app)  # Link manager back to GUI to allow function calls from buttons

    app.mainloop()

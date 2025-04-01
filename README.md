![Header](./P@55w0rd_M@n@g3r.png)

### ABOUT
A simple password manager with a customtkinter GUI. I made this program as a learning/portfolio project

## What I learned:
The first version of this project was a simple CLI password manager that stored the passwords in plain text. I've iterated over this adding more and more complexity as a way to improve my skills and continue learning. Along the way, I've learned about using GUI's to interact with the data I'm storing. I've also added a login function that saves a hashed password before you can access your account database. SQLITE3 is utilized for the database. Once you create a local account, you can add or remove passwords through the GUI. The app will encrypt all of your account information and store it in the database. I believe the most valuable lesson I've learned from this project is the importance of dependency injection and writing decoupled code. I created a working password manager, but eventually I reached a point in complexity where every new feature broke the program. At that point, I realized that everything I had written was overly dependent on other pieces of the program. This led to major refactoring of the general architecture. By decoupling the code and adding more dependency injection, the program is in a better position for future improvements.

## Future Imrovements
- Add backup method
- Further refactoring
- Improve user account display to accomodate longer lists of accounts
- Hide password input during login
- More secure local account password checks before creating account
- Add key-listeners for improved QOL when navigating or adding info
- Clear fields when account info is accepted for account storage
- More secure storage
- Background image (tkinter caused lagging previously)
- Account tags/organization

## Dependencies
- Python 3.11 or newer
- Customtkinter
- tkinter
- sqlite3


## Security
This is a practice project, and is **NOT fully secure** yet. It is more secure than saving your info in plaintext, however the encryption key is stored alongside your local account database in a text file. Please **DO NOT** rely on this program for storage of critical information.

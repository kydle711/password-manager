import os.path

import pytest

from src.passwordfilehandler import PasswordFileHandler

TEST_DB = 'test.db'
TEMP_KEY_FILE = 'temp_key.txt'

sample_account_info = [
    [i, f"account{i}", f"username{i}", f"password{i}"] for i in range(1,6)
]

print("using test account info:")
print(sample_account_info)

@pytest.fixture(scope='module')
def file_handler():
    with PasswordFileHandler(account_database=TEST_DB, key_file=TEMP_KEY_FILE) as fh:
        yield fh

    clean_test_files(TEST_DB, TEMP_KEY_FILE)


def test_add_and_read_account_info(file_handler, sample_data=sample_account_info):
    assert file_handler.read_accounts() == [] # Database should be empty

    for account in sample_data:
        file_handler.add_account_info(account[1:]) #Slice out index since it won't be added in real program

    assert file_handler.read_accounts() == sample_account_info

def test_find_account_from_index(file_handler, sample_data=sample_account_info):
    for account in sample_data:
        read_from_index_data = file_handler.find_account_from_index(account[0])
        assert read_from_index_data == account[1:]

def test_delete_account_info(file_handler, sample_data=sample_account_info):
    """ Delete one account based off of SQL index, which starts at 1"""
    """ Should delete [3, account3, username3, password3"""
    file_handler.delete_account_info(index_to_delete=3)

    sample_account_info.remove(sample_account_info[2])
    for i in range(len(sample_account_info)):
        sample_account_info[i][0] = i + 1   # Reset the indices to match the database being vacuumed

    assert file_handler.read_accounts() == sample_account_info
    print(sample_account_info)


def clean_test_files(test_db=TEST_DB, test_key=TEMP_KEY_FILE):
    try:
        print("Removing test database...")
        os.remove(test_db)
    except FileNotFoundError as e:
        print(f"File not found: may have already been removed - {e}")

    try:
        print("Removing temp key file...")
        os.remove(test_key)
    except FileNotFoundError as e:
        print(f"File not found: may have already been removed - {e}")
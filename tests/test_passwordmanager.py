import os
import tempfile
import shutil
import pytest
from unittest import mock
from src.passwordmanager import PasswordManager
from passlib.hash import pbkdf2_sha256


@pytest.fixture
def data_dir():
    tmp = tempfile.mkdtemp()
    yield tmp
    shutil.rmtree(tmp)


@pytest.fixture
def pm(data_dir):
    manager = PasswordManager(data_path=data_dir)
    manager.window = mock.Mock()
    manager.window.current_frame = mock.Mock()
    return manager


def test_create_account(pm, data_dir):
    username = "testuser"
    password = "securepass"

    pm.create_new_local_account(username, password, password)

    acct_path = os.path.join(data_dir, f"{username}.acct")
    assert os.path.exists(acct_path)

    with open(acct_path, "r") as f:
        stored = f.read()
        assert pbkdf2_sha256.verify(password, stored)

    pm.window.current_frame.account_created_message.assert_called_once()


def test_create_account_password_mismatch(pm):
    pm.create_new_local_account("user", "abcd1234", "wxyz1234")
    pm.window.current_frame.passwords_not_matching_error.assert_called_once()


def test_create_account_password_too_short(pm):
    pm.create_new_local_account("user", "123", "123")
    pm.window.current_frame.password_too_short_error.assert_called_once()


def test_create_account_username_taken(pm, data_dir):
    username = "existing"
    acct_path = os.path.join(data_dir, f"{username}.acct")
    with open(acct_path, "w") as f:
        f.write("dummyhash")

    pm.create_new_local_account(username, "strongpass", "strongpass")
    pm.window.current_frame.account_exists_error.assert_called_once()


def test_login_success(pm, data_dir):
    username = "loginuser"
    password = "mypassword"
    acct_path = os.path.join(data_dir, f"{username}.acct")
    with open(acct_path, "w") as f:
        f.write(pbkdf2_sha256.hash(password))

    pm.login(username, password)
    pm.window.set_user_account_frame.assert_called_once_with(username)


def test_login_invalid_password(pm, data_dir):
    username = "user"
    acct_path = os.path.join(data_dir, f"{username}.acct")
    with open(acct_path, "w") as f:
        f.write(pbkdf2_sha256.hash("correctpass"))

    pm.login(username, "wrongpass")
    pm.window.current_frame.invalid_login_error.assert_called_once()


def test_login_nonexistent_account(pm):
    pm.login("ghostuser", "irrelevant")
    pm.window.current_frame.account_does_not_exist_error.assert_called_once()
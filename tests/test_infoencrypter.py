import os.path
import pytest

from cryptography.fernet import Fernet
from infoencrypter import InfoEncrypter

TEMP_KEY_FILE = "temp_key.txt"

@pytest.fixture
def inf_enc(key_file = TEMP_KEY_FILE):
    yield InfoEncrypter(key_file)
    try:
        print("Deleting temp file...")
        os.remove(TEMP_KEY_FILE)
    except FileNotFoundError:
        print("File has already been removed")
    except Exception as e:
        print(f"unexpected exception: {e}")


def test_check_existing_key(inf_enc):
    open(TEMP_KEY_FILE, 'a').close()
    assert inf_enc._check_existing_key()
    os.remove(TEMP_KEY_FILE)
    assert not inf_enc._check_existing_key()

def test_generate_new_key(inf_enc):
    assert inf_enc.encryption_key is not None    # ensure a key is generated

    with open(TEMP_KEY_FILE, 'rb') as kf:  #read key from file
        read_key = kf.read()

    """ Ensure set key matches what was written to the file """
    assert read_key is not None
    assert read_key == inf_enc.encryption_key

def test_read_key(inf_enc):
    byte_string = b'test bytes'
    with open(TEMP_KEY_FILE, 'wb') as kf:
        kf.write(byte_string)

    assert inf_enc._read_key() == byte_string

def test_set_fernet(inf_enc):
    assert inf_enc.fernet is not None
    assert type(inf_enc.fernet) == Fernet

def test_encrypt_and_decrypt(inf_enc):
    test_string = 'secret password'
    encrypted_data = inf_enc.encrypt_info(test_string)
    assert test_string != encrypted_data

    decrypted_data = inf_enc.decrypt_info(encrypted_data)

    assert test_string == decrypted_data





from app.models.credentials_model import Credentials, set_env_var
from tests.test_data import CredentialsData
import pytest
import os
import json

t = CredentialsData()


def test_credentials_data():
    credentials = Credentials.create(path=t.path, **t.credentials_kwargs)

    assert credentials.data == t.credentials_kwargs

    os.remove(os.path.join(t.path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(t.path, '.piggy'))
    set_env_var(var='PATH', value=None)


def test_create_dot_piggy_dir():
    credentials = Credentials.create(path=t.path, **t.credentials_kwargs)

    assert os.path.isdir(os.path.join(t.path, '.piggy'))

    os.remove(os.path.join(t.path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(t.path, '.piggy'))
    set_env_var(var='PATH', value=None)


def test_write_credentials_to_file():
    credentials = Credentials.create(path=t.path, **t.credentials_kwargs)

    assert os.path.exists(os.path.join(t.path, '.piggy', 'credentials.json'))

    with open(os.path.join(t.path, '.piggy', 'credentials.json'), 'r') as file:
        json_file_data = file.read()
    file_data = json.loads(json_file_data)

    assert file_data == t.credentials_kwargs

    os.remove(os.path.join(t.path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(t.path, '.piggy'))
    set_env_var(var='PATH', value=None)


def test_missing_attribute():
    data = t.credentials_kwargs
    deleted_key = 'crypto_user_password'
    del data[deleted_key]
    with pytest.raises(KeyError) as error:
        credentials = Credentials.create(path=t.path, **data)

    assert error.value.args[0] == deleted_key


def test_read():
    credentials = Credentials.create(path=t.path, **t.credentials_kwargs)
    credentials1 = Credentials.read(
        credentials_file_path=os.path.join(t.path, '.piggy', 'credentials.json'))

    assert credentials.data == credentials1.data

    os.remove(os.path.join(t.path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(t.path, '.piggy'))
    set_env_var(var='PATH', value=None)


def test_update():
    credentials = Credentials.create(path=t.path, **t.credentials_kwargs)
    credentials.update(crypto_user_password='password2')

    assert credentials.data['crypto_user_password'] == 'password2'

    with open(os.path.join(t.path, '.piggy', 'credentials.json'), 'r') as file:
        json_file_data = file.read()
    file_data = json.loads(json_file_data)

    assert file_data['crypto_user_password'] == 'password2'

    os.remove(os.path.join(t.path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(t.path, '.piggy'))
    set_env_var(var='PATH', value=None)

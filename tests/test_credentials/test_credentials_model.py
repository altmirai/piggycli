from app.models.credentials_model import Credentials
import pytest
import os
import json


def test_missing_attribute(test_data):
    data = test_data.credentials_kwargs
    deleted_key = 'crypto_user_password'
    del data[deleted_key]
    with pytest.raises(KeyError) as error:
        credentials = Credentials.create(path=test_data.test_path, **data)

    assert error.value.args[0] == deleted_key


def test_read(credentials, test_data):
    credentials1 = Credentials.read(
        credentials_file_path=os.path.join(test_data.test_path, '.piggy', 'credentials.json'))

    assert credentials.data == credentials1.data


def test_update(credentials, test_data):
    credentials.update(crypto_user_password='password2')

    assert credentials.data['crypto_user_password'] == 'password2'

    with open(os.path.join(test_data.test_path, '.piggy', 'credentials.json'), 'r') as file:
        json_file_data = file.read()
    file_data = json.loads(json_file_data)

    assert file_data['crypto_user_password'] == 'password2'

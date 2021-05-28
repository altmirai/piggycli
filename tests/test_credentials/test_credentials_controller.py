from app.controllers.credentials_controller import CredentialsController
from conftest import CredentialsData
import os
import json


def test_show(credentials, test_data):

    credentials_file_path = os.path.join(
        test_data.test_path, '.piggy', 'credentials.json')

    credentials = CredentialsController()
    resp_json = credentials.show(credentials_file_path=credentials_file_path)
    resp = json.loads(resp_json)

    assert test_data.credentials_kwargs == resp['data']


def test_update(credentials, test_data):

    credentials_file_path = os.path.join(
        test_data.test_path, '.piggy', 'credentials.json')

    credentials = CredentialsController()
    resp_json = credentials.update(
        credentials_file_path=credentials_file_path, crypto_user_password="password2")
    resp = json.loads(resp_json)

    assert resp['data']['crypto_user_password'] == 'password2'

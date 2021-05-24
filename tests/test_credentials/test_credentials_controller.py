from app.controllers.credentials_controller import CredentialsController
from app.models.credentials_model import Credentials, set_env_var
from tests.test_data import CredentialsData
import os
import json


t = CredentialsData()


def clean_up():
    os.remove(os.path.join(t.path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(t.path, '.piggy'))
    set_env_var(var='PATH', value=None)


def test_create():
    credentials = CredentialsController()
    resp_json = credentials.create(path=t.path, **t.credentials_kwargs)
    resp = json.loads(resp_json)

    assert t.credentials_kwargs == resp['data']

    clean_up()


def test_show():
    credentials = Credentials.create(path=t.path, **t.credentials_kwargs)

    credentials_file_path = os.path.join(t.path, '.piggy', 'credentials.json')

    credentials = CredentialsController()
    resp_json = credentials.show(credentials_file_path=credentials_file_path)
    resp = json.loads(resp_json)

    assert t.credentials_kwargs == resp['data']

    clean_up()


def test_update():
    credentials = Credentials.create(path=t.path, **t.credentials_kwargs)

    credentials_file_path = os.path.join(t.path, '.piggy', 'credentials.json')

    credentials = CredentialsController()
    resp_json = credentials.update(
        credentials_file_path=credentials_file_path, crypto_user_password="password2")
    resp = json.loads(resp_json)

    assert resp['data']['crypto_user_password'] == 'password2'

    clean_up()

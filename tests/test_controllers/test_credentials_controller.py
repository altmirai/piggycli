from app.controllers.credentials_controller import CredentialsController
import tests.data as data
import os
import json


def test_create():
    pass


def test_create_from_file():
    pass


def test_show(credentials):
    controller = CredentialsController()
    resp_json = controller.show(
        credentials_file_path=data.credentials_file_path)
    resp = json.loads(resp_json)

    assert credentials.data == resp['data']


def test_update(credentials):
    new_password = 'P@ssword1'
    controller = CredentialsController()
    resp_json = controller.update(
        credentials_file_path=data.credentials_file_path, crypto_user_password=new_password)
    resp = json.loads(resp_json)

    assert resp['data']['crypto_user_password'] == new_password

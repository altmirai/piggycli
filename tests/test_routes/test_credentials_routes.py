from click.testing import CliRunner
from app.routes import click
from app.models.credentials_model import Credentials, set_env_var
import json
import os


def test_data():
    return {
        'credentials':
        {
            'aws_region': 'us-east-2',
            'ssh_key_name': 'Piggy_SSH_Key_91e285d1',
            "cluster_id": "cluster-e6kouniaxtf",
            'aws_access_key_id': 'MLTnp708EbxF7/9iQT29juEw77rlN931wyjls6Vp',
            'aws_secret_access_key': 'AKIA3PBN5ZODEY7MAREB',
            'customer_ca_key_password': 'password1',
            'crypto_officer_password': 'password1',
            'crypto_user_username': 'cryptouser',
            'crypto_user_password': 'password1'
        },
        'bad_file': {
            'ssh_key_name': 'Piggy_SSH_Key_91e285d1',
            "cluster_id": "cluster-e6kouniaxtf",
            'credentials_file_path': '/Users/kyle/.piggy/credentials',
            'aws_access_key_id': 'MLTnp708EbxF7/9iQT29juEw77rlN931wyjls6Vp',
            'aws_secret_access_key': 'AKIA3PBN5ZODEY7MAREB',
            'customer_ca_key_password': 'password1',
            'crypto_officer_password': 'password1',
            'crypto_user_username': 'cryptouser',
            'crypto_user_password': 'password1'

        }
    }


test_path = os.getcwd()


def clean_up():
    os.remove(os.path.join(test_path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(test_path, '.piggy'))
    set_env_var(var='PATH', value=None)


def test_credentials_set():
    data = test_data()['credentials']
    credentials = Credentials.create(path=test_path, **data)
    runner = CliRunner()
    result = runner.invoke(
        click.credentials, ['set', '-file', os.path.join(test_path, '.piggy', 'credentials.json')])
    assert result.exit_code == 0

    clean_up()


def test_credentials_create():
    data = test_data()['credentials']

    runner = CliRunner()
    result = runner.invoke(click.credentials, ['create',
                                               '-path', test_path,
                                               '-region', 'us-east-2',
                                               '-ssh_key_name', 'Piggy_SSH_Key_91e285d1',
                                               '-cluster_id', "cluster-e6kouniaxtf",
                                               '-aws_access_key_id', 'MLTnp708EbxF7/9iQT29juEw77rlN931wyjls6Vp',
                                               '-aws_secret_access_key', 'AKIA3PBN5ZODEY7MAREB',
                                               '-customer_ca_key_password', 'password1',
                                               '-crypto_officer_password', 'password1',
                                               '-crypto_user_username', 'cryptouser',
                                               '-crypto_user_password', 'password1'
                                               ])

    assert result.exit_code == 0

    clean_up()


def test_credentials_update():
    data = test_data()['credentials']
    credentials = Credentials.create(path=test_path, **data)

    runner = CliRunner()
    results = runner.invoke(
        click.credentials, ['update', '-crypto_user_password', 'password2'])

    assert results.exit_code == 0

    with open(os.path.join(test_path, '.piggy', 'credentials.json'), 'r') as file:
        json_file_data = file.read()
    file_data = json.loads(json_file_data)

    assert file_data['crypto_user_password'] == 'password2'

    clean_up()

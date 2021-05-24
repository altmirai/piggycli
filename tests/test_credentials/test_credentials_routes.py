from click.testing import CliRunner
from app.routes import click
from app.models.credentials_model import Credentials, set_env_var
from tests.test_data import CredentialsData
import json
import os


t = CredentialsData()


def clean_up():
    os.remove(os.path.join(t.path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(t.path, '.piggy'))
    set_env_var(var='PATH', value=None)


def test_credentials_set():
    credentials = Credentials.create(path=t.path, **t.credentials_kwargs)
    runner = CliRunner()
    result = runner.invoke(
        click.credentials, ['set', '-file', os.path.join(t.path, '.piggy', 'credentials.json')])
    assert result.exit_code == 0

    clean_up()


def test_credentials_create():
    runner = CliRunner()
    result = runner.invoke(click.credentials, ['create',
                                               '-path', t.path,
                                               '-region', t.aws_region,
                                               '-ssh_key_name', t.ssh_key_name,
                                               '-cluster_id', t.cluster_id,
                                               '-instance_id', t.instance_id,
                                               '-aws_access_key_id', t.aws_access_key_id,
                                               '-aws_secret_access_key', t.aws_secret_access_key,
                                               '-customer_ca_key_password', t.customer_ca_key_password,
                                               '-crypto_officer_password', t.crypto_officer_password,
                                               '-crypto_user_username', t.crypto_user_username,
                                               '-crypto_user_password', t.crypto_user_password
                                               ])

    assert result.exit_code == 0

    clean_up()


def test_credentials_update():
    credentials = Credentials.create(path=t.path, **t.credentials_kwargs)

    runner = CliRunner()
    results = runner.invoke(
        click.credentials, ['update', '-crypto_user_password', 'password2'])

    assert results.exit_code == 0

    with open(os.path.join(t.path, '.piggy', 'credentials.json'), 'r') as file:
        json_file_data = file.read()
    file_data = json.loads(json_file_data)

    assert file_data['crypto_user_password'] == 'password2'

    clean_up()

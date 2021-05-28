from click.testing import CliRunner
from app.routes import click
import json
import os


def test_credentials_set(credentials, test_data):
    runner = CliRunner()
    result = runner.invoke(
        click.credentials, ['set', '-file', os.path.join(test_data.test_path, '.piggy', 'credentials.json')])
    assert result.exit_code == 0


def test_credentials_create(test_data):
    runner = CliRunner()
    result = runner.invoke(click.credentials, ['create',
                                               '-path', test_data.test_path,
                                               '-region', test_data.aws_region,
                                               '-ssh_key_name', test_data.ssh_key_name,
                                               '-cluster_id', test_data.cluster_id,
                                               '-instance_id', test_data.instance_id,
                                               '-aws_access_key_id', test_data.aws_access_key_id,
                                               '-aws_secret_access_key', test_data.aws_secret_access_key,
                                               '-customer_ca_key_password', test_data.customer_ca_key_password,
                                               '-crypto_officer_password', test_data.crypto_officer_password,
                                               '-crypto_user_username', test_data.crypto_user_username,
                                               '-crypto_user_password', test_data.crypto_user_password
                                               ])

    assert result.exit_code == 0


def test_credentials_update(credentials, test_data):
    runner = CliRunner()
    results = runner.invoke(
        click.credentials, ['update', '-crypto_user_password', 'password2'])

    assert results.exit_code == 0

    with open(os.path.join(test_data.test_path, '.piggy', 'credentials.json'), 'r') as file:
        json_file_data = file.read()
    file_data = json.loads(json_file_data)

    assert file_data['crypto_user_password'] == 'password2'

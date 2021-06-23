# from click.testing import CliRunner
# import tests.data as data
# from app.routes import click
# import json
# import os


# def test_credentials_set(credentials):
#     runner = CliRunner()
#     result = runner.invoke(
#         click.credentials, ['set', '-file', os.path.join(data.test_path, '.piggy', 'credentials.json')])
#     assert result.exit_code == 0


# def test_credentials_create():
#     runner = CliRunner()
#     result = runner.invoke(click.credentials, ['create',
#                                                '-path', data.test_path,
#                                                '-region', data.aws_region,
#                                                '-ssh_key_name', data.ssh_key_name,
#                                                '-cluster_id', data.cluster_id,
#                                                '-instance_id', data.instance_id,
#                                                '-aws_access_key_id', data.aws_access_key_id,
#                                                '-aws_secret_access_key', data.aws_secret_access_key,
#                                                '-customer_ca_key_password', data.customer_ca_key_password,
#                                                '-crypto_officer_password', data.crypto_officer_password,
#                                                '-crypto_user_username', data.crypto_user_username,
#                                                '-crypto_user_password', data.crypto_user_password
#                                                ])

#     assert result.exit_code == 0


# def test_credentials_update(credentials):
#     runner = CliRunner()
#     results = runner.invoke(
#         click.credentials, ['update', '-crypto_user_password', 'password2'])

#     assert results.exit_code == 0

#     with open(os.path.join(data.test_path, '.piggy', 'credentials.json'), 'r') as file:
#         json_file_data = file.read()
#     file_data = json.loads(json_file_data)

#     assert file_data['crypto_user_password'] == 'password2'

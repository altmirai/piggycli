from app.controllers.setup_controller import Setup
from app.controllers.credentials_controller import CredentialsController
import boto3
import click
import json
import os
import subprocess


class Config(object):

    def __init__(self):
        with open('.env', 'r') as file:
            env_vars_json = file.read()
        env_vars = json.loads(env_vars_json)
        self.path = env_vars['PATH']
        self.credentials_file_path = os.path.join(
            self.path, '.piggy', 'credentials.json')


pass_config = click.make_pass_decorator(Config, ensure=True)


class NotRequiredIf(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if = kwargs.pop('not_required_if')
        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs['help'] = (kwargs.get('help', '') +
                          ' NOTE: This argument is mutually exclusive with %s' %
                          self.not_required_if
                          ).strip()
        super(NotRequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        we_are_present = self.name in opts
        not_required_true = ctx.params.get(self.not_required_if)

        if not_required_true:
            if we_are_present:
                raise click.UsageError(
                    "Illegal usage: `%s` is mutually exclusive with `%s`" % (
                        self.name, self.not_required_if))
            else:
                self.prompt = None
                self.required = False

        return super(NotRequiredIf, self).handle_parse_result(ctx, opts, args)


@click.group()
def piggy():
    pass


@piggy.command()
@click.option('-path', 'path', prompt='Path', required=True)
@click.option('-region', 'aws_region', prompt='AWS Region', required=True)
@click.option('-id', 'aws_access_key_id', prompt='AWS Access Key ID', required=True)
@click.option('-key', 'aws_secret_access_key', prompt='AWS Secret Access Key', required=True)
@click.option('-customer_ca_key_password', 'customer_ca_key_password', prompt='Customer CA Key Password', required=True)
@click.option('-crypto_officer_password', 'crypto_officer_password', prompt='Crypto Officer Password', required=True)
@click.option('-crypto_user_username', 'crypto_user_username', prompt='Crypto User Username', required=True)
@click.option('-crypto_user_password', 'crypto_user_password', prompt='Crypto User Password', required=True)
def setup(**kwargs):

    aws_access_key_id = kwargs['aws_access_key_id']
    aws_secret_access_key = kwargs['aws_secret_access_key']

    # ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key_id,
    #                    aws_secret_access_key=aws_secret_access_key)
    # cloudhsmv2 = boto3.client(
    #     'cloudhsmv2', aws_access_key_id=aws_access_key_id,
    #     aws_secret_access_key=aws_secret_access_key)
    ec2 = boto3.client('ec2')
    cloudhsmv2 = boto3.client('cloudhsmv2')

    setup = Setup(
        ec2=ec2,
        cloudhsmv2=cloudhsmv2,
        path=kwargs['path'],
        aws_region=kwargs['aws_region'],
        customer_ca_key_password=kwargs['customer_ca_key_password'],
        crypto_officer_password=kwargs['crypto_officer_password'],
        crypto_user_username=kwargs['crypto_user_username'],
        crypto_user_password=kwargs['crypto_user_password']
    )

    resp = setup.run()
    cluster_id = resp['cluster_id']
    ssh_key_name = resp['ssh_key_name']
    ssh_key_pem = resp['ssh_key_pem']
    instance_id = resp['instance_id']
    breakpoint()


@piggy.group()
def credentials():
    pass


@credentials.command()
@click.option('-path', 'path', type=click.Path(), prompt='Path', required=True)
@click.option('-region', 'aws_region', prompt='AWS Region', required=True)
@click.option('-ssh_key_name', 'ssh_key_name', prompt='SSH Key Name', required=True)
@click.option('-cluster_id', 'cluster_id', prompt='Cluster ID', required=True)
@click.option('-aws_access_key_id', 'aws_access_key_id', prompt='AWS Access Key ID', required=True)
@click.option('-aws_secret_access_key', 'aws_secret_access_key', prompt='AWS Secret Access Key', required=True)
@click.option('-customer_ca_key_password', 'customer_ca_key_password', prompt='Customer CA Key Password', required=True)
@click.option('-crypto_officer_password', 'crypto_officer_password', prompt='Crypto Officer Password', required=True)
@click.option('-crypto_user_username', 'crypto_user_username', prompt='Crypto User Username', required=True)
@click.option('-crypto_user_password', 'crypto_user_password', prompt='Crypto User Password', required=True)
def create(**kwargs):
    credentials = CredentialsController()
    resp = credentials.create(**kwargs)
    click.echo(resp)


@credentials.command()
@click.option('-file', 'credentials_file_path', type=click.Path(exists=True))
def set(credentials_file_path):
    credentials = CredentialsController()
    resp = credentials.show(credentials_file_path=credentials_file_path)
    click.echo(resp)


@credentials.command()
@pass_config
@click.option('-region', 'aws_region', required=False)
@click.option('-ssh_key_name', 'ssh_key_name', required=False)
@click.option('-cluster_id', 'cluster_id', required=False)
@click.option('-aws_access_key_id', 'aws_access_key_id', required=False)
@click.option('-aws_secret_access_key', 'aws_secret_access_key', required=False)
@click.option('-customer_ca_key_password', 'customer_ca_key_password', required=False)
@click.option('-crypto_officer_password', 'crypto_officer_password', required=False)
@click.option('-crypto_user_username', 'crypto_user_username', required=False)
@click.option('-crypto_user_password', 'crypto_user_password', required=False)
def update(config, **kwargs):
    update_dict = {}
    for key, value in kwargs.items():
        if value is not None:
            update_dict[key] = value

    credentials = CredentialsController()
    resp = credentials.update(
        credentials_file_path=config.credentials_file_path, **update_dict)
    click.echo(resp)

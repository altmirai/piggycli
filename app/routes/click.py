from app.controllers.setup_controller import Setup
from app.controllers.credentials_controller import CredentialsController
from app.controllers.status_controller import StatusController
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

        self.path = env_vars.get('PATH')

        if bool(self.path):
            self.credentials_file_path = os.path.join(
                self.path, '.piggy', 'credentials.json')
        else:
            self.credentials_file_path = None


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

    ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key)
    cloudhsmv2 = boto3.client(
        'cloudhsmv2', aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)

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

    credentials = CredentialsController()
    cedentials_json = credentials.create(
        path=kwargs['path'],
        aws_region=kwargs['aws_region'],
        aws_access_key_id=kwargs['aws_access_key_id'],
        aws_secret_access_key=kwargs['aws_secret_access_key'],
        customer_ca_key_password=kwargs['customer_ca_key_password'],
        crypto_officer_password=kwargs['crypto_officer_password'],
        crypto_user_username=kwargs['crypto_user_username'],
        crypto_user_password=kwargs['crypto_user_password'],
        cluster_id=resp['cluster_id'],
        instance_id=resp['instance_id'],
        ssh_key_name=resp['ssh_key_name']
    )

    click.echo(cedentials_json)


@piggy.group()
def credentials():
    pass


@credentials.command()
@click.option('-path', 'path', type=click.Path(), prompt='Path', required=True)
@click.option('-region', 'aws_region', prompt='AWS Region', required=True)
@click.option('-ssh_key_name', 'ssh_key_name', prompt='SSH Key Name', required=True)
@click.option('-cluster_id', 'cluster_id', prompt='Cluster ID', required=True)
@click.option('-instance_id', 'instance_id', prompt='Instance ID', required=True)
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
@click.option('-instance_id', 'instance_id', required=False)
@click.option('-aws_access_key_id', 'aws_access_key_id', required=False)
@click.option('-aws_secret_access_key', 'aws_secret_access_key', required=False)
@click.option('-customer_ca_key_password', 'customer_ca_key_password', required=False)
@click.option('-crypto_officer_password', 'crypto_officer_password', required=False)
@click.option('-crypto_user_username', 'crypto_user_username', required=False)
@click.option('-crypto_user_password', 'crypto_user_password', required=False)
def update(config, **kwargs):
    if bool(config.path):
        update_dict = {}
        for key, value in kwargs.items():
            if bool(value):
                update_dict[key] = value

        credentials = CredentialsController()
        resp = credentials.update(
            credentials_file_path=config.credentials_file_path, **update_dict)

        click.echo(resp)
    else:
        no_config_found()


@piggy.command()
@pass_config
@click.option('-sleep', 'action', flag_value='sleep', default=False)
@click.option('-wake', 'action', flag_value='wake', default=False)
def status(config, action):
    if bool(config.path):
        credentials = CredentialsController().create_from_file(
            credentials_file_path=config.credentials_file_path)

        aws_access_key_id = credentials.data['aws_access_key_id']
        aws_secret_access_key = credentials.data['aws_secret_access_key']

        ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key)
        cloudhsmv2 = boto3.client(
            'cloudhsmv2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        if action == 'wake':
            if click.confirm('Are you sure you want to wake the pig?'):
                click.echo('Waking the Pig!')
            else:
                click.echo('Piggy sleeps tonight!')
        elif action == 'sleep':
            if click.confirm('Are you sure you want to put the pig to sleep?'):
                click.echo('Putting the pig to bed!')
            else:
                click.echo('The pig remains active!')
        else:
            status = StatusController(credentials_file_path=config.credentials_file_path,
                                      path=config.path, ec2=ec2, cloudhsmv2=cloudhsmv2)

            click.echo(status.show())
    else:
        no_config_found()


def no_config_found():
    click.echo('')
    click.echo(
        'No config file found.'
    )
    click.echo('If you have already setup your AWS infrastructure, run piggy credentials set -file <your config file> or piggy credentials create.')
    click.echo(
        'If you have not set up your AWS infrastructre, run piggy setup.')
    click.echo('')

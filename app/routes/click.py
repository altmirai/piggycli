from app.controllers.setup_controller import Setup
from app.controllers.credentials_controller import CredentialsController
from app.controllers.status_controller import StatusController
from app.controllers.addresses_controller import AddressController
from app.controllers.tx_controller import TxController

import boto3
import click
import json
import os
import subprocess


class Config(object):

    def __init__(self):
        try:
            with open('.env', 'r') as file:
                env_vars_json = file.read()
            env_vars = json.loads(env_vars_json)

            self.path = env_vars.get('PATH')
        except:
            self.path = None

        if bool(self.path):
            self.credentials_file_path = os.path.join(
                self.path, '.piggy', 'credentials.json')
        else:
            self.credentials_file_path = None

        self.creds_exists = os.path.exists(self.credentials_file_path)


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


def no_credentials_found():
    click.echo('')
    click.echo(
        'No credentials file found.'
    )
    click.echo('If you have already setup your AWS infrastructure, run piggy credentials set -file <your config file> or piggy credentials create.')
    click.echo(
        'If you have not set up your AWS infrastructre, run piggy setup.')
    click.echo('')


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
    resource = boto3.resource(
        'ec2', aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)

    setup = Setup(
        ec2=ec2,
        cloudhsmv2=cloudhsmv2,
        resource=resource,
        path=kwargs['path'],
        aws_region=kwargs['aws_region'],
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
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
    if bool(config.creds_exists):
        update_dict = {}
        for key, value in kwargs.items():
            if bool(value):
                update_dict[key] = value

        credentials = CredentialsController()
        resp = credentials.update(
            credentials_file_path=config.credentials_file_path, **update_dict)

        click.echo(resp)
    else:
        no_credentials_found()


@piggy.command()
@pass_config
@click.option('-sleep', 'action', flag_value='sleep', default=False)
@click.option('-wake', 'action', flag_value='wake', default=False)
def status(config, action):
    if bool(config.creds_exists):
        credentials = CredentialsController().create_from_file(
            credentials_file_path=config.credentials_file_path)

        aws_access_key_id = credentials.data['aws_access_key_id']
        aws_secret_access_key = credentials.data['aws_secret_access_key']

        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        cloudhsmv2 = boto3.client(
            'cloudhsmv2',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        resource = boto3.resource(
            'ec2',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        status = StatusController(
            credentials_file_path=config.credentials_file_path,
            path=config.path,
            ec2=ec2,
            cloudhsmv2=cloudhsmv2,
            resource=resource
        )

        if action == 'wake':
            if click.confirm('Are you sure you want to wake the pig, starting an HSM costs money?'):
                resp = status.wake()
                click.echo(resp)
        elif action == 'sleep':
            if click.confirm('Are you sure you want to put the pig to sleep?'):
                resp = status.sleep()
                click.echo(resp)
        else:
            resp = status.show()
            click.echo(resp)
    else:
        no_credentials_found()


@piggy.group()
def address():
    pass


@address.command()
@pass_config
def list(config):
    if bool(config.creds_exists):
        controller = AddressController(config=config)
        resp = controller.index()
        for address in resp['data']['addresses']:
            click.echo('')
            click.echo(
                f"id: {address.id}, address: {address.address}, confirmed_balance: {address.confirmed_balance}, spent: {address.spent}")
            click.echo('')
    else:
        no_credentials_found()


@address.command()
@pass_config
def create(config):
    if bool(config.creds_exists):
        controller = AddressController(config=config)
        resp = controller.create()
        address = resp['data']['address']
        click.echo('')
        click.echo(f'id: {address.id}')
        click.echo(f'address: {address.address}')
        click.echo(f'confirmed_balance: {address.confirmed_balance}')
        click.echo(f'spent: {address.spent}')
        click.echo('')
        click.echo(f'public_key_handle: {address.pub_key_handle}')
        click.echo(f'private_key_handle: {address.private_key_handle}')
        click.echo('public_key_pem: ')
        click.echo(address.pub_key_pem)
    else:
        no_credentials_found()


@address.command()
@click.option('-id', 'id', prompt='Address ID', required=True)
@pass_config
def show(config, id):
    if bool(config.creds_exists):
        controller = AddressController(config=config)
        resp = controller.show(id=id)
        address = resp['data']['address']
        click.echo('')
        click.echo(f'id: {address.id}')
        click.echo(f'address: {address.address}')
        click.echo(f'confirmed_balance: {address.confirmed_balance}')
        click.echo(f'spent: {address.spent}')
        click.echo('')
        click.echo(f'public_key_handle: {address.pub_key_handle}')
        click.echo(f'private_key_handle: {address.private_key_handle}')
        click.echo('public_key_pem: ')
        click.echo(address.pub_key_pem)
    else:
        no_credentials_found()


@piggy.command()
@pass_config
@click.option('-all', 'all', is_flag=True, required=True, prompt="Send recipient all the BTC in address", cls=NotRequiredIf, not_required_if='partial')
@click.option('-some', 'partial', is_flag=True)
@click.option('-from', 'address_id', prompt='Sending Address ID', required=True)
@click.option('-to', 'recipient', prompt='Recipient Addreess', required=True)
@click.option('-fee', 'fee', type=click.INT, prompt='Mining Fee', required=True)
@click.option('-qty', 'value', type=click.INT, prompt='Quantity to send',  cls=NotRequiredIf, not_required_if='all')
@click.option('-caddr', 'change_address', required=True, prompt='Change address',
              cls=NotRequiredIf, not_required_if='all')
def send(config, address_id, recipient, all, partial, fee, value, change_address):
    if bool(config.creds_exists):
        controller = TxController(config=config)
        valid = controller.validate(address_id=address_id, recipient=recipient,
                                    all=all, fee=fee, value=value, change_address=change_address)

        if valid.get('error') is not None:
            click.echo('')
            click.echo(f"Danger Will Robinson! {valid['error']}")
            click.echo('')

        elif all:
            click.echo('')
            click.echo('Transation Details:')
            click.echo()
            click.echo(f"Address {valid['address'].address} will send:")
            click.echo(
                f"  * {valid['value']} SATs to {valid['recipient']}, and")
            click.echo(f"  * pay a {fee} SATs mining fee.")
            click.echo('')

            if click.confirm('Confirm send'):
                create_resp = controller.create(**valid)

        else:
            click.echo('')
            click.echo('Transation Details:')
            click.echo()
            click.echo(f"Address {valid['address'].address} will sends:")
            click.echo(
                f"  * {valid['value']} SATs to {valid['recipient']},")
            click.echo(
                f"  * {valid['change']} SATs to {valid['change_address']}, and")
            click.echo(f"  * pay a {fee} SATs mining fee.")
            click.echo('')

            if click.confirm('Confirm send'):
                resp = controller.create(**valid)

    else:
        no_credentials_found()

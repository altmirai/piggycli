from app.controllers.setup_controller import Setup
from app.models.config_model import Config
import click


@click.group()
def piggy():
    pass


@piggy.command()
@click.option('-path', 'path', prompt='Config File Path', required=True)
@click.option('-region', 'region', prompt='AWS Region', required=True)
@click.option('-id', 'aws_access_key_id', prompt='AWS Access Key ID', required=True)
@click.option('-key', 'aws_secret_access_key', prompt='AWS Secret Access Key', required=True)
def setup(path, region, aws_access_key_id, aws_secret_access_key):
    # try:
    setup = Setup()
    setup.create(
        path=path,
        region=region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    # except Exception as error:
    #     click.echo(error)


@piggy.command()
@click.option('-p', 'path', required=True)
def config(path):
    config = Config()
    config.create(path)
    click.echo(path)
    breakpoint()

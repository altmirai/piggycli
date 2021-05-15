from app.models.config_model import Config
from app.models.ssh_key_model import SSHKey
from app.models.instance_model import Instance
from app.utilities.terraform import Tf
import os
import boto3


class Setup:

    def __init__(self):

        _check_packages()
        self.ec2 = boto3.client('ec2')
        self.cloudhsmv2 = boto3.client('cloudhsmv2')

    def create(self, path, region, aws_access_key_id, aws_secret_access_key):

        config = Config(path=path)
        config.create(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        ssh_key = SSHKey.create(client=self.ec2)
        config.update(ssh_key_name=ssh_key.name)

        with open(f'{path}/{ssh_key.name}.pem', 'w') as file:
            file.write(ssh_key.material)

        build = Tf(
            region=region,
            ssh_key_name=config.ssh_key_name
        ).build()

        instance = Instance(
            client=self.ec2,
            id=build['instance_id'],
            ssh_key_file=f'{path}/{config.ssh_key_name}.pem'
        )

        instance.install_packages()

        breakpoint()

        return


class PackageNotInstalledError(Exception):
    pass


def _check_packages():
    aws_proc = os.system('aws --version')
    terraform_proc = os.system('terraform --version')
    if aws_proc != 0 and terraform_proc != 0:
        raise PackageNotInstalledError(
            'Nether AWS CLI nor Terraform are installed.')
    elif aws_proc != 0:
        raise PackageNotInstalledError('AWS CLI is not installed.')
    elif terraform_proc != 0:
        raise PackageNotInstalledError('Terraform is not installed.')
    return

from app.models.config_model import Config
from app.models.ssh_key_model import SSHKey
import os
import boto3


class Setup:
    def __init__(self):
        _check_packages()
        self.ec2 = boto3.client('ec2')
        self.cloudhsmv2 = boto3.client('cloudhsmv2')

    def create(self, path, aws_access_key_id, aws_secret_access_key):
        config = Config(path=path)
        config.create(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        ssh_key = SSHKey.create(client=self.ec2)
        config.update(
            ssh_key_name=ssh_key.name,
            ssh_key_material=ssh_key.material
        )

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

from app.models.config_model import Config
import os


class PackageNotInstalledError(Exception):
    pass


class Setup:
    def __init__(self):
        _check_packages()

    def create(self, path, aws_access_key):
        config = Config()
        config.create(path=path, aws_access_key=aws_access_key)

        return


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

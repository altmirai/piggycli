from app.models.config_model import Config
from app.models.ssh_key_model import SSHKey
from app.models.instance_model import Instance
from app.models.cluster_model import Cluster
from app.models.hsm_model import HSM
from app.models.certificate_model import Certs

from app.utilities.terraform import Tf
import os
import boto3
import time


class Setup:

    def __init__(self):

        _check_packages()
        self.ec2 = boto3.client('ec2')
        self.cloudhsmv2 = boto3.client('cloudhsmv2')

    def create(self, path, region, aws_access_key_id, aws_secret_access_key, customer_ca_key_password):

        config = Config(path=path)
        config.create(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        # config.update(ssh_key_name='Piggy_SSH_Key_5aea082f')

        ssh_key = SSHKey.create(client=self.ec2)
        config.update(ssh_key_name=ssh_key.name)

        with open(f'{path}/{ssh_key.name}.pem', 'w') as file:
            file.write(ssh_key.material)

        build = Tf(
            region=region,
            ssh_key_name=config.ssh_key_name
        ).build()

        cluster = Cluster(client=self.cloudhsmv2, id=build['cluster_id'])

        instance = Instance(
            client=self.ec2,
            id=build['instance_id'],
            ssh_key_file=f'{path}/{config.ssh_key_name}.pem'
        )

        instance.install_packages()

        _create_first_hsm(cluster=cluster, cloudhsmv2=self.cloudhsmv2)

        certs = Certs(
            pem_csr=cluster.csr,
            cluster_id=cluster.id,
            passphrase=customer_ca_key_password,
            file_path=path
        )
        certs.write_to_files()
        _initialize_cluster(cluster=cluster, certs=certs)

        certs.upload_customer_ca_cert(ec2_instance=instance)
        cluster.configure_cloudhsm_client(ec2_instance=instance)

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


def _create_first_hsm(cluster, cloudhsmv2):
    hsm = HSM.create(cluster_id=cluster.id,
                     availability_zone=cluster.azs[0], client=cloudhsmv2)

    seconds = 0
    while hsm.state != 'ACTIVE':
        time.sleep(10)
        seconds += 10
        elapsed = time.localtime(seconds)
        str_time = time.strftime("%Mm%Ss", elapsed)
        print(
            f'aws_cloudhsm_v2_HSM: Creating ... [{str_time} elapsed]')
    print(f'aws_cloudhsm_v2_HSM: Created! [{str_time} elapsed]')
    return


def _initialize_cluster(cluster, certs):
    cluster.initialize(certs)

    seconds = 0
    while cluster.state != 'INITIALIZED':
        time.sleep(10)
        seconds += 10
        elapsed = time.localtime(seconds)
        str_time = time.strftime("%Mm%Ss", elapsed)
        print(
            f'aws_cloudhsm_v2_Cluster({cluster.id}): Initiating ... [{str_time} elapsed]')
    print(
        f'aws_cloudhsm_v2_Cluster({cluster.id}): Initiated! [{str_time} elapsed]')
    return

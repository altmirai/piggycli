from app.models.credentials_model import Credentials
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
    def __init__(self, ec2, cloudhsmv2, path, aws_region, customer_ca_key_password, crypto_officer_password, crypto_user_username, crypto_user_password):
        _check_packages(packages=['aws', 'terraform'])
        self.ec2 = ec2
        self.cloudhsmv2 = cloudhsmv2
        self.path = path
        self.aws_region = aws_region
        self.customer_ca_key_password = customer_ca_key_password
        self.crypto_officer_password = crypto_officer_password
        self.crypto_user_username = crypto_user_username
        self.crypto_user_password = crypto_user_password

    def run(self):
        ssh_key = _get_ssh_key(client=self.ec2)

        resp = _build_infrastructure(
            ssh_key_name=ssh_key.name, region=self.aws_region)

        cluster = _cluster(id=resp['cluster_id'], client=self.cloudhsmv2)

        self.path = _set_path(path=self.path, cluster=cluster)

        ssh_key.write_to_file(path=self.path)
        ssh_key_file = os.path.join(self.path, f'{ssh_key.name}.pem')

        instance = _instance(
            client=self.ec2, id=resp['instance_id'], ssh_key_file=ssh_key_file)

        _hsm(cluster=cluster, client=self.cloudhsmv2)

        certs = _certs(
            cluster=cluster, customer_ca_key_password=self.customer_ca_key_password, path=self.path, instance=instance)

        _initialize_cluster(cluster=cluster, certs=certs)

        _activate_cluster(cluster=cluster, instance=instance, crypto_officer_password=self.crypto_officer_password,
                          crypto_user_username=self.crypto_user_username, crypto_user_password=self.crypto_user_password)

        return {
            'cluster_id': cluster.id,
            'ssh_key_name': ssh_key.name,
            'ssh_key_pem': ssh_key.material,
            'instance_id': instance.id
        }


def _check_packages(packages=[]):
    for package in packages:
        proc = os.system(f'{package} --version')
        if proc != 0:
            raise PackageNotInstalledError(f'{package} is not installed')
    return


def _get_ssh_key(client):
    return SSHKey.create(client=client)


def _build_infrastructure(region, ssh_key_name):
    return Tf(
        region=region,
        ssh_key_name=ssh_key_name
    ).build()


def _cluster(client, id):
    return Cluster(client=client, id=id)


def _set_path(path, cluster):
    path = os.path.join(path, cluster.id)
    if os.path.isdir(path) is False:
        os.mkdir(path)
    return path


def _instance(client, id, ssh_key_file):
    instance = Instance(client=client, id=id, ssh_key_file=ssh_key_file)
    instance.install_packages()
    return instance


def _hsm(client, cluster):
    hsm = HSM.create(
        cluster_id=cluster.id,
        availability_zone=cluster.azs[0],
        client=client
    )

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


def _certs(customer_ca_key_password, cluster, path, instance):
    certs = Certs(
        pem_csr=cluster.csr,
        cluster_id=cluster.id,
        passphrase=customer_ca_key_password,
        file_path=path
    )
    certs.write_to_files()
    certs.upload_customer_ca_cert(ec2_instance=instance)

    return certs


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


def _activate_cluster(cluster, instance, crypto_officer_password, crypto_user_username, crypto_user_password):
    cluster.activate(
        instance=instance,
        crypto_officer_password=crypto_officer_password,
        crypto_user_username=crypto_user_username,
        crypto_user_password=crypto_user_password
    )

    seconds = 0
    while cluster.state != 'ACTIVE':
        time.sleep(10)
        seconds += 10
        elapsed = time.localtime(seconds)
        str_time = time.strftime("%Mm%Ss", elapsed)
        print(
            f'aws_cloudhsm_v2_Cluster({cluster.id}): Activating ... [{str_time} elapsed]')
    print(
        f'aws_cloudhsm_v2_Cluster({cluster.id}): Active! [{str_time} elapsed]')
    return


class PackageNotInstalledError(Exception):
    pass

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
    def __init__(self, ec2, cloudhsmv2, path, aws_region, aws_access_key_id, aws_secret_access_key, customer_ca_key_password,
                 crypto_officer_password, crypto_user_username, crypto_user_password):
        _check_packages(packages=['aws', 'terraform'])
        self.ec2 = ec2
        self.cloudhsmv2 = cloudhsmv2
        self.path = path
        self.aws_region = aws_region
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.customer_ca_key_password = customer_ca_key_password
        self.crypto_officer_password = crypto_officer_password
        self.crypto_user_username = crypto_user_username
        self.crypto_user_password = crypto_user_password

    def run(self):
        ssh_key = self.ssh_key()
        resp = self.build_infrastructure(ssh_key_name=ssh_key.name)
        cluster = self.cluster(id=resp['cluster_id'])

        self.path = os.path.join(self.path, cluster.id)
        os.mkdir(self.path)

        self.config_file(
            aws_region=self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            ssh_key_name=ssh_key.name,
            cluster_id=cluster.id
        )
        ssh_key.write_to_file(path=self.path)
        ssh_key_file = os.path.join(self.path, f'{ssh_key.name}.pem')

        instance = self.instance(
            id=resp['instance_id'], ssh_key_file=ssh_key_file)

        instance.install_packages()

        self.hsm(cluster=cluster, cloudhsmv2=self.cloudhsmv2)

        certs = self.certs(cluster=cluster, instance=instance)
        certs.write_to_files()
        certs.upload_customer_ca_cert(ec2_instance=instance)
        self.config_file(
            customer_ca_key_password=self.customer_ca_key_password)

        self.initialize_cluster(cluster=cluster, certs=certs)

        self.activate_cluster(cluster=cluster, instance=instance)

        self.config_file(
            crypto_officer_password=self.crypto_officer_password,
            crypto_user_username=self.crypto_user_username,
            crypto_user_password=self.crypto_user_password
        )

        config_file_env_varriable = os.path.join(
            self.path, 'piggy_config.json')
        os.environ["PIGGY_CONFIG"] = config_file_env_varriable

        return

    def ssh_key(self):
        return SSHKey.create(client=self.ec2)

    def build_infrastructure(self, ssh_key_name):
        return Tf(
            region=self.aws_region,
            ssh_key_name=ssh_key_name
        ).build()

    def cluster(self, id):
        return Cluster(client=self.cloudhsmv2, id=id)

    def instance(self, id, ssh_key_file):
        return Instance(client=self.ec2, id=id, ssh_key_file=ssh_key_file)

    def config_file(self, **kwargs):
        config = Config(path=self.path)
        if os.path.exists(os.path.join(self.path, 'piggy_config.json')):
            config.update(**kwargs)
        else:
            config.create(**kwargs)

    def hsm(self, cluster, cloudhsmv2):
        hsm = HSM.create(
            cluster_id=cluster.id,
            availability_zone=cluster.azs[0],
            client=cloudhsmv2
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

    def certs(self, cluster, instance):
        return Certs(
            pem_csr=cluster.csr,
            cluster_id=cluster.id,
            passphrase=self.customer_ca_key_password,
            file_path=self.path
        )

    def initialize_cluster(self, cluster, certs):
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

    def activate_cluster(self, cluster, instance):
        cluster.activate(
            instance=instance,
            crypto_officer_password=self.crypto_officer_password,
            crypto_user_username=self.crypto_user_username,
            crypto_user_password=self.crypto_user_password
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


def _check_packages(packages=[]):
    for package in packages:
        proc = os.system(f'{package} --version')
        if proc != 0:
            raise PackageNotInstalledError(f'{package} is not installed')
    return

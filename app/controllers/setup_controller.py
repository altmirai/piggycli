from app.models.ssh_key_model import SSHKey
from app.models.instance_model import Instance
from app.models.cluster_model import Cluster
from app.models.hsm_model import HSM
from app.models.certificate_model import Certs
import app.utilities.ssh as ssh
from app.utilities.terraform import Tf
import os
import time


class Setup:
    def __init__(self, ec2, cloudhsmv2, resource, path, aws_region, aws_access_key_id, aws_secret_access_key,
                 customer_ca_key_password, crypto_officer_password, crypto_user_username, crypto_user_password):
        _check_packages(packages=['aws', 'terraform'])

        self.ec2 = ec2
        self.cloudhsmv2 = cloudhsmv2
        self.resource = resource
        self.path = path
        self.aws_region = aws_region
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.customer_ca_key_password = customer_ca_key_password
        self.crypto_officer_password = crypto_officer_password
        self.crypto_user_username = crypto_user_username
        self.crypto_user_password = crypto_user_password

    def run(self):
        ssh_key = _get_ssh_key(client=self.ec2)

        resp = _build_infrastructure(
            ssh_key_name=ssh_key.name,
            region=self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

        cluster = _cluster(id=resp['cluster_id'], client=self.cloudhsmv2)

        self.path = _set_path(path=self.path, cluster=cluster)

        ssh_key_file = _write_ssh_key_to_file(
            ssh_key=ssh_key, cluster_id=cluster.id, path=self.path)

        instance = _instance(
            resource=self.resource, id=resp['instance_id'], ssh_key=ssh_key)

        hsm = _hsm(cluster=cluster, client=self.cloudhsmv2)

        certs = _certs(
            cluster=cluster, customer_ca_key_password=self.customer_ca_key_password)

        _write_certs_to_file(certs=certs, path=self.path, cluster=cluster)

        customer_ca_cert_path = os.path.join(self.path, 'customerCA.crt')
        _upload_customer_ca_cert(
            instance=instance,
            file_path=customer_ca_cert_path,
            ssh_key=ssh_key
        )

        _initialize_cluster(cluster=cluster, certs=certs)

        _activate_cluster(
            cluster=cluster,
            instance=instance,
            ssh_key=ssh_key,
            crypto_officer_password=self.crypto_officer_password,
            crypto_user_username=self.crypto_user_username,
            crypto_user_password=self.crypto_user_password
        )

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
    return True


def _get_ssh_key(client):
    return SSHKey.create(client=client)


def _build_infrastructure(region, ssh_key_name, aws_access_key_id, aws_secret_access_key):
    return Tf(
        region=region,
        ssh_key_name=ssh_key_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    ).build()


def _cluster(client, id):
    return Cluster(client=client, id=id)


def _set_path(path, cluster):
    path = os.path.join(path, cluster.id)
    if os.path.isdir(path) is False:
        os.mkdir(path)
    return path


def _write_ssh_key_to_file(ssh_key, cluster_id, path):
    ssh_key_file = ssh_key.write_to_file(cluster_id=cluster_id, path=path)
    return ssh_key_file
    # ssh_key_file = os.path.join(path, f'{ssh_key.name}.pem')
    # try:
    #     with open(ssh_key_file, 'w') as file:
    #         file.write(ssh_key.material)
    #     assert os.path.exists(ssh_key_file)
    #     return ssh_key_file
    # except Exception as error:
    #     raise WriteFileError(error.args[0])


def _instance(resource, id, ssh_key):
    instance = Instance(resource=resource, id=id)
    instance.install_packages(ssh_key_file=ssh_key.ssh_key_file)
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
    return hsm


def _certs(customer_ca_key_password, cluster):
    certs = Certs(
        pem_csr=cluster.csr,
        passphrase=customer_ca_key_password
    )

    return certs


def _write_certs_to_file(certs, path, cluster):
    # Customer CA Key
    with open(os.path.join(path, 'customerCA.key'), 'wb') as file:
        file.write(certs.pem_private_key)

    # Customer CA Certificate
    with open(os.path.join(path, 'customerCA.crt'), 'wb') as file:
        file.write(certs.pem_ca_cert)

    # Cluster CSR
    csr = certs.pem_csr if type(
        certs.pem_csr) is bytes else certs.pem_csr.encode('utf-8')
    with open(os.path.join(path, f'{cluster.id}_ClusterCSR.csr'), 'wb') as file:
        file.write(csr)

    # Customer HSM Certificate
    with open(os.path.join(path, f'{cluster.id}_CustomerHSMCertificate.crt'), 'wb') as file:
        file.write(certs.pem_hsm_cert)


def _upload_customer_ca_cert(file_path, instance, ssh_key):
    if os.path.exists(file_path):
        ssh.upload_file_to_instance(
            ip_address=instance.public_ip_address,
            ssh_key_file=ssh_key.ssh_key_file,
            file_path=file_path
        )
    return True


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


def _activate_cluster(cluster, instance, crypto_officer_password, crypto_user_username, crypto_user_password, ssh_key):
    cluster.activate(
        instance=instance,
        crypto_officer_password=crypto_officer_password,
        crypto_user_username=crypto_user_username,
        crypto_user_password=crypto_user_password,
        ssh_key=ssh_key
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


class WriteFileError(Exception):
    pass

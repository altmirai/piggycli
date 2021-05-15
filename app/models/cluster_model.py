import app.utilities.ssh as ssh


class Cluster:

    def __init__(self, **kwargs):
        self.client = kwargs['client']
        self.id = kwargs['id']

    @classmethod
    def create(cls, **kwargs):
        return False

    @classmethod
    def all(cls, **kwargs):
        client = kwargs['client']
        resp = client.describe_clusters()
        return resp['Clusters']

    @property
    def hsms(self):
        return self.read()['Hsms']

    @property
    def azs(self):
        subnet_mapping = self.read()['SubnetMapping']
        azs = []
        for key, value in subnet_mapping.items():
            azs.append(key)
        return azs

    @property
    def csr(self):
        return self.read()['Certificates']['ClusterCsr']

    @property
    def state(self):
        return self.read()['State']

    def initialize(self, certs):
        assert self.state == 'UNINITIALIZED', 'Cluster state is not UNITIALIZED'
        assert certs.valid, 'Certificates not valid'
        self.client.initialize_cluster(
            ClusterId=self.id,
            SignedCert=certs.pem_hsm_cert.decode('UTF-8'),
            TrustAnchor=certs.pem_ca_cert.decode('UTF-8')
        )
        return

    def configure_cloudhsm_client(self, ec2_instance):
        ssh.configure_cloudhsm_client(
            ip_address=ec2_instance.public_ip_address,
            ssh_key_file=ec2_instance.ssh_key_file,
            hsm_ip_address=self.hsms[0]['EniIp']
        )
        return

    def activate(self, ec2_instance, co_password):
        ssh.activate_cluser(
            ip_address=ec2_instance.public_ip_address,
            ssh_key_file=ec2_instance.ssh_key_file,
            co_password=co_password
        )
        return

    def create_crypto_user(self, ec2_instance, crypto_officer, crypto_user):
        ssh.create_crypto_user(
            ip_address=ec2_instance.public_ip_address,
            ssh_key_file=ec2_instance.ssh_key_file,
            crypto_officer=crypto_officer,
            crypto_user=crypto_user
        )
        return

    def read(self):
        resp = self.client.describe_clusters(
            Filters={'clusterIds': [self.id]})
        return resp['Clusters'][0]

    def destroy(self):
        return False

import app.utilities.ssh as ssh


class Cluster:

    def __init__(self, client, id):
        self.client = client
        self.id = id

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

    def activate(self, instance, crypto_officer_password, crypto_user_username, crypto_user_password):
        eni_ip = self.hsms[0]['EniIp']
        ssh.activate_cluster(
            ip_address=instance.public_ip_address,
            ssh_key_file=instance.ssh_key_file,
            eni_ip=eni_ip,
            crypto_officer_password=crypto_officer_password,
            crypto_user_username=crypto_user_username,
            crypto_user_password=crypto_user_password
        )
        return

    def read(self):
        resp = self.client.describe_clusters(
            Filters={'clusterIds': [self.id]})
        return resp['Clusters'][0]

    def destroy(self):
        return False

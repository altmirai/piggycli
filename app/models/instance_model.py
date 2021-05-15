import app.utilities.ssh as ssh
import boto3


class Instance:

    def __init__(self, client, id, ssh_key_file):
        self.client = client
        self.id = id
        self.ssh_key_file = ssh_key_file

    @classmethod
    def all(cls, **kwargs):
        client = kwargs['client']
        resp = client.describe_instances()
        return resp['Reservations']

    @property
    def public_ip_address(self):
        instance = self.read()
        return instance.public_ip_address

    def install_packages(self):
        outputs = ssh.install_packages(ip_address=self.public_ip_address,
                                       ssh_key_file=self.ssh_key_file)

        return True

    def create(self):
        return False

    def read(self):
        resouce = boto3.resource('ec2')
        instance = resouce.Instance(self.id)
        return instance

    def update(self):

        return

    def destroy(self):
        return False

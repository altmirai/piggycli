from app.models.pub_key_model import PubKey
from app.models.instance_model import Instance
from app.models.cluster_model import Cluster
from app.models.address_model import Address

import uuid
import os


class AddressController:

    def __init__(self, credentials):
        self.id = f'addr-{str(uuid.uuid4())[-12:]}'
        self.credentials = credentials

    def all(self):
        return

    def create(self, ip_address, ssh_key_file, eni_ip, s3):
        pub_key = PubKey.create(
            ip_address=ip_address,
            ssh_key_file=ssh_key_file,
            eni_ip=eni_ip,
            crypto_user_username=self.credentials.data['crypto_user_username'],
            crypto_user_password=self.credentials.data['crypto_user_password'],
            label=self.id
        )

        address = Address.create(pub_key=pub_key)

        bucket = f"{self.credentials.data['cluster_id']}-bucket"

        assert address.save(
            bucket=bucket,
            s3=s3,
            region=self.credentials.data['aws_region']
        ), f"Failed to save address: {self.id} to bucket: {bucket}"

        return address

    def show(self):
        return

    def update(self):
        return

    def destroy(self):
        return


class SSHKeyFileNotFoundError(Exception):
    pass

from app.models.pub_key_model import PubKey
from app.models.instance_model import Instance
from app.models.cluster_model import Cluster
from unittest.mock import patch
import tests.data as data
import boto3


@patch('app.models.pub_key_model.ssh.gen_ecc_key_pair', return_value=data.gen_ecc_key_pair_resp, autospec=True)
def test_create(mock_gen_ecc_key_pair):
    pub_key = PubKey.create(
        ip_address=data.public_ip_address,
        ssh_key_file=data.ssh_key_file,
        eni_ip=data.eni_ip,
        crypto_user_username=data.crypto_user_username,
        crypto_user_password=data.crypto_user_password,
        label=data.label
    )

    assert pub_key.handle == data.handle


def test_download_pem_file():
    instance = Instance(resource=boto3.resource('ec2'),
                        id='i-02d10eade3ffe9de9')
    pub_key = PubKey(
        label=data.label,
        handle=data.handle,
        private_key_handle=data.private_key_handle,
        public_key_pem_file_name=data.public_key_pem_file_name
    )
    pub_key.download_pem_file(
        ip_address=instance.public_ip_address,
        ssh_key_file='/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/production_files/cluster-2f2ynawbwz5/Piggy_SSH_Key_bdd3f8d5.pem',
        local_path=data.production_path
    )
    breakpoint()

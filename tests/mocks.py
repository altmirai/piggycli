import tests.data as data
from unittest.mock import patch, Mock
import os

tf = Mock()
tf.build.return_value = {
    'cluster_id': data.cluster_id,
    'vpc_id': data.vpc_id,
    'instance_id': data.instance_id
}


ssh_key = Mock()
ssh_key.fingerprint = data.KeyFingerprint
ssh_key.id = data.KeyPairId
ssh_key.material = data.KeyMaterial
ssh_key.name = data.KeyName
ssh_key.ssh_key_file = os.path.join(
    data.test_path, data.cluster_id, f'{data.KeyName}.pem')
ssh_key.wrtie_to_file.return_value = True

cluster = Mock()
cluster.id = data.cluster_id
cluster.azs = data.azs
cluster.csr = data.pem_csr
cluster.initialize.return_value = True
cluster.activate.return_value = True

instance = Mock()
instance.id = data.instance_id
instance.public_ip_address = data.public_ip_address

hsm = Mock()
hsm.id = data.hsm_id
hsm.cluster_id = data.cluster_id

certs = Mock()
certs.pem_private_key = data.pem_private_key
certs.pem_csr = data.pem_csr
certs.pem_hsm_cert = data.pem_hsm_cert
certs.pem_ca_cert = data.pem_ca_cert

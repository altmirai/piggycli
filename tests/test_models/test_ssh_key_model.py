from app.models.ssh_key_model import SSHKey
import tests.data as data
import os


def test_write_to_file(ssh_key):
    ssh_key_file_path = ssh_key.write_to_file(
        cluster_path=data.test_cluster_path)

    assert os.path.exists(ssh_key_file_path)

    with open(ssh_key_file_path, 'r') as file:
        ssh_key_material = file.read()

    assert ssh_key_material == data.KeyMaterial

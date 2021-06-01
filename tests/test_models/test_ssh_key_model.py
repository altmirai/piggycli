from app.models.ssh_key_model import SSHKey
import tests.data as data
import os


def test_write_to_file(ssh_key):
    ssh_key_file = ssh_key.write_to_file(
        cluster_id=data.cluster_id, path=data.test_path)

    assert os.path.exists(ssh_key_file)

    with open(ssh_key_file, 'r') as file:
        ssh_key_material = file.read()

    assert ssh_key_material == data.KeyMaterial

# def test_client(ssh_key_ec2_test_create):
#     ssh_key = SSHKey.create(client=ssh_key_ec2_test_create)
#     assert ssh_key.name == 'Piggy_SSH_Key_0194afd1'


# def test_client_all(ssh_key_ec2_test_all):
#     ssh_keys = SSHKey.all(client=ssh_key_ec2_test_all)
#     assert ssh_keys[0]['KeyName'] == 'Piggy_SSH_Key_0194afd1'
#     assert ssh_keys[1]['KeyName'] == 'Piggy_SSH_Key_40cc19f5'

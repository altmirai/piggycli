from app.models.ssh_key_model import SSHKey
import botocore.session
from botocore.stub import Stubber, ANY
import os


create_key_pair_resp = {'KeyFingerprint': '08:c9:28:e5:24:38:d5:ef:9b:a1:76:22:9f:00:0c:eb:47:16:59:cd', 'KeyMaterial': '-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAkOrCB3e0Fj/Cv797THZn5YgxIPywNdlg284rMSshrLl8QC83\n0ck0K9CP3Y+rCuHGx7t/2tCtl66uKlwOPFvWGDi+akonkUeVqnV8U1z5jNhI8SwY\niXtcFX0twIGHaaxYQrWZvOUAnmE8JUGd7Pysy4Sy7/ZEldXwEN3fN2NIPRnQwii7\nS5tv573C2am2MMXtwEKtQi3uWgPu//maXqoM0/PuxTDk9DUKnN88nvNBMoTlHr1P\nl9QsHMPyXvJ/+TTPdVybXwMvv1KgCMeGid43CPu7SFa8trx9DuvSY03TwYyhZIp6\nMsPZot6pu+opRXgF7SkSpp/+ABPoA836sPF0+wIDAQABAoIBAAESi68Mdru3axSK\nMTpmoewz7tEkrZUob6wQwYcSn6QslzvOXaZiy80LNRVZq9VfyF3QCGkxJCe8NjPA\nDKbrsxDo0pfsxpAvrG7fgbUIOhyNuTR3tBLIY+0QyRbknoDsspaDy4h3VWLWq2BH\nNQj88bZr2/skomtNcwJc8frx9CXnmR1erB8d7UybKFiYL4ggM/MVQbdn66ZpmKCK\naZ774lbgdiwp8YZp1ANFw7zBr1MTqXKLmghtYZoornRUVk2c3OPUII62jmarUaqn\nKL+q2198j0axDsmFCAALTbmxjo//XWxwTeaRNwsi0hqeENEy1ywtidn1A8eHJaOi\nvGlV6LkCgYEA4rabAGB7OQTunGj6BiQBN8AnG/1B77HBA/VRy3YUHdPaBYtldLuX\nZrQKuE3l13uX0whXr+BQVDtDiegocz4r41/MR9uUoQFHnsL25D+A44xveT2scTHm\nBHpUprq8ti4XyNJGpnZXSxQCRzhcGnJItvfOaQWW+slEnR4RUuWCdjUCgYEAo6Mn\nmT+NyNCfJHWvF951fvRi7liktRzIcIL7Hu4gDkTTJ7U/Ms3OgQTsQ6VIfNeotAYC\nFe/GVb+SB91MnnCFwPbwt1vIwdLGvKtAUq3OQvE8Jv1LCC3XQJcRv/tJuP6lLz1t\nWNF59Uz0Ar6VN9tIctdribKGP6Dxg32OLlrV5G8CgYEAotnQlYC4gsjMLYYqsuaC\nCW35qd1N08O3hgRd8OysnpBi98Cd7DAkHR4O5TzvcM3SzUAc3LUgfqDjbthY1g8+\nr2FM+AD+zniA3cXmWyZSiyGBoXFvwQ+6zlShIfLZQ3PwmcyR+1jec4u35zjQ0B5v\npR50InRlc1fH9aR3hThfclECgYEAh+bv80GqIpbJJQGsKnmyQX78TxFFsbk26uKN\nZxHDg7Y7XCYWV74/fD23bzLtMen2DZVT1B4wLXUN9gQgJxIys6EjKFVNNVQ1g+oC\nYOhCfqxVFdiVoTRZKiaNMlGj18V9MO+mSfangEep/EGGMj6nO+GXSWQARQYIrvju\nxabhL3cCgYEAlPAbQgqljbfs6pIG5eEKHNLXaCZxFeZDQ+PQ9CYBsCL0nPo0e1iw\nHNFx2A/BN0hEZxiOO0LnDV5paFhAd+rFhSvxdgwhOBvxU1TDwcNCoyqpbJ57BB3e\n5d+ShkCu0K3LbKn65ZAtvJCB9yleu5VUIt6i+q/aaPLcWTcf+YxVDfM=\n-----END RSA PRIVATE KEY-----',
                        'KeyName': 'Piggy_SSH_Key_0194afd1', 'KeyPairId': 'key-0a070814c64fa0e65', 'ResponseMetadata': {'RequestId': '56d9520a-80e8-4603-9a92-6a78c3ef42ca', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '56d9520a-80e8-4603-9a92-6a78c3ef42ca', 'cache-control': 'no-cache, no-store', 'strict-transport-security': 'max-age=31536000; includeSubDomains', 'content-type': 'text/xml;charset=UTF-8', 'content-length': '2103', 'vary': 'accept-encoding', 'date': 'Sat, 22 May 2021 00:23:15 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}


def test_create():
    client = botocore.session.get_session().create_client('ec2')
    with Stubber(client) as stubber:
        stubber.add_response(
            'create_key_pair', create_key_pair_resp, {'KeyName': ANY})
        key = SSHKey.create(client=client)

        assert key.name == create_key_pair_resp['KeyName']
        assert key.id == create_key_pair_resp['KeyPairId']
        assert key.material == create_key_pair_resp['KeyMaterial']
        assert key.fingerprint == create_key_pair_resp['KeyFingerprint']


describe_key_pairs_resp = {'KeyPairs': [{'KeyPairId': 'key-0a070814c64fa0e65', 'KeyFingerprint': '08:c9:28:e5:24:38:d5:ef:9b:a1:76:22:9f:00:0c:eb:47:16:59:cd', 'KeyName': 'Piggy_SSH_Key_0194afd1', 'Tags': []}, {'KeyPairId': 'key-071d152e1ec5428df', 'KeyFingerprint': 'de:7b:e3:aa:81:52:89:be:a5:01:a0:87:8d:67:76:47:e8:a5:9f:0c', 'KeyName': 'Piggy_SSH_Key_40cc19f5', 'Tags': []}], 'ResponseMetadata': {
    'RequestId': 'd75d4307-370d-4d3c-8218-773d9d924c49', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'd75d4307-370d-4d3c-8218-773d9d924c49', 'cache-control': 'no-cache, no-store', 'strict-transport-security': 'max-age=31536000; includeSubDomains', 'content-type': 'text/xml;charset=UTF-8', 'content-length': '772', 'date': 'Sat, 22 May 2021 00:32:55 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}


def test_all():
    client = botocore.session.get_session().create_client('ec2')
    with Stubber(client) as stubber:
        stubber.add_response('describe_key_pairs', describe_key_pairs_resp, {})
        key_pairs = SSHKey.all(client=client)

    assert key_pairs == [{'KeyPairId': 'key-0a070814c64fa0e65', 'KeyName': 'Piggy_SSH_Key_0194afd1'},
                         {'KeyPairId': 'key-071d152e1ec5428df', 'KeyName': 'Piggy_SSH_Key_40cc19f5'}]


def test_write_to_file():
    client = botocore.session.get_session().create_client('ec2')
    test_path = os.getcwd()

    with Stubber(client) as stubber:
        stubber.add_response(
            'create_key_pair', create_key_pair_resp, {'KeyName': ANY})
        key = SSHKey.create(client=client)
        key.write_to_file(path=test_path)

        pem_file_path = os.path.join(test_path, f'{key.name}.pem')

        assert os.path.exists(pem_file_path)
        with open(pem_file_path, 'r') as file:
            pem_file = file.read()
        assert pem_file == key.material

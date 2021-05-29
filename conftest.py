from app.models.credentials_model import Credentials, read_env_vars, set_env_var
from app.models.ssh_key_model import SSHKey
import botocore.session
from botocore.stub import Stubber, ANY

import pytest
import os


class CredentialsData:
    def __init__(self):
        self.test_path = '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/tests/test_files'
        self.production_path = '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/production_files'
        self.aws_region = 'us-east-2'
        self.ssh_key_name = 'Piggy_SSH_Key_cf865bae'
        self.cluster_id = 'cluster-lbtkdldygfh'
        self.instance_id = 'i-051bdb2ae099024a5'
        self.aws_access_key_id = 'AKIA5YNNN4JH6JDQF5XH'
        self.aws_secret_access_key = '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'
        self.customer_ca_key_password = 'password1'
        self.crypto_officer_password = 'password1'
        self.crypto_user_username = 'cryptouser'
        self.crypto_user_password = 'password1'
        self.KeyFingerprint = '08:c9:28:e5:24:38:d5:ef:9b:a1:76:22:9f:00:0c:eb:47:16:59:cd'
        self.KeyMaterial = '-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAkOrCB3e0Fj/Cv797THZn5YgxIPywNdlg284rMSshrLl8QC83\n0ck0K9CP3Y+rCuHGx7t/2tCtl66uKlwOPFvWGDi+akonkUeVqnV8U1z5jNhI8SwY\niXtcFX0twIGHaaxYQrWZvOUAnmE8JUGd7Pysy4Sy7/ZEldXwEN3fN2NIPRnQwii7\nS5tv573C2am2MMXtwEKtQi3uWgPu//maXqoM0/PuxTDk9DUKnN88nvNBMoTlHr1P\nl9QsHMPyXvJ/+TTPdVybXwMvv1KgCMeGid43CPu7SFa8trx9DuvSY03TwYyhZIp6\nMsPZot6pu+opRXgF7SkSpp/+ABPoA836sPF0+wIDAQABAoIBAAESi68Mdru3axSK\nMTpmoewz7tEkrZUob6wQwYcSn6QslzvOXaZiy80LNRVZq9VfyF3QCGkxJCe8NjPA\nDKbrsxDo0pfsxpAvrG7fgbUIOhyNuTR3tBLIY+0QyRbknoDsspaDy4h3VWLWq2BH\nNQj88bZr2/skomtNcwJc8frx9CXnmR1erB8d7UybKFiYL4ggM/MVQbdn66ZpmKCK\naZ774lbgdiwp8YZp1ANFw7zBr1MTqXKLmghtYZoornRUVk2c3OPUII62jmarUaqn\nKL+q2198j0axDsmFCAALTbmxjo//XWxwTeaRNwsi0hqeENEy1ywtidn1A8eHJaOi\nvGlV6LkCgYEA4rabAGB7OQTunGj6BiQBN8AnG/1B77HBA/VRy3YUHdPaBYtldLuX\nZrQKuE3l13uX0whXr+BQVDtDiegocz4r41/MR9uUoQFHnsL25D+A44xveT2scTHm\nBHpUprq8ti4XyNJGpnZXSxQCRzhcGnJItvfOaQWW+slEnR4RUuWCdjUCgYEAo6Mn\nmT+NyNCfJHWvF951fvRi7liktRzIcIL7Hu4gDkTTJ7U/Ms3OgQTsQ6VIfNeotAYC\nFe/GVb+SB91MnnCFwPbwt1vIwdLGvKtAUq3OQvE8Jv1LCC3XQJcRv/tJuP6lLz1t\nWNF59Uz0Ar6VN9tIctdribKGP6Dxg32OLlrV5G8CgYEAotnQlYC4gsjMLYYqsuaC\nCW35qd1N08O3hgRd8OysnpBi98Cd7DAkHR4O5TzvcM3SzUAc3LUgfqDjbthY1g8+\nr2FM+AD+zniA3cXmWyZSiyGBoXFvwQ+6zlShIfLZQ3PwmcyR+1jec4u35zjQ0B5v\npR50InRlc1fH9aR3hThfclECgYEAh+bv80GqIpbJJQGsKnmyQX78TxFFsbk26uKN\nZxHDg7Y7XCYWV74/fD23bzLtMen2DZVT1B4wLXUN9gQgJxIys6EjKFVNNVQ1g+oC\nYOhCfqxVFdiVoTRZKiaNMlGj18V9MO+mSfangEep/EGGMj6nO+GXSWQARQYIrvju\nxabhL3cCgYEAlPAbQgqljbfs6pIG5eEKHNLXaCZxFeZDQ+PQ9CYBsCL0nPo0e1iw\nHNFx2A/BN0hEZxiOO0LnDV5paFhAd+rFhSvxdgwhOBvxU1TDwcNCoyqpbJ57BB3e\n5d+ShkCu0K3LbKn65ZAtvJCB9yleu5VUIt6i+q/aaPLcWTcf+YxVDfM=\n-----END RSA PRIVATE KEY-----'
        self.KeyName = 'Piggy_SSH_Key_0194afd1'
        self.KeyPairId = 'key-0a070814c64fa0e65'

    @property
    def credentials_kwargs(self):
        return {
            'aws_region': self.aws_region,
            'ssh_key_name': self.ssh_key_name,
            'cluster_id': self.cluster_id,
            'instance_id': self.instance_id,
            'aws_access_key_id': self.aws_access_key_id,
            'aws_secret_access_key': self.aws_secret_access_key,
            'customer_ca_key_password': self.customer_ca_key_password,
            'crypto_officer_password': self.crypto_officer_password,
            'crypto_user_username': self.crypto_user_username,
            'crypto_user_password': self.crypto_user_password,
        }

    @property
    def ssh_key_create_resp(self):
        return {
            'KeyFingerprint': self.KeyFingerprint,
            'KeyMaterial': self.KeyMaterial,
            'KeyName': self.KeyName,
            'KeyPairId': self.KeyPairId
        }


t = CredentialsData()


def pytest_sessionstart(session):
    os.mkdir(t.test_path)
    set_env_var(var='PATH', value=t.test_path)


@pytest.fixture
def credentials():
    credentials = Credentials.create(path=t.test_path, **t.credentials_kwargs)
    yield credentials
    os.remove(os.path.join(t.test_path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(t.test_path, '.piggy'))


@pytest.fixture
def ssh_key_ec2_test_create():
    client = botocore.session.get_session().create_client('ec2')
    with Stubber(client) as stubber:
        stubber.add_response(
            'create_key_pair',
            t.ssh_key_create_resp,
            {'KeyName': ANY}
        )
        yield client


@pytest.fixture
def ssh_key_ec2_test_all():
    client = botocore.session.get_session().create_client('ec2')
    with Stubber(client) as stubber:
        stubber.add_response(
            'describe_key_pairs',
            {
                'KeyPairs': [
                    {
                        'KeyPairId': 'key-0a070814c64fa0e65',
                        'KeyFingerprint': '08:c9:28:e5:24:38:d5:ef:9b:a1:76:22:9f:00:0c:eb:47:16:59:cd',
                        'KeyName': 'Piggy_SSH_Key_0194afd1',
                        'Tags': []
                    },
                    {
                        'KeyPairId': 'key-071d152e1ec5428df',
                        'KeyFingerprint': 'de:7b:e3:aa:81:52:89:be:a5:01:a0:87:8d:67:76:47:e8:a5:9f:0c',
                        'KeyName': 'Piggy_SSH_Key_40cc19f5',
                        'Tags': []
                    }
                ]},
            {}
        )
        yield client


@pytest.fixture
def test_data():
    return CredentialsData()


def pytest_sessionfinish(session, exitstatus):
    os.rmdir(t.test_path)
    set_env_var(var='PATH', value=t.production_path)

from app.models.certificate_model import Certs
from app.models.credentials_model import Credentials, read_env_vars, set_env_var
from app.models.ssh_key_model import SSHKey

import botocore.session
from botocore.stub import Stubber, ANY

from unittest.mock import patch, Mock
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
        self.KeyFingerprint2 = 'de:7b:e3:aa:81:52:89:be:a5:01:a0:87:8d:67:76:47:e8:a5:9f:0c'
        self.KeyName2 = 'Piggy_SSH_Key_40cc19f5'
        self.KeyPairId2 = 'key-071d152e1ec5428df'

        self.pem_csr = '-----BEGIN CERTIFICATE REQUEST-----\nMIIC0TCCAbkCAQAwgYsxRDAJBgNVBAYTAlVTMAkGA1UECAwCQ0EwDQYDVQQKDAZD\nYXZpdW0wDQYDVQQLDAZOM0ZJUFMwDgYDVQQHDAdTYW5Kb3NlMUMwQQYDVQQDDDpI\nU006QjRGMUU4QjY3OTY3NTg2M0Y4REIzMjExMTM2NEIzOlBBUlROOjEzLCBmb3Ig\nRklQUyBtb2RlMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvDY9IZlR\nThUQ2Jfc+JWPC15WqZbMRKiEba+FICcwno+izaDza+rzpqtaU0Q5UVYGOe4vEtVj\nxsj3hdhXc2rK53vhw4EdmKojPzAy3F/TJGzSvzIlPUCdWLtbKlNEkg/VGu1YcsMV\nvQvyGFSusj8idWT4DvsZxPuEwiXE4qEPmyB1uo2lKIYWfulP9QrRdvnrBF/zBmXO\nblg3zHf1KQ8bYWW8Lc/DGcRnRvPBfDvYNS6DJPrMiM+QeqhM5Iegu7OlTOTkV72d\nmaMqTuuWOGrb6LCDr7hWGfjAE3517Jt2ia2bB8YE5Wda4mUBEmpVl5Kho547S6Sx\nMiChX3U3VCHbVwIDAQABoAAwDQYJKoZIhvcNAQELBQADggEBAKqEhDqVClGRES2C\nIwqKxPVYo5lbynEZ94qSeKzI9rgoW3kPVyro1vBxAzMwDSJd1TXmw2fJAOY7Zdiw\n+j0SMZCb81ehVNa8VRUsOrU6phC72jqUSFSWpRkCDxc9inIdUfBpqIQxsd0JpYB7\nzvyuKILMNDI3Ys7S4i1ErHv8IyDUdmVjP+qRaEAhecBEt5GVZPDg/vjEsS83hqf4\n7EZ9S9noDgnoa79W1ovFr8wW8EZ5Spi50D5hsFCMy4a4rErwneAATEm2MmtLfIy7\nCWTUET6SZN2Ncn/oM1ulVYofYTctmpiAGMMjB9joA6nW0I2QfhaSOTugU+NmwnC0\nOo+qHwM=\n-----END CERTIFICATE REQUEST-----\n'
        self.passphrase = 'password1'
        self.pem_private_key = b'-----BEGIN RSA PRIVATE KEY-----\nProc-Type: 4,ENCRYPTED\nDEK-Info: AES-256-CBC,6F7135B1FF40772431A52344F2C28F3E\n\n17swNOMYJtX7XSMnL9C6MPmIaI34peR4CPUt0IWaiu5AfuHeGrho2PhaljlKX/Lt\nw4ykD/zrrKk88BrhTTPhArJNOporxC8d2BeyXtiIXqz4+yn256Ox4zfzkAdGq2xq\nRRzNHZot417yqUcIUSI+H39WkHVunhpNWJixMFKp5yhTf1JUHXCNOPNr4M/aALFD\n9U1pJ4t1H0umrNdHKI7lWat5+lnfXPe9GrQ+NYYobM6MX6uM7Mb9ggzN0234rOQM\nhLYdMGUCvXrWUoVHQ7mRR/DBa4S2ptAbyHsQZCOLLvnfQE+lCpT8SxkUf3xyeRGC\njGqHWANEHbdW7LKNS9aSbjoM5fXx9ToJJJiFAo4RuFVpTufVh8zhPscx1DjvVXLQ\nPo1WZrZusELmhzvJOgJQkNvrVnfGmHtB6CuzHUyXAriN1VUekWlNYi3gP5fC5MjO\n+bISUXiGLHi0DYe+x+0PHquI/u5Gugeh/k+q7pvbTnZ/r9so+P4aW2q1IDloFYXv\nDVO3VGdSef3mp1k4B49257K5Vri1XYjLXAkbQyuVFGWphQ4bSHCscZhAevpzCDVk\nPrD0R+egohy/ErZllbp7+rc+VpHMBXpi5LEYAetpdR5URrgZAP5L2WWS4/WtsoAb\nnApoqMuq53QaOjjWx2wTtyU1lOGoT5pSS4/c1UKxV/72Dpbu96e8MBhjwwmIZiGW\nD5fjHJzEDZxtA/YFS1UHxb8hPsMRJkb67dR1fOSDXBWLZdi0MQ1que60bXV4+a8W\nJTKzpf8yOaNkI98QqGcvbfZWcgQ/sMVduOrx1VsndFqXiJ4M5heCAU+3gKAaX9HG\nkoYtTnp+LbshZNawdyW1MtdeeP8zrVfAx+WrYcI8/XL7+tge4n6VkVoqxD6IJX3a\nZ6EPY/J/IBSQsYIeQe4QDrjR1ztbNBS4KMBlJofM3IlPY5ee9L61QBwCW9zM9FNI\n8s54O2D3nGgc5fGteB5Ze4qGDFshPKXJU5uFcSZ19202NhuPTeWkuCFXMSz41eRL\n3kog6OW5q3UNPgMAb9nmuQzDt7fALY9fzl3n6CV/lli68oP8ji8iqqTvP5tjkgQa\nVC5IY97qs0JoeEnORSMo0SdnL/4YK5eni5pZxR1pvdXV0t4Vqap0f2SEi0yL8HxA\nLtmCTYdD9e/IEFcPjoFp/M5NcPUP81S8gJUwLWo9eI2Cpe7tZBrdWHQ6Z8Kc3mQQ\nflT5wXps/H9CmVkDFIu/VuOLxHxVzl7L20a8zkZDRhqnij/IqG+UM27dZ/Rc48Vu\nG7S4um6eahANe7r2n4gDApQBlziUApR5PIeZUFpKELTNKJ4BY1Ttsmt+y3EDU8Uk\nBt38zSYs251WmKjuRwR99dny7p+jjxBdJSW5xpoSv7/DdH9UaF2PhAXetdeYRWnt\nu2lshQzrZBruQpcSCbFS3FvmlNlKc4zoSt9lNp+NgGLZzbLciSQhF5+nyz2k+K26\nZyTbjiaWhK+AfxtgWG84iuJI7DtcuP1MRuud0aV9PZV/KZ8X1AnqDsxCUsUwjtAj\nM5PTCWRL0tSkQKRue8iueN498DdzlK+QqkRGdN3j/YTmh8KZzLvjiUxAUPXByjaV\n-----END RSA PRIVATE KEY-----\n'

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

    @property
    def ssh_key_describe_resp(self):
        return {
            'KeyPairs': [
                {
                    'KeyPairId':  self.KeyPairId,
                    'KeyFingerprint':  self.KeyFingerprint,
                    'KeyName': self.KeyName,
                    'Tags': []
                },
                {
                    'KeyPairId': self.KeyPairId2,
                    'KeyFingerprint': self.KeyFingerprint2,
                    'KeyName': self.KeyName2,
                    'Tags': []
                }
            ]}

    @property
    def ssh_key_kwargs(self):
        return {
            'id': self.KeyPairId,
            'name': self.KeyName,
            'material': self.KeyMaterial,
            'fingerprint': self.KeyFingerprint
        }

    @property
    def certs_kwargs(self):
        return {
            'pem_csr':  self.pem_csr,
            'passphrase': self.passphrase
        }


t = CredentialsData()


def pytest_sessionstart(session):
    if os.path.isdir(t.test_path):
        files = os.listdir(t.test_path)
        for file in files:
            os.remove(os.path.join(t.test_path, file))
    else:
        os.mkdir(t.test_path)
    set_env_var(var='PATH', value=t.test_path)


@ pytest.fixture
def credentials():
    credentials = Credentials.create(path=t.test_path, **t.credentials_kwargs)
    yield credentials
    os.remove(os.path.join(t.test_path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(t.test_path, '.piggy'))


@ pytest.fixture
def ssh_key_ec2_test_create():
    client = botocore.session.get_session().create_client('ec2')
    with Stubber(client) as stubber:
        stubber.add_response(
            'create_key_pair',
            t.ssh_key_create_resp,
            {'KeyName': ANY}
        )
        yield client


@ pytest.fixture
def ssh_key_ec2_test_all():
    client = botocore.session.get_session().create_client('ec2')
    with Stubber(client) as stubber:
        stubber.add_response(
            'describe_key_pairs',
            t.ssh_key_describe_resp,
            {}
        )
        yield client


@pytest.fixture
def ssh_key():
    ssh_key = SSHKey(**t.ssh_key_kwargs)
    yield ssh_key


@pytest.fixture
# @patch('conftest.certs.pem_private_key', return_value=t.pem_private_key, autospec=True)
def certs():
    certs = Certs(**t.certs_kwargs)
    yield certs


@ pytest.fixture
def test_data():
    return CredentialsData()


def pytest_sessionfinish(session, exitstatus):
    files = os.listdir(t.test_path)
    for file in files:
        os.remove(os.path.join(t.test_path, file))
    os.rmdir(t.test_path)
    set_env_var(var='PATH', value=t.production_path)

import app.controllers.setup_controller as setup
import botocore.session
from botocore.stub import Stubber, ANY
import os
from unittest.mock import patch, Mock
import boto3


@patch('app.controllers.setup_controller.os.system', return_value=0, autospec=True)
def test_check_packages(mock_system):
    assert setup._check_packages(packages=['aws', 'terraform'])


create_key_pair_resp = {'KeyFingerprint': '08:c9:28:e5:24:38:d5:ef:9b:a1:76:22:9f:00:0c:eb:47:16:59:cd', 'KeyMaterial': '-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAkOrCB3e0Fj/Cv797THZn5YgxIPywNdlg284rMSshrLl8QC83\n0ck0K9CP3Y+rCuHGx7t/2tCtl66uKlwOPFvWGDi+akonkUeVqnV8U1z5jNhI8SwY\niXtcFX0twIGHaaxYQrWZvOUAnmE8JUGd7Pysy4Sy7/ZEldXwEN3fN2NIPRnQwii7\nS5tv573C2am2MMXtwEKtQi3uWgPu//maXqoM0/PuxTDk9DUKnN88nvNBMoTlHr1P\nl9QsHMPyXvJ/+TTPdVybXwMvv1KgCMeGid43CPu7SFa8trx9DuvSY03TwYyhZIp6\nMsPZot6pu+opRXgF7SkSpp/+ABPoA836sPF0+wIDAQABAoIBAAESi68Mdru3axSK\nMTpmoewz7tEkrZUob6wQwYcSn6QslzvOXaZiy80LNRVZq9VfyF3QCGkxJCe8NjPA\nDKbrsxDo0pfsxpAvrG7fgbUIOhyNuTR3tBLIY+0QyRbknoDsspaDy4h3VWLWq2BH\nNQj88bZr2/skomtNcwJc8frx9CXnmR1erB8d7UybKFiYL4ggM/MVQbdn66ZpmKCK\naZ774lbgdiwp8YZp1ANFw7zBr1MTqXKLmghtYZoornRUVk2c3OPUII62jmarUaqn\nKL+q2198j0axDsmFCAALTbmxjo//XWxwTeaRNwsi0hqeENEy1ywtidn1A8eHJaOi\nvGlV6LkCgYEA4rabAGB7OQTunGj6BiQBN8AnG/1B77HBA/VRy3YUHdPaBYtldLuX\nZrQKuE3l13uX0whXr+BQVDtDiegocz4r41/MR9uUoQFHnsL25D+A44xveT2scTHm\nBHpUprq8ti4XyNJGpnZXSxQCRzhcGnJItvfOaQWW+slEnR4RUuWCdjUCgYEAo6Mn\nmT+NyNCfJHWvF951fvRi7liktRzIcIL7Hu4gDkTTJ7U/Ms3OgQTsQ6VIfNeotAYC\nFe/GVb+SB91MnnCFwPbwt1vIwdLGvKtAUq3OQvE8Jv1LCC3XQJcRv/tJuP6lLz1t\nWNF59Uz0Ar6VN9tIctdribKGP6Dxg32OLlrV5G8CgYEAotnQlYC4gsjMLYYqsuaC\nCW35qd1N08O3hgRd8OysnpBi98Cd7DAkHR4O5TzvcM3SzUAc3LUgfqDjbthY1g8+\nr2FM+AD+zniA3cXmWyZSiyGBoXFvwQ+6zlShIfLZQ3PwmcyR+1jec4u35zjQ0B5v\npR50InRlc1fH9aR3hThfclECgYEAh+bv80GqIpbJJQGsKnmyQX78TxFFsbk26uKN\nZxHDg7Y7XCYWV74/fD23bzLtMen2DZVT1B4wLXUN9gQgJxIys6EjKFVNNVQ1g+oC\nYOhCfqxVFdiVoTRZKiaNMlGj18V9MO+mSfangEep/EGGMj6nO+GXSWQARQYIrvju\nxabhL3cCgYEAlPAbQgqljbfs6pIG5eEKHNLXaCZxFeZDQ+PQ9CYBsCL0nPo0e1iw\nHNFx2A/BN0hEZxiOO0LnDV5paFhAd+rFhSvxdgwhOBvxU1TDwcNCoyqpbJ57BB3e\n5d+ShkCu0K3LbKn65ZAtvJCB9yleu5VUIt6i+q/aaPLcWTcf+YxVDfM=\n-----END RSA PRIVATE KEY-----',
                        'KeyName': 'Piggy_SSH_Key_0194afd1', 'KeyPairId': 'key-0a070814c64fa0e65', 'ResponseMetadata': {'RequestId': '56d9520a-80e8-4603-9a92-6a78c3ef42ca', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '56d9520a-80e8-4603-9a92-6a78c3ef42ca', 'cache-control': 'no-cache, no-store', 'strict-transport-security': 'max-age=31536000; includeSubDomains', 'content-type': 'text/xml;charset=UTF-8', 'content-length': '2103', 'vary': 'accept-encoding', 'date': 'Sat, 22 May 2021 00:23:15 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}


def test_get_ssh_key():
    client = botocore.session.get_session().create_client('ec2')
    with Stubber(client) as stubber:
        stubber.add_response(
            'create_key_pair', create_key_pair_resp, {'KeyName': ANY})
        key = setup._get_ssh_key(client=client)
    assert key.name == create_key_pair_resp['KeyName']
    assert key.material == create_key_pair_resp['KeyMaterial']


test_setup_vars = {
    'aws_region': 'us-east-2',
    'ec2': boto3.client('ec2'),
    'cloudhsmv2': boto3.client('cloudhsmv2'),
    'path': '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/tests/test_files',
    'customer_ca_key_password': 'password1',
    'crypto_officer_password': 'password1',
    'crypto_user_username': 'cryptosuer',
    'crypto_user_password': 'password'
}


ssh_key = Mock()
ssh_key.fingerprint = '3b:be:63:1a:58:ad:dd:1c:70:78:34:15:04:ec:16:44:5a:0a:e3:f5'
ssh_key.id = 'key-0ba3c39febf94bc76'
ssh_key.material = '-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAgXfOzntBKb9+VkQdkIB0JtyAWN+TZNCiqLlEc7XNRs3H3Tt0\nezQZ0YCfZPYrF+qKmoODCD66GQcD3yG/TQ4fPihMciEh8QdzYyrMNzg/6PLGI+Bi\nVyOAj/GoKhamvu9okkFdU94wd7NVLAWtpqY2cWHOakaOG5+/isgI+zP0a7PtOClf\nlIiG0y1H4ukGJQPn1VtUJKAkSKELc/DBfr7LHEkG6GsNQVOjOj0jwBNr2pOt0uSX\nHX1n2Z20yZnyT42s68TR+Ksxa70FU3/BJOXZHEFhF1RMtR4a3wX6RrLotgKvMFJi\no6OlEyBI8yFnlBi9ju1QjY+86O0rMO8Oqux7SQIDAQABAoIBAHljYsTYbZ1+DS9H\nCE0/EyiIn9I0NhdVQt1db9/puoFDWbyFDU6i5/41Ub2wzXDMGI6M9eNaJNRobmnc\nU2gk8Igv8pUjmZZK/RYiv3yawdlhHwPuU2YORHEyDBECUe89u1c98Ao9jkX9H8N5\nw3o3513hbU7Zvk4KNuYhbcJR0T7VBJRDAJNh7VaspQmDDc5pjmf+MRCr9It8eME+\nZ4jSzO8S+RdtR6kGl9WABEXVvBJuVmMGlMtu0SXsUilxRLNQvhB6q4L8L4OkTJxi\nCUXlJYSlbJS0Gj4j9ChsIGKgTkZ3qmspqUkiCk244l0DFlZmz5zFBQH3B3RtgQTf\ndu+EdJ0CgYEA4HU/nEngpuh1DKX7hN5nUQdF75uRmMICnkOVsjMEIOPBb7+qhxu1\n1u5BN2f6jQD4g5YHUtCE5oyObtCRAe7aFi1n0f3faQFwo78fMBSZ6NgOjkv/BfuP\nTLeH2TBbfibBHko1AHIYOz8+VcehBg7rV0v+/ZHL58Zq4IAxcrfOR0MCgYEAk6lY\n0lvwbyoqqldjCT3hylBDF2hAi/hEsa6pVtlmLPGmjpzXaJYnC6S0KVicDDCj7E9Z\nj8zjDhtdBb9tXDrMwVZ8C+JIjdfslSu+qVpT/5csMr7MYSzLPBLRoP2Kmj0KbUua\nVpqiqtEsfsVoNh50gPj/znHH0V7ucKjUymk/rIMCgYEAomp08uRKWLwQJmzciRJd\ndDZtFqpdOkn4lwiUg3OC40GqsO/htw4IEFQqgKsOk4VGTgD7n6Me56yBTBJDO0DY\nMf/9BehMBrFyDiq3qJTfoarlLXY0POIAmSScej4RlkD4sLBFleL5QbXLp0pia/3T\nsUFea6FaCIZ8w6I/JaF28/0CgYAHas5HYs7lBp02CUW0RSN+YiG8n0P+w+3PbxKa\nhjkXsNvI9h/r5P75GsDiAs1z302cpS++hXAyWTWHAGKh62I1o/5/KlKyrVH4/EWL\nhDoL8LALrIHfr7xVvCxDhfjcXoyTiOSrzQC2y+MMSyY88bKwd9GBsT10Sux3REPM\nFxVXuQKBgQCgV8nokRRUcxu15m14jbLApwq7+B9F+zK+b7yhA/hOPyJAhEXeCqth\n99bJtfwzady4FjXekcnZrBRC/lHNnZn9HIyS+VX/VWNDugaygt6xKJ0Bmf/ln7j3\nrtxGc4eiBHAMWbrAqsSIUTJ0zm083CL6Vl2NsS403Was12qcq0N3vw==\n-----END RSA PRIVATE KEY-----'
ssh_key.name = 'Piggy_SSH_Key_cf865bae'
ssh_key.wrtie_to_file.return_value = True

build_infra_resp = {'cluster_id': 'cluster-lbtkdldygfh',
                    'vpc_id': 'vpc-06f745fe81ec3c1a8', 'instance_id': 'i-051bdb2ae099024a5'}

cluster = Mock()
cluster.id = 'cluster-lbtkdldygfh'
cluster.azs = ['us-east-2a', 'us-east-2b', 'us-east-2c']
cluster.csr = "-----BEGIN CERTIFICATE REQUEST-----\nMIIC0TCCAbkCAQAwgYsxRDAJBgNVBAYTAlVTMAkGA1UECAwCQ0EwDQYDVQQKDAZD\nYXZpdW0wDQYDVQQLDAZOM0ZJUFMwDgYDVQQHDAdTYW5Kb3NlMUMwQQYDVQQDDDpI\nU006QjRGMUU4QjY3OTY3NTg2M0Y4REIzMjExMTM2NEIzOlBBUlROOjEzLCBmb3Ig\nRklQUyBtb2RlMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvDY9IZlR\nThUQ2Jfc+JWPC15WqZbMRKiEba+FICcwno+izaDza+rzpqtaU0Q5UVYGOe4vEtVj\nxsj3hdhXc2rK53vhw4EdmKojPzAy3F/TJGzSvzIlPUCdWLtbKlNEkg/VGu1YcsMV\nvQvyGFSusj8idWT4DvsZxPuEwiXE4qEPmyB1uo2lKIYWfulP9QrRdvnrBF/zBmXO\nblg3zHf1KQ8bYWW8Lc/DGcRnRvPBfDvYNS6DJPrMiM+QeqhM5Iegu7OlTOTkV72d\nmaMqTuuWOGrb6LCDr7hWGfjAE3517Jt2ia2bB8YE5Wda4mUBEmpVl5Kho547S6Sx\nMiChX3U3VCHbVwIDAQABoAAwDQYJKoZIhvcNAQELBQADggEBAKqEhDqVClGRES2C\nIwqKxPVYo5lbynEZ94qSeKzI9rgoW3kPVyro1vBxAzMwDSJd1TXmw2fJAOY7Zdiw\n+j0SMZCb81ehVNa8VRUsOrU6phC72jqUSFSWpRkCDxc9inIdUfBpqIQxsd0JpYB7\nzvyuKILMNDI3Ys7S4i1ErHv8IyDUdmVjP+qRaEAhecBEt5GVZPDg/vjEsS83hqf4\n7EZ9S9noDgnoa79W1ovFr8wW8EZ5Spi50D5hsFCMy4a4rErwneAATEm2MmtLfIy7\nCWTUET6SZN2Ncn/oM1ulVYofYTctmpiAGMMjB9joA6nW0I2QfhaSOTugU+NmwnC0\nOo+qHwM=\n-----END CERTIFICATE REQUEST-----\n"
# cluster.initialize.return_value = True
# cluster.activate.return_value = True


instance = Mock()
instance.id = 'i-051bdb2ae099024a5'
instance.public_ip_address = '18.222.220.62'
instance.ssh_key_file = '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/tests/test_files/cluster-lbtkdldygfh/Piggy_SSH_Key_cf865bae.pem'

hsm = Mock()
hsm.id = 'hsm-u25cdzfj56s'
hsm.cluster_id = 'cluster-lbtkdldygfh'

certs = Mock()
certs.pem_private_key = b'-----BEGIN RSA PRIVATE KEY-----\nProc-Type: 4,ENCRYPTED\nDEK-Info: AES-256-CBC,6F7135B1FF40772431A52344F2C28F3E\n\n17swNOMYJtX7XSMnL9C6MPmIaI34peR4CPUt0IWaiu5AfuHeGrho2PhaljlKX/Lt\nw4ykD/zrrKk88BrhTTPhArJNOporxC8d2BeyXtiIXqz4+yn256Ox4zfzkAdGq2xq\nRRzNHZot417yqUcIUSI+H39WkHVunhpNWJixMFKp5yhTf1JUHXCNOPNr4M/aALFD\n9U1pJ4t1H0umrNdHKI7lWat5+lnfXPe9GrQ+NYYobM6MX6uM7Mb9ggzN0234rOQM\nhLYdMGUCvXrWUoVHQ7mRR/DBa4S2ptAbyHsQZCOLLvnfQE+lCpT8SxkUf3xyeRGC\njGqHWANEHbdW7LKNS9aSbjoM5fXx9ToJJJiFAo4RuFVpTufVh8zhPscx1DjvVXLQ\nPo1WZrZusELmhzvJOgJQkNvrVnfGmHtB6CuzHUyXAriN1VUekWlNYi3gP5fC5MjO\n+bISUXiGLHi0DYe+x+0PHquI/u5Gugeh/k+q7pvbTnZ/r9so+P4aW2q1IDloFYXv\nDVO3VGdSef3mp1k4B49257K5Vri1XYjLXAkbQyuVFGWphQ4bSHCscZhAevpzCDVk\nPrD0R+egohy/ErZllbp7+rc+VpHMBXpi5LEYAetpdR5URrgZAP5L2WWS4/WtsoAb\nnApoqMuq53QaOjjWx2wTtyU1lOGoT5pSS4/c1UKxV/72Dpbu96e8MBhjwwmIZiGW\nD5fjHJzEDZxtA/YFS1UHxb8hPsMRJkb67dR1fOSDXBWLZdi0MQ1que60bXV4+a8W\nJTKzpf8yOaNkI98QqGcvbfZWcgQ/sMVduOrx1VsndFqXiJ4M5heCAU+3gKAaX9HG\nkoYtTnp+LbshZNawdyW1MtdeeP8zrVfAx+WrYcI8/XL7+tge4n6VkVoqxD6IJX3a\nZ6EPY/J/IBSQsYIeQe4QDrjR1ztbNBS4KMBlJofM3IlPY5ee9L61QBwCW9zM9FNI\n8s54O2D3nGgc5fGteB5Ze4qGDFshPKXJU5uFcSZ19202NhuPTeWkuCFXMSz41eRL\n3kog6OW5q3UNPgMAb9nmuQzDt7fALY9fzl3n6CV/lli68oP8ji8iqqTvP5tjkgQa\nVC5IY97qs0JoeEnORSMo0SdnL/4YK5eni5pZxR1pvdXV0t4Vqap0f2SEi0yL8HxA\nLtmCTYdD9e/IEFcPjoFp/M5NcPUP81S8gJUwLWo9eI2Cpe7tZBrdWHQ6Z8Kc3mQQ\nflT5wXps/H9CmVkDFIu/VuOLxHxVzl7L20a8zkZDRhqnij/IqG+UM27dZ/Rc48Vu\nG7S4um6eahANe7r2n4gDApQBlziUApR5PIeZUFpKELTNKJ4BY1Ttsmt+y3EDU8Uk\nBt38zSYs251WmKjuRwR99dny7p+jjxBdJSW5xpoSv7/DdH9UaF2PhAXetdeYRWnt\nu2lshQzrZBruQpcSCbFS3FvmlNlKc4zoSt9lNp+NgGLZzbLciSQhF5+nyz2k+K26\nZyTbjiaWhK+AfxtgWG84iuJI7DtcuP1MRuud0aV9PZV/KZ8X1AnqDsxCUsUwjtAj\nM5PTCWRL0tSkQKRue8iueN498DdzlK+QqkRGdN3j/YTmh8KZzLvjiUxAUPXByjaV\n-----END RSA PRIVATE KEY-----\n'
certs.pem_csr = '-----BEGIN CERTIFICATE REQUEST-----\nMIIC0TCCAbkCAQAwgYsxRDAJBgNVBAYTAlVTMAkGA1UECAwCQ0EwDQYDVQQKDAZD\nYXZpdW0wDQYDVQQLDAZOM0ZJUFMwDgYDVQQHDAdTYW5Kb3NlMUMwQQYDVQQDDDpI\nU006QjRGMUU4QjY3OTY3NTg2M0Y4REIzMjExMTM2NEIzOlBBUlROOjEzLCBmb3Ig\nRklQUyBtb2RlMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvDY9IZlR\nThUQ2Jfc+JWPC15WqZbMRKiEba+FICcwno+izaDza+rzpqtaU0Q5UVYGOe4vEtVj\nxsj3hdhXc2rK53vhw4EdmKojPzAy3F/TJGzSvzIlPUCdWLtbKlNEkg/VGu1YcsMV\nvQvyGFSusj8idWT4DvsZxPuEwiXE4qEPmyB1uo2lKIYWfulP9QrRdvnrBF/zBmXO\nblg3zHf1KQ8bYWW8Lc/DGcRnRvPBfDvYNS6DJPrMiM+QeqhM5Iegu7OlTOTkV72d\nmaMqTuuWOGrb6LCDr7hWGfjAE3517Jt2ia2bB8YE5Wda4mUBEmpVl5Kho547S6Sx\nMiChX3U3VCHbVwIDAQABoAAwDQYJKoZIhvcNAQELBQADggEBAKqEhDqVClGRES2C\nIwqKxPVYo5lbynEZ94qSeKzI9rgoW3kPVyro1vBxAzMwDSJd1TXmw2fJAOY7Zdiw\n+j0SMZCb81ehVNa8VRUsOrU6phC72jqUSFSWpRkCDxc9inIdUfBpqIQxsd0JpYB7\nzvyuKILMNDI3Ys7S4i1ErHv8IyDUdmVjP+qRaEAhecBEt5GVZPDg/vjEsS83hqf4\n7EZ9S9noDgnoa79W1ovFr8wW8EZ5Spi50D5hsFCMy4a4rErwneAATEm2MmtLfIy7\nCWTUET6SZN2Ncn/oM1ulVYofYTctmpiAGMMjB9joA6nW0I2QfhaSOTugU+NmwnC0\nOo+qHwM=\n-----END CERTIFICATE REQUEST-----\n'
certs.pem_hsm_cert = b'-----BEGIN CERTIFICATE-----\nMIIDVTCCAj2gAwIBAgIUGVpAlXDcW6bULCcyAPeUMgY2Hf4wDQYJKoZIhvcNAQEL\nBQAwPTELMAkGA1UEBhMCVVMxCjAIBgNVBAgMAS4xCjAIBgNVBAcMAS4xCjAIBgNV\nBAoMAS4xCjAIBgNVBAMMAS4wHhcNMjEwNTIzMTcwNDQ2WhcNMzEwNTIzMTgwNDQ2\nWjCBizFEMAkGA1UEBhMCVVMwCQYDVQQIDAJDQTANBgNVBAoMBkNhdml1bTANBgNV\nBAsMBk4zRklQUzAOBgNVBAcMB1Nhbkpvc2UxQzBBBgNVBAMMOkhTTTpCNEYxRThC\nNjc5Njc1ODYzRjhEQjMyMTExMzY0QjM6UEFSVE46MTMsIGZvciBGSVBTIG1vZGUw\nggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC8Nj0hmVFOFRDYl9z4lY8L\nXlaplsxEqIRtr4UgJzCej6LNoPNr6vOmq1pTRDlRVgY57i8S1WPGyPeF2Fdzasrn\ne+HDgR2YqiM/MDLcX9MkbNK/MiU9QJ1Yu1sqU0SSD9Ua7VhywxW9C/IYVK6yPyJ1\nZPgO+xnE+4TCJcTioQ+bIHW6jaUohhZ+6U/1CtF2+esEX/MGZc5uWDfMd/UpDxth\nZbwtz8MZxGdG88F8O9g1LoMk+syIz5B6qEzkh6C7s6VM5ORXvZ2ZoypO65Y4atvo\nsIOvuFYZ+MATfnXsm3aJrZsHxgTlZ1riZQESalWXkqGjnjtLpLEyIKFfdTdUIdtX\nAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAKAogyiwCBLFzu7k0i42NQ4AZbYkQg1k\nS6e7N3oOVwG/BEaeyt47Uc99g0cSnhtvet/Mlt4GURPc66bZY1EoHQ0N/UFF3BCB\nk4Gumu6BToIogAjiFmKLDVgeWrCtJlHxdYLe6lyiIEbGuuMBOZ6lmLxRS8Fj6/as\nblxkvdbrVjKutFJPwUI46gmGvaSP+x1lV3KyJcRgG2Q4Sw0hctMFm88jjZZ9mK5F\n3am64/bU9jIa4edirjv5fXhgQcxSlLMA1ltQtgQBypnHVUlgCAG28n8YLjoS2lQO\nbiwa/jYdJFKwyZ08Mv23ixNeACb8PNT61iHsqa6Xq6igYUwaqwIFH2Y=\n-----END CERTIFICATE-----\n'
certs.pem_ca_cert = b'-----BEGIN CERTIFICATE-----\nMIIDCDCCAfCgAwIBAgIBATANBgkqhkiG9w0BAQsFADA9MQswCQYDVQQGEwJVUzEK\nMAgGA1UECAwBLjEKMAgGA1UEBwwBLjEKMAgGA1UECgwBLjEKMAgGA1UEAwwBLjAe\nFw0yMTA1MjMxNzA0NDZaFw0zMTA1MjMxODA0NDZaMD0xCzAJBgNVBAYTAlVTMQow\nCAYDVQQIDAEuMQowCAYDVQQHDAEuMQowCAYDVQQKDAEuMQowCAYDVQQDDAEuMIIB\nIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxOECV3e8foFfXoqsWZJ+Wwo4\nRQFwOdQvWyH/dGWadbN3G/KMxOxZIcpAL0z/UmpG9hiqOem6OdmQyzdTI6ZfUCkn\nKXEinFnS+ZpA6zetrfVl5f7h3fyJAu8Da2o9eaR8BMn2ATg0QRv6aWpwuMPlIQ2h\ni4Fp0zmp2Xp3aO5wNoY9Thw6/eM1MWk0WIDvkmzEVqKhCpvGCwO0bD+NWMYlhZxM\nw9PTSVpMS5zq0ugvWP9I6vO4ZEm422e6MzdvED4LAD1FAS519I8Y+VKWVP5Wrr/2\nL2ovK6ml7mLQi9Bs0PU9HuYqh1tX8Vj5658dDu6L8t1IBR7gb8mrt2zH5fyqnwID\nAQABoxMwETAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQBtWL/g\nVoclYzrJAeAkcMPewPD5+4O3UfszRvL4EcProx1/XPsvVIjRQ4oBDrCWlmiIxq02\n97JzucooTsyVcJycR4ppoEhW/1XXHyrbBE8nVAcS0x+eQpwJQ9OtW0NM+qAaEjZd\nU/vqeYZwmeSs4aHXhPhifeazrzzaZSVhlHs2rEW1/taxIxCFYT6SipJDLqVlKt6f\nksXtdn8BOcYy1Q6ybXpN+g9D3EnM/X4uHyt3pJ0y14KZHBDd9oYwpx2SLc2SGneG\nZb5zsWluSmrtQS1U8TgT9PrgcTZGwQcurka3yzdb84IkZ0ZSJGn0sZ1TdHWeQB1j\nbix3cnyr6DF7ZD5n\n-----END CERTIFICATE-----\n'


@patch('app.controllers.setup_controller._get_ssh_key', return_value=ssh_key, autospec=True)
@patch('app.controllers.setup_controller._build_infrastructure', return_value=build_infra_resp, autospec=True)
@patch('app.controllers.setup_controller._cluster', return_value=cluster, autospec=True)
@patch('app.controllers.setup_controller._instance', return_value=instance, autospec=True)
@patch('app.controllers.setup_controller._hsm', return_value=hsm, autospec=True)
@patch('app.controllers.setup_controller._certs', return_value=certs, autospec=True)
@patch('app.controllers.setup_controller._upload_customer_ca_cert', return_value=True, autospec=True)
@patch('app.controllers.setup_controller._initialize_cluster', return_value=True, autospec=True)
@patch('app.controllers.setup_controller._activate_cluster', return_value=True, autospec=True)
def test_run(*args):
    test_setup = setup.Setup(**test_setup_vars)
    resp = test_setup.run()
    assert resp['cluster_id'] == cluster.id
    assert resp['ssh_key_name'] == ssh_key.name
    assert resp['ssh_key_pem'] == ssh_key.material
    assert resp['instance_id'] == instance.id

    os.remove(os.path.join(
        test_setup_vars['path'], cluster.id, 'customerCA.key'))
    os.remove(os.path.join(
        test_setup_vars['path'], cluster.id, 'customerCA.crt'))
    os.remove(os.path.join(
        test_setup_vars['path'], cluster.id, f'{cluster.id}_ClusterCSR.csr'))
    os.remove(os.path.join(
        test_setup_vars['path'], cluster.id, f'{cluster.id}_CustomerHSMCertificate.crt'))
    os.remove(instance.ssh_key_file)
    os.rmdir(os.path.join(test_setup_vars['path'], cluster.id))

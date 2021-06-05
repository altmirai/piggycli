import boto3
import botocore.session
from botocore.response import StreamingBody
import io
import json
import os
import datetime
from botocore.vendored.six import StringIO
from dateutil.tz import tzutc
from unittest.mock import Mock

aws_region = 'us-east-2'

resource = boto3.resource('ec2')
ec2 = botocore.session.get_session().create_client('ec2')
cloudhsmv2 = botocore.session.get_session().create_client('cloudhsmv2')
s3 = botocore.session.get_session().create_client('s3', region_name=aws_region)

test_path = '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/tests/test_files'
production_path = '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/production_files'
credentials_file_path = os.path.join(
    test_path,
    '.piggy',
    'credentials.json'
)

cluster_id = 'cluster-lbtkdldygfh'
instance_id = 'i-051bdb2ae099024a5'
vpc_id = 'vpc-06f745fe81ec3c1a8'

hsm_id = 'hsm-u25cdzfj56s'
eni_ip = '10.1.0.9'

ssh_key_name = 'Piggy_SSH_Key_0194afd1'
ssh_key_file = os.path.join(test_path, cluster_id, f'{ssh_key_name}.pem')

azs = ['us-east-2a', 'us-east-2b', 'us-east-2c']
public_ip_address = '18.222.220.62'

aws_access_key_id = 'AKIA5YNNN4JH6JDQF5XH'
aws_secret_access_key = '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'
customer_ca_key_password = 'password1'
crypto_officer_password = 'password1'
crypto_user_username = 'cryptouser'
crypto_user_password = 'password1'

KeyFingerprint = '08:c9:28:e5:24:38:d5:ef:9b:a1:76:22:9f:00:0c:eb:47:16:59:cd'
KeyMaterial = '-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAkOrCB3e0Fj/Cv797THZn5YgxIPywNdlg284rMSshrLl8QC83\n0ck0K9CP3Y+rCuHGx7t/2tCtl66uKlwOPFvWGDi+akonkUeVqnV8U1z5jNhI8SwY\niXtcFX0twIGHaaxYQrWZvOUAnmE8JUGd7Pysy4Sy7/ZEldXwEN3fN2NIPRnQwii7\nS5tv573C2am2MMXtwEKtQi3uWgPu//maXqoM0/PuxTDk9DUKnN88nvNBMoTlHr1P\nl9QsHMPyXvJ/+TTPdVybXwMvv1KgCMeGid43CPu7SFa8trx9DuvSY03TwYyhZIp6\nMsPZot6pu+opRXgF7SkSpp/+ABPoA836sPF0+wIDAQABAoIBAAESi68Mdru3axSK\nMTpmoewz7tEkrZUob6wQwYcSn6QslzvOXaZiy80LNRVZq9VfyF3QCGkxJCe8NjPA\nDKbrsxDo0pfsxpAvrG7fgbUIOhyNuTR3tBLIY+0QyRbknoDsspaDy4h3VWLWq2BH\nNQj88bZr2/skomtNcwJc8frx9CXnmR1erB8d7UybKFiYL4ggM/MVQbdn66ZpmKCK\naZ774lbgdiwp8YZp1ANFw7zBr1MTqXKLmghtYZoornRUVk2c3OPUII62jmarUaqn\nKL+q2198j0axDsmFCAALTbmxjo//XWxwTeaRNwsi0hqeENEy1ywtidn1A8eHJaOi\nvGlV6LkCgYEA4rabAGB7OQTunGj6BiQBN8AnG/1B77HBA/VRy3YUHdPaBYtldLuX\nZrQKuE3l13uX0whXr+BQVDtDiegocz4r41/MR9uUoQFHnsL25D+A44xveT2scTHm\nBHpUprq8ti4XyNJGpnZXSxQCRzhcGnJItvfOaQWW+slEnR4RUuWCdjUCgYEAo6Mn\nmT+NyNCfJHWvF951fvRi7liktRzIcIL7Hu4gDkTTJ7U/Ms3OgQTsQ6VIfNeotAYC\nFe/GVb+SB91MnnCFwPbwt1vIwdLGvKtAUq3OQvE8Jv1LCC3XQJcRv/tJuP6lLz1t\nWNF59Uz0Ar6VN9tIctdribKGP6Dxg32OLlrV5G8CgYEAotnQlYC4gsjMLYYqsuaC\nCW35qd1N08O3hgRd8OysnpBi98Cd7DAkHR4O5TzvcM3SzUAc3LUgfqDjbthY1g8+\nr2FM+AD+zniA3cXmWyZSiyGBoXFvwQ+6zlShIfLZQ3PwmcyR+1jec4u35zjQ0B5v\npR50InRlc1fH9aR3hThfclECgYEAh+bv80GqIpbJJQGsKnmyQX78TxFFsbk26uKN\nZxHDg7Y7XCYWV74/fD23bzLtMen2DZVT1B4wLXUN9gQgJxIys6EjKFVNNVQ1g+oC\nYOhCfqxVFdiVoTRZKiaNMlGj18V9MO+mSfangEep/EGGMj6nO+GXSWQARQYIrvju\nxabhL3cCgYEAlPAbQgqljbfs6pIG5eEKHNLXaCZxFeZDQ+PQ9CYBsCL0nPo0e1iw\nHNFx2A/BN0hEZxiOO0LnDV5paFhAd+rFhSvxdgwhOBvxU1TDwcNCoyqpbJ57BB3e\n5d+ShkCu0K3LbKn65ZAtvJCB9yleu5VUIt6i+q/aaPLcWTcf+YxVDfM=\n-----END RSA PRIVATE KEY-----'
KeyName = 'Piggy_SSH_Key_0194afd1'
KeyPairId = 'key-0a070814c64fa0e65'

KeyFingerprint2 = 'de:7b:e3:aa:81:52:89:be:a5:01:a0:87:8d:67:76:47:e8:a5:9f:0c'
KeyName2 = 'Piggy_SSH_Key_40cc19f5'
KeyPairId2 = 'key-071d152e1ec5428df'

passphrase = 'password1'
pem_private_key = b'-----BEGIN RSA PRIVATE KEY-----\nProc-Type: 4,ENCRYPTED\nDEK-Info: AES-256-CBC,6F7135B1FF40772431A52344F2C28F3E\n\n17swNOMYJtX7XSMnL9C6MPmIaI34peR4CPUt0IWaiu5AfuHeGrho2PhaljlKX/Lt\nw4ykD/zrrKk88BrhTTPhArJNOporxC8d2BeyXtiIXqz4+yn256Ox4zfzkAdGq2xq\nRRzNHZot417yqUcIUSI+H39WkHVunhpNWJixMFKp5yhTf1JUHXCNOPNr4M/aALFD\n9U1pJ4t1H0umrNdHKI7lWat5+lnfXPe9GrQ+NYYobM6MX6uM7Mb9ggzN0234rOQM\nhLYdMGUCvXrWUoVHQ7mRR/DBa4S2ptAbyHsQZCOLLvnfQE+lCpT8SxkUf3xyeRGC\njGqHWANEHbdW7LKNS9aSbjoM5fXx9ToJJJiFAo4RuFVpTufVh8zhPscx1DjvVXLQ\nPo1WZrZusELmhzvJOgJQkNvrVnfGmHtB6CuzHUyXAriN1VUekWlNYi3gP5fC5MjO\n+bISUXiGLHi0DYe+x+0PHquI/u5Gugeh/k+q7pvbTnZ/r9so+P4aW2q1IDloFYXv\nDVO3VGdSef3mp1k4B49257K5Vri1XYjLXAkbQyuVFGWphQ4bSHCscZhAevpzCDVk\nPrD0R+egohy/ErZllbp7+rc+VpHMBXpi5LEYAetpdR5URrgZAP5L2WWS4/WtsoAb\nnApoqMuq53QaOjjWx2wTtyU1lOGoT5pSS4/c1UKxV/72Dpbu96e8MBhjwwmIZiGW\nD5fjHJzEDZxtA/YFS1UHxb8hPsMRJkb67dR1fOSDXBWLZdi0MQ1que60bXV4+a8W\nJTKzpf8yOaNkI98QqGcvbfZWcgQ/sMVduOrx1VsndFqXiJ4M5heCAU+3gKAaX9HG\nkoYtTnp+LbshZNawdyW1MtdeeP8zrVfAx+WrYcI8/XL7+tge4n6VkVoqxD6IJX3a\nZ6EPY/J/IBSQsYIeQe4QDrjR1ztbNBS4KMBlJofM3IlPY5ee9L61QBwCW9zM9FNI\n8s54O2D3nGgc5fGteB5Ze4qGDFshPKXJU5uFcSZ19202NhuPTeWkuCFXMSz41eRL\n3kog6OW5q3UNPgMAb9nmuQzDt7fALY9fzl3n6CV/lli68oP8ji8iqqTvP5tjkgQa\nVC5IY97qs0JoeEnORSMo0SdnL/4YK5eni5pZxR1pvdXV0t4Vqap0f2SEi0yL8HxA\nLtmCTYdD9e/IEFcPjoFp/M5NcPUP81S8gJUwLWo9eI2Cpe7tZBrdWHQ6Z8Kc3mQQ\nflT5wXps/H9CmVkDFIu/VuOLxHxVzl7L20a8zkZDRhqnij/IqG+UM27dZ/Rc48Vu\nG7S4um6eahANe7r2n4gDApQBlziUApR5PIeZUFpKELTNKJ4BY1Ttsmt+y3EDU8Uk\nBt38zSYs251WmKjuRwR99dny7p+jjxBdJSW5xpoSv7/DdH9UaF2PhAXetdeYRWnt\nu2lshQzrZBruQpcSCbFS3FvmlNlKc4zoSt9lNp+NgGLZzbLciSQhF5+nyz2k+K26\nZyTbjiaWhK+AfxtgWG84iuJI7DtcuP1MRuud0aV9PZV/KZ8X1AnqDsxCUsUwjtAj\nM5PTCWRL0tSkQKRue8iueN498DdzlK+QqkRGdN3j/YTmh8KZzLvjiUxAUPXByjaV\n-----END RSA PRIVATE KEY-----\n'
pem_csr = '-----BEGIN CERTIFICATE REQUEST-----\nMIIC0TCCAbkCAQAwgYsxRDAJBgNVBAYTAlVTMAkGA1UECAwCQ0EwDQYDVQQKDAZD\nYXZpdW0wDQYDVQQLDAZOM0ZJUFMwDgYDVQQHDAdTYW5Kb3NlMUMwQQYDVQQDDDpI\nU006QjRGMUU4QjY3OTY3NTg2M0Y4REIzMjExMTM2NEIzOlBBUlROOjEzLCBmb3Ig\nRklQUyBtb2RlMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvDY9IZlR\nThUQ2Jfc+JWPC15WqZbMRKiEba+FICcwno+izaDza+rzpqtaU0Q5UVYGOe4vEtVj\nxsj3hdhXc2rK53vhw4EdmKojPzAy3F/TJGzSvzIlPUCdWLtbKlNEkg/VGu1YcsMV\nvQvyGFSusj8idWT4DvsZxPuEwiXE4qEPmyB1uo2lKIYWfulP9QrRdvnrBF/zBmXO\nblg3zHf1KQ8bYWW8Lc/DGcRnRvPBfDvYNS6DJPrMiM+QeqhM5Iegu7OlTOTkV72d\nmaMqTuuWOGrb6LCDr7hWGfjAE3517Jt2ia2bB8YE5Wda4mUBEmpVl5Kho547S6Sx\nMiChX3U3VCHbVwIDAQABoAAwDQYJKoZIhvcNAQELBQADggEBAKqEhDqVClGRES2C\nIwqKxPVYo5lbynEZ94qSeKzI9rgoW3kPVyro1vBxAzMwDSJd1TXmw2fJAOY7Zdiw\n+j0SMZCb81ehVNa8VRUsOrU6phC72jqUSFSWpRkCDxc9inIdUfBpqIQxsd0JpYB7\nzvyuKILMNDI3Ys7S4i1ErHv8IyDUdmVjP+qRaEAhecBEt5GVZPDg/vjEsS83hqf4\n7EZ9S9noDgnoa79W1ovFr8wW8EZ5Spi50D5hsFCMy4a4rErwneAATEm2MmtLfIy7\nCWTUET6SZN2Ncn/oM1ulVYofYTctmpiAGMMjB9joA6nW0I2QfhaSOTugU+NmwnC0\nOo+qHwM=\n-----END CERTIFICATE REQUEST-----\n'
pem_hsm_cert = b'-----BEGIN CERTIFICATE-----\nMIIDVTCCAj2gAwIBAgIUGVpAlXDcW6bULCcyAPeUMgY2Hf4wDQYJKoZIhvcNAQEL\nBQAwPTELMAkGA1UEBhMCVVMxCjAIBgNVBAgMAS4xCjAIBgNVBAcMAS4xCjAIBgNV\nBAoMAS4xCjAIBgNVBAMMAS4wHhcNMjEwNTIzMTcwNDQ2WhcNMzEwNTIzMTgwNDQ2\nWjCBizFEMAkGA1UEBhMCVVMwCQYDVQQIDAJDQTANBgNVBAoMBkNhdml1bTANBgNV\nBAsMBk4zRklQUzAOBgNVBAcMB1Nhbkpvc2UxQzBBBgNVBAMMOkhTTTpCNEYxRThC\nNjc5Njc1ODYzRjhEQjMyMTExMzY0QjM6UEFSVE46MTMsIGZvciBGSVBTIG1vZGUw\nggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC8Nj0hmVFOFRDYl9z4lY8L\nXlaplsxEqIRtr4UgJzCej6LNoPNr6vOmq1pTRDlRVgY57i8S1WPGyPeF2Fdzasrn\ne+HDgR2YqiM/MDLcX9MkbNK/MiU9QJ1Yu1sqU0SSD9Ua7VhywxW9C/IYVK6yPyJ1\nZPgO+xnE+4TCJcTioQ+bIHW6jaUohhZ+6U/1CtF2+esEX/MGZc5uWDfMd/UpDxth\nZbwtz8MZxGdG88F8O9g1LoMk+syIz5B6qEzkh6C7s6VM5ORXvZ2ZoypO65Y4atvo\nsIOvuFYZ+MATfnXsm3aJrZsHxgTlZ1riZQESalWXkqGjnjtLpLEyIKFfdTdUIdtX\nAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAKAogyiwCBLFzu7k0i42NQ4AZbYkQg1k\nS6e7N3oOVwG/BEaeyt47Uc99g0cSnhtvet/Mlt4GURPc66bZY1EoHQ0N/UFF3BCB\nk4Gumu6BToIogAjiFmKLDVgeWrCtJlHxdYLe6lyiIEbGuuMBOZ6lmLxRS8Fj6/as\nblxkvdbrVjKutFJPwUI46gmGvaSP+x1lV3KyJcRgG2Q4Sw0hctMFm88jjZZ9mK5F\n3am64/bU9jIa4edirjv5fXhgQcxSlLMA1ltQtgQBypnHVUlgCAG28n8YLjoS2lQO\nbiwa/jYdJFKwyZ08Mv23ixNeACb8PNT61iHsqa6Xq6igYUwaqwIFH2Y=\n-----END CERTIFICATE-----\n'
pem_ca_cert = b'-----BEGIN CERTIFICATE-----\nMIIDCDCCAfCgAwIBAgIBATANBgkqhkiG9w0BAQsFADA9MQswCQYDVQQGEwJVUzEK\nMAgGA1UECAwBLjEKMAgGA1UEBwwBLjEKMAgGA1UECgwBLjEKMAgGA1UEAwwBLjAe\nFw0yMTA1MjMxNzA0NDZaFw0zMTA1MjMxODA0NDZaMD0xCzAJBgNVBAYTAlVTMQow\nCAYDVQQIDAEuMQowCAYDVQQHDAEuMQowCAYDVQQKDAEuMQowCAYDVQQDDAEuMIIB\nIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxOECV3e8foFfXoqsWZJ+Wwo4\nRQFwOdQvWyH/dGWadbN3G/KMxOxZIcpAL0z/UmpG9hiqOem6OdmQyzdTI6ZfUCkn\nKXEinFnS+ZpA6zetrfVl5f7h3fyJAu8Da2o9eaR8BMn2ATg0QRv6aWpwuMPlIQ2h\ni4Fp0zmp2Xp3aO5wNoY9Thw6/eM1MWk0WIDvkmzEVqKhCpvGCwO0bD+NWMYlhZxM\nw9PTSVpMS5zq0ugvWP9I6vO4ZEm422e6MzdvED4LAD1FAS519I8Y+VKWVP5Wrr/2\nL2ovK6ml7mLQi9Bs0PU9HuYqh1tX8Vj5658dDu6L8t1IBR7gb8mrt2zH5fyqnwID\nAQABoxMwETAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQBtWL/g\nVoclYzrJAeAkcMPewPD5+4O3UfszRvL4EcProx1/XPsvVIjRQ4oBDrCWlmiIxq02\n97JzucooTsyVcJycR4ppoEhW/1XXHyrbBE8nVAcS0x+eQpwJQ9OtW0NM+qAaEjZd\nU/vqeYZwmeSs4aHXhPhifeazrzzaZSVhlHs2rEW1/taxIxCFYT6SipJDLqVlKt6f\nksXtdn8BOcYy1Q6ybXpN+g9D3EnM/X4uHyt3pJ0y14KZHBDd9oYwpx2SLc2SGneG\nZb5zsWluSmrtQS1U8TgT9PrgcTZGwQcurka3yzdb84IkZ0ZSJGn0sZ1TdHWeQB1j\nbix3cnyr6DF7ZD5n\n-----END CERTIFICATE-----\n'

# PubKey
label = 'addr-2ddf60b68546'
handle = '1835230'
private_key_handle = '1835243'
pem = '-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEeLOShJhDaDhwDpwrLA56bLLPlBe22JCe\no5D6eKR3u1P5OE7FTYs32UKuwLXKy45A1PWoqFBt4r36/WqH1qjXwA==\n-----END PUBLIC KEY-----\n'

# Address
address_id = 'addr-2ddf60b68546'
pub_key_pem = '-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEeLOShJhDaDhwDpwrLA56bLLPlBe22JCe\no5D6eKR3u1P5OE7FTYs32UKuwLXKy45A1PWoqFBt4r36/WqH1qjXwA==\n-----END PUBLIC KEY-----\n'
pub_key_handle = '1835230'
address = '13t19fyUcjneGiLCYmVKzH78gMzZDXYyED'

# Bucket
bucket_name = f'{cluster_id}-bucket'

create_key_pair_resp = {
    'KeyFingerprint': KeyFingerprint,
    'KeyMaterial': KeyMaterial,
    'KeyName': KeyName,
    'KeyPairId': KeyPairId
}

describe_clusters_resp = {
    'Clusters':
    [
        {
            'BackupPolicy': 'DEFAULT',
            'BackupRetentionPolicy': {
                'Type': 'DAYS',
                'Value': '90'
            },
            'ClusterId': cluster_id,
            'Hsms': [
                {
                    'AvailabilityZone': 'us-east-2a',
                    'ClusterId': cluster_id,
                    'SubnetId': 'subnet-03fce2972dfdfe9b8',
                    'EniId': 'eni-08ff8a68aae5933c1',
                    'EniIp': '10.0.1.6',
                    'HsmId': hsm_id,
                    'State': 'ACTIVE',
                    'StateMessage': 'HSM created.'
                }
            ], 'HsmType': 'hsm1.medium',
            'SecurityGroup': 'sg-0778d7aa573ae2427',
            'State': 'ACTIVE',
            'SubnetMapping': {
                'us-east-2a': 'subnet-03fce2972dfdfe9b8',
                'us-east-2b': 'subnet-0ba1722070b8dd5c4',
                'us-east-2c': 'subnet-0ec0911a438c139ea'
            },
            'VpcId': '',
            'Certificates':
            {
                'ClusterCsr': pem_csr,
                'HsmCertificate': '',
                'AwsHardwareCertificate': '',
                'ManufacturerHardwareCertificate': '',
                'ClusterCertificate': ''
            },
                'TagList':
                [
                    {
                        'Key': 'Name',
                        'Value': 'cloudhsm_cluster'
                    }
            ]
        }
    ]
}


build_infra_resp = {
    'cluster_id': cluster_id,
    'vpc_id': vpc_id,
    'instance_id': instance_id
}

create_hsm_resp = {
    'Hsm':
    {
        'AvailabilityZone': 'us-east-2a',
        'ClusterId': cluster_id,
        'SubnetId': 'subnet-03fce2972dfdfe9b8',
        'HsmId': hsm_id,
        'State': 'CREATE_IN_PROGRESS'
    }
}

delete_hsm_resp = {'HsmId': hsm_id}

describe_instances_resp = {
    'Reservations':
    [
        {
            'Groups': [],
            'Instances':
            [
                {
                    'AmiLaunchIndex': 0,
                    'ImageId': 'ami-077e31c4939f6a2f3',
                    'InstanceId': instance_id,
                    'InstanceType': 't2.micro',
                    'KeyName': ssh_key_name,
                    'Monitoring':
                    {
                        'State': 'disabled'
                    },
                        'Placement':
                        {
                            'AvailabilityZone': 'us-east-2a',
                            'GroupName': '',
                            'Tenancy': 'default'
                    },
                            'PrivateDnsName': 'ip-10-0-0-190.us-east-2.compute.internal',
                            'PrivateIpAddress': '10.0.0.190',
                            'ProductCodes': [],
                            'PublicDnsName': '',
                            'State':
                            {
                                'Code': 80,
                                'Name': 'stopped'
                    },
                                'StateTransitionReason': 'User initiated (2021-05-29 01:28:54 GMT)',
                                'SubnetId': 'subnet-01e5b0f8e5be3bf01',
                                'VpcId': vpc_id,
                                'Architecture': 'x86_64',
                                'BlockDeviceMappings':
                                [
                                    {
                                        'DeviceName': '/dev/xvda',
                                        'Ebs':
                                        {
                                            'AttachTime': datetime.datetime(2021, 5, 29, 0, 38, 36, tzinfo=tzutc()),
                                            'DeleteOnTermination': True,
                                            'Status': 'attached',
                                            'VolumeId': 'vol-025692bd4913d872c'
                                        }
                                    }
                    ],
                    'ClientToken': 'E8515C74-B4FC-4655-980B-8F4394DF4F16',
                    'EbsOptimized': False,
                    'EnaSupport': True,
                    'Hypervisor': 'xen',
                    'NetworkInterfaces':
                    [
                        {
                            'Attachment':
                            {
                                'AttachTime': datetime.datetime(2021, 5, 29, 0, 38, 35, tzinfo=tzutc()),
                                'AttachmentId': 'eni-attach-0c4c6ca6d1ebf5835',
                                'DeleteOnTermination': True,
                                'DeviceIndex': 0,
                                'Status': 'attached',
                                'NetworkCardIndex': 0
                            },
                            'Description': '',
                            'Groups':
                            [
                                {
                                    'GroupName': 'cloudhsm-cluster-2f2ynawbwz5-sg',
                                    'GroupId': 'sg-0778d7aa573ae2427'
                                },
                                {
                                    'GroupName': 'default',
                                    'GroupId': 'sg-0259648b4083884a5'
                                }
                            ],
                            'Ipv6Addresses': [],
                            'MacAddress': '02:49:e2:cf:b8:f0',
                            'NetworkInterfaceId': 'eni-043e068e735e6279a',
                            'OwnerId': '945793393231',
                            'PrivateDnsName': 'ip-10-0-0-190.us-east-2.compute.internal',
                            'PrivateIpAddress': '10.0.0.190',
                            'PrivateIpAddresses':
                            [
                                {
                                    'Primary': True,
                                    'PrivateDnsName': 'ip-10-0-0-190.us-east-2.compute.internal',
                                    'PrivateIpAddress': '10.0.0.190'
                                }
                            ],
                            'SourceDestCheck': True,
                            'Status': 'in-use',
                            'SubnetId': 'subnet-01e5b0f8e5be3bf01',
                            'VpcId': 'vpc-062a43279040c9896',
                            'InterfaceType': 'interface'
                        }
                    ],
                    'RootDeviceName': '/dev/xvda',
                    'RootDeviceType': 'ebs',
                    'SecurityGroups':
                    [
                        {
                            'GroupName': 'cloudhsm-cluster-2f2ynawbwz5-sg',
                            'GroupId': 'sg-0778d7aa573ae2427'
                        },
                        {
                            'GroupName': 'default',
                            'GroupId': 'sg-0259648b4083884a5'
                        }
                    ],
                    'SourceDestCheck': True,
                    'StateReason':
                    {
                        'Code': 'Client.UserInitiatedShutdown',
                        'Message': 'Client.UserInitiatedShutdown: User initiated shutdown'
                    },
                    'VirtualizationType': 'hvm',
                    'CpuOptions':
                    {
                        'CoreCount': 1,
                        'ThreadsPerCore': 1
                    },
                    'CapacityReservationSpecification':
                    {
                        'CapacityReservationPreference': 'open'
                    },
                    'HibernationOptions':
                    {
                        'Configured': False
                    },
                    'MetadataOptions':
                    {
                        'State': 'applied',
                        'HttpTokens': 'optional',
                        'HttpPutResponseHopLimit': 1,
                        'HttpEndpoint': 'enabled'
                    },
                    'EnclaveOptions':
                    {
                        'Enabled': False
                    }
                }
            ],
            'OwnerId': '945793393231',
            'ReservationId': 'r-0a28e490b4e1ccd0e'
        }
    ],
}

gen_ecc_key_pair_resp = {
    'data':
    {
        'label': label,
        'handle': handle,
        'private_key_handle': private_key_handle,
        'pem': pem
    },
    'status_code': 200
}

list_buckets_false_resp = {'Buckets': [], 'Owner': {
    'ID': '6db94838fea6a8498fd800ac2ea3eea867a95870a8e8b263770a751e580c166e'}}

create_bucket_resp = {
    'Location': f'http: //{cluster_id}-bucket.s3.amazonaws.com /'}

list_buckets_true_resp = {
    'Buckets':
    [
        {
            'Name': 'cluster-lbtkdldygfh-bucket',
                    'CreationDate': datetime.datetime(2021, 6, 4, 15, 31, 27, tzinfo=tzutc())
        }
    ],
    'Owner':
    {
        'ID': '6db94838fea6a8498fd800ac2ea3eea867a95870a8e8b263770a751e580c166e'
    }
}


list_objects_resp = {
    'Contents':
    [
        {
            'Key': 'addr-2ddf60b68546',
            'LastModified': datetime.datetime(2021, 6, 4, 16, 52, 31, tzinfo=tzutc()),
            'ETag': '"bde5d79445637dfa506e3de03d137c32"',
            'Size': 308,
            'StorageClass':
            'STANDARD',
            'Owner':
            {
                'ID': '6db94838fea6a8498fd800ac2ea3eea867a95870a8e8b263770a751e580c166e'
            }
        }
    ],
    'Name': 'cluster-lbtkdldygfh-bucket',
    'Prefix': '',
    'MaxKeys': 1000,
    'EncodingType': 'url'
}

obj_data = {
    'pub_key_handle': pub_key_handle,
    'private_key_handle': private_key_handle,
    'pub_key_pem': pub_key_pem,
    'address': address
}

body_encoded = json.dumps(obj_data).encode('UTF-8')

body = StreamingBody(io.BytesIO(body_encoded), len(body_encoded))

get_object_resp = {
    'AcceptRanges': 'bytes',
    'LastModified': datetime.datetime(2021, 6, 4, 16, 52, 31, tzinfo=tzutc()),
    'ContentLength': 308,
    'ETag': '"bde5d79445637dfa506e3de03d137c32"',
            'ContentType': 'binary/octet-stream',
            'Metadata': {},
            'Body': body
}


put_object_resp = {
    'ResponseMetadata':
    {
        'RequestId': 'XC168DY8X89V84N7',
        'HostId': '05BOjg6ZL25KfjxZOCbHso7oXzgCAgkHuOdt+PcV1MQmPM/QmaXQPIcJg3+loo8o4ein4P7GmAI=',
        'HTTPStatusCode': 200,
        'HTTPHeaders':
        {
            'x-amz-id-2': '05BOjg6ZL25KfjxZOCbHso7oXzgCAgkHuOdt+PcV1MQmPM/QmaXQPIcJg3+loo8o4ein4P7GmAI=',
            'x-amz-request-id': 'XC168DY8X89V84N7',
            'date': 'Fri, 04 Jun 2021 19:55:51 GMT',
            'etag': '"bde5d79445637dfa506e3de03d137c32"',
            'server': 'AmazonS3',
            'content-length': '0'
        },
            'RetryAttempts': 0
    },
    'ETag': '"bde5d79445637dfa506e3de03d137c32"'
}

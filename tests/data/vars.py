import boto3
import botocore.session
import os

altmirai_access_key_id = 'AKIA3PBN5ZODNJA7B4FO'
altmirai_secret_access_key = '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'

aws_region = 'us-east-2'

resource = boto3.resource('ec2')
ec2 = botocore.session.get_session().create_client('ec2')
cloudhsmv2 = botocore.session.get_session().create_client('cloudhsmv2')
s3 = botocore.session.get_session().create_client('s3', region_name=aws_region)

cluster_id = 'cluster-lbtkdldygfh'
test_base_path = '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/tests/test_files'
test_cluster_path = os.path.join(test_base_path, cluster_id)
production_path = '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/production_files'

instance_id = 'i-051bdb2ae099024a5'
vpc_id = 'vpc-06f745fe81ec3c1a8'

credentials_file_path = os.path.join(
    test_cluster_path,
    'credentials.json'
)

hsm_id = 'hsm-u25cdzfj56s'
eni_ip = '10.1.0.9'

ssh_key_name = 'Piggy_SSH_Key_0194afd1'
ssh_key_file_path = os.path.join(test_cluster_path, f'{ssh_key_name}.pem')

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
label = 'addr-d78121d8375a'
handle = '2097415'
private_key_handle = '2097416'
pem = '-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE8B06BQfTPLFC3iuApDKK3218TZd+89YY\n8LXmQw/SWaLyZ5K2fiGPFeibYsA+vOorg2KqisQExyHi6nqJDKyFoA==\n-----END PUBLIC KEY-----\n'

# Address
address_id = 'addr-d78121d8375a'
pub_key_pem = '-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE8B06BQfTPLFC3iuApDKK3218TZd+89YY\n8LXmQw/SWaLyZ5K2fiGPFeibYsA+vOorg2KqisQExyHi6nqJDKyFoA==\n-----END PUBLIC KEY-----\n'
pub_key_handle = '2097415'
address = '1CpuPq63tVhL5vhAhL2GLFYkMZT7DBrv9J'
confirmed_balance = 190000
txrefs = [
    {
        'tx_hash': '995e70e4c78fe60d26c5f6904204b2d4e819aa63686a10eeca97cb17b76151fa',
        'block_height': 687813,
        'tx_input_n': -1,
        'tx_output_n': 0,
        'value': 90000,
        'ref_balance': 190000,
        'spent': False,
        'confirmations': 145,
        'confirmed': '2021-06-16 14:24:04+00:00',
        'double_spend': False
    },
    {
        'tx_hash': '429eca7b6cc576a2aa9acefc05bf8c21c92a4aeceae0d03d1d45aff964e6e50b',
        'block_height': 687809,
        'tx_input_n': -1,
        'tx_output_n': 1,
        'value': 100000,
        'ref_balance': 100000,
        'spent': False,
        'confirmations': 149,
        'confirmed': '2021-06-16 13:41:40+00:00',
        'double_spend': False
    }
]
spent = False

# TX
recipient = '1Pzc72SMoaxWZhkAqZFFjGRKnCHMBLTWs8'
fee = 15000
value = 175000

# TX Output Script
outputs = [bytearray(
    b'\x98\xab\x02\x00\x00\x00\x00\x00\x19v\xa9\x14\xfc7\xc7\xc2\x0c\x05\xa0(\x00d\xe8 \xe0\x92\xd9\xcf\x99\xe9\xb3&\x88\xac'
)
]

# Unsigned Tx
messages = [
    {
        'message': bytearray(b'\x01\x00\x00\x00\x02\xfaQa\xb7\x17\xcb\x97\xca\xee\x10jhc\xaa\x19\xe8\xd4\xb2\x04B\x90\xf6\xc5&\r\xe6\x8f\xc7\xe4p^\x99\x00\x00\x00\x00\x19v\xa9\x14\x81\xb8\xabxOc\x97\xb1\xf7:\xfe\x0b\xdaL!\xf3S,\x0bg\x88\xac\xff\xff\xff\xff\x0b\xe5\xe6d\xf9\xafE\x1d=\xd0\xe0\xea\xecJ*\xc9!\x8c\xbf\x05\xfc\xce\x9a\xaa\xa2v\xc5l{\xca\x9eB\x01\x00\x00\x00\x00\xff\xff\xff\xff\x01\x98\xab\x02\x00\x00\x00\x00\x00\x19v\xa9\x14\xfc7\xc7\xc2\x0c\x05\xa0(\x00d\xe8 \xe0\x92\xd9\xcf\x99\xe9\xb3&\x88\xac\x00\x00\x00\x00\x01\x00\x00\x00'),
        'tx_input': {
            'output_no': 0,
            'outpoint_index': b'\x00\x00\x00\x00',
            'outpoint_hash': bytearray(b'\xfaQa\xb7\x17\xcb\x97\xca\xee\x10jhc\xaa\x19\xe8\xd4\xb2\x04B\x90\xf6\xc5&\r\xe6\x8f\xc7\xe4p^\x99')
        }
    },
    {
        'message': bytearray(b'\x01\x00\x00\x00\x02\xfaQa\xb7\x17\xcb\x97\xca\xee\x10jhc\xaa\x19\xe8\xd4\xb2\x04B\x90\xf6\xc5&\r\xe6\x8f\xc7\xe4p^\x99\x00\x00\x00\x00\x00\xff\xff\xff\xff\x0b\xe5\xe6d\xf9\xafE\x1d=\xd0\xe0\xea\xecJ*\xc9!\x8c\xbf\x05\xfc\xce\x9a\xaa\xa2v\xc5l{\xca\x9eB\x01\x00\x00\x00\x19v\xa9\x14\x81\xb8\xabxOc\x97\xb1\xf7:\xfe\x0b\xdaL!\xf3S,\x0bg\x88\xac\xff\xff\xff\xff\x01\x98\xab\x02\x00\x00\x00\x00\x00\x19v\xa9\x14\xfc7\xc7\xc2\x0c\x05\xa0(\x00d\xe8 \xe0\x92\xd9\xcf\x99\xe9\xb3&\x88\xac\x00\x00\x00\x00\x01\x00\x00\x00'),
        'tx_input': {
            'output_no': 1,
            'outpoint_index': b'\x01\x00\x00\x00',
            'outpoint_hash': bytearray(b'\x0b\xe5\xe6d\xf9\xafE\x1d=\xd0\xe0\xea\xecJ*\xc9!\x8c\xbf\x05\xfc\xce\x9a\xaa\xa2v\xc5l{\xca\x9eB')
        }
    }
]
to_sign = [
    b'\xe9=8\xc2ay\x1b\x85\xfb\xec\xaf\xb5 \xd6\xc1\xe49\xdf&{W\x94\xca\xef\x9f\xbfj\x97\xf9\x90\x89\xdf',
    b'\xa7\xa5\xff\xc9\xf6\x8c\x1b\nS0\x17\xa5\x05\xb1\xe1\x9d/\xdc\x9f\x8dQ\xdd\xb5j\x11L\xe2\xc2\xac\xb7\xb6@'
]
version = b'\x01\x00\x00\x00'
tx_inputs = [
    {
        'output_no': 0,
        'outpoint_index': b'\x00\x00\x00\x00',
        'outpoint_hash': bytearray(b'\xfaQa\xb7\x17\xcb\x97\xca\xee\x10jhc\xaa\x19\xe8\xd4\xb2\x04B\x90\xf6\xc5&\r\xe6\x8f\xc7\xe4p^\x99')
    },
    {
        'output_no': 1,
        'outpoint_index': b'\x01\x00\x00\x00',
        'outpoint_hash': bytearray(b'\x0b\xe5\xe6d\xf9\xafE\x1d=\xd0\xe0\xea\xecJ*\xc9!\x8c\xbf\x05\xfc\xce\x9a\xaa\xa2v\xc5l{\xca\x9eB')
    }
]
tx_in_count = b'\x02'
placeholder = b'\x00'
sequence = b'\xff\xff\xff\xff'
tx_out_count = b'\x01'
lock_time = b'\x00\x00\x00\x00'
hash_code = b'\x01\x00\x00\x00'

# Signed Tx
signatures = [
    b"0F\x02!\x00\xfa.*\xb0\xb0\x90*\xe2\xb5(\x17\x0e\x18OI_\xf1\x1d\xf3M(\x8c\x18\x1a\x8bK\xa2\xfc\xc4\x16r\x1b\x02!\x00\xf0o\xaf?\xe7\xee\x90\xb4=|Atm&\xf1\xa8\x08'\x1cj(i\xa3\x94\xdd)\x86c\xc7o\xaf\xbe",
    b'0E\x02 D[\xcf\xb8\x86\x0cSf\xbbr\xe6\xbe\xe3\x90\x83\xd7\xa3w\x98\xf6?\xef\x8e\xca>/\xff\x87\xbd\xac\xce\xd1\x02!\x00\x8b\xd9d\x8d\r\xb5V\xd4\xa7f\xf2\x0b\xb1\x12\x909\x85\x1d\xcdf\x90\x02\x18X7\x9a\xb0\nB\x08\xf4\xfa'
]
tx_hex = '0100000002fa5161b717cb97caee106a6863aa19e8d4b2044290f6c5260de68fc7e4705e99000000008b483045022100fa2e2ab0b0902ae2b528170e184f495ff11df34d288c181a8b4ba2fcc416721b02200f9050c018116f4bc283be8b92d90e56b287c07c86defca6e2a8d82908c69183014104f01d3a0507d33cb142de2b80a4328adf6d7c4d977ef3d618f0b5e6430fd259a2f26792b67e218f15e89b62c03ebcea2b8362aa8ac404c721e2ea7a890cac85a0ffffffff0be5e664f9af451d3dd0e0eaec4a2ac9218cbf05fcce9aaaa276c56c7bca9e42010000008a4730440220445bcfb8860c5366bb72e6bee39083d7a37798f63fef8eca3e2fff87bdacced1022074269b72f24aa92b58990df44eed6fc535910f801f4687e38837ae828e2d4c47014104f01d3a0507d33cb142de2b80a4328adf6d7c4d977ef3d618f0b5e6430fd259a2f26792b67e218f15e89b62c03ebcea2b8362aa8ac404c721e2ea7a890cac85a0ffffffff0198ab0200000000001976a914fc37c7c20c05a0280064e820e092d9cf99e9b32688ac00000000'

# Bucket
bucket_name = f'{cluster_id}-bucket'

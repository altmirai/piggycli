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
cluster.hsms = [
    {
        'AvailabilityZone': 'us-east-2a',
        'ClusterId': data.cluster_id,
        'SubnetId': 'subnet-03fce2972dfdfe9b8',
                    'EniId': 'eni-08ff8a68aae5933c1',
                    'EniIp': data.eni_ip,
                    'HsmId': data.hsm_id,
                    'State': 'ACTIVE',
                    'StateMessage': 'HSM created.'
    }
]
cluster.initialize.return_value = True
cluster.activate.return_value = True

instance = Mock()
instance.id = data.instance_id
instance.public_ip_address = data.public_ip_address
instance.state = 'running'
instance.ssh_key_name == data.ssh_key_name


hsm = Mock()
hsm.id = data.hsm_id
hsm.cluster_id = data.cluster_id

certs = Mock()
certs.pem_private_key = data.pem_private_key
certs.pem_csr = data.pem_csr
certs.pem_hsm_cert = data.pem_hsm_cert
certs.pem_ca_cert = data.pem_ca_cert

x509 = Mock()
x509.private_key.return_value = True
# b'-----BEGIN RSA PRIVATE KEY-----\nProc-Type: 4,ENCRYPTED\nDEK-Info: AES-256-CBC,6F7135B1FF40772431A52344F2C28F3E\n\n17swNOMYJtX7XSMnL9C6MPmIaI34peR4CPUt0IWaiu5AfuHeGrho2PhaljlKX/Lt\nw4ykD/zrrKk88BrhTTPhArJNOporxC8d2BeyXtiIXqz4+yn256Ox4zfzkAdGq2xq\nRRzNHZot417yqUcIUSI+H39WkHVunhpNWJixMFKp5yhTf1JUHXCNOPNr4M/aALFD\n9U1pJ4t1H0umrNdHKI7lWat5+lnfXPe9GrQ+NYYobM6MX6uM7Mb9ggzN0234rOQM\nhLYdMGUCvXrWUoVHQ7mRR/DBa4S2ptAbyHsQZCOLLvnfQE+lCpT8SxkUf3xyeRGC\njGqHWANEHbdW7LKNS9aSbjoM5fXx9ToJJJiFAo4RuFVpTufVh8zhPscx1DjvVXLQ\nPo1WZrZusELmhzvJOgJQkNvrVnfGmHtB6CuzHUyXAriN1VUekWlNYi3gP5fC5MjO\n+bISUXiGLHi0DYe+x+0PHquI/u5Gugeh/k+q7pvbTnZ/r9so+P4aW2q1IDloFYXv\nDVO3VGdSef3mp1k4B49257K5Vri1XYjLXAkbQyuVFGWphQ4bSHCscZhAevpzCDVk\nPrD0R+egohy/ErZllbp7+rc+VpHMBXpi5LEYAetpdR5URrgZAP5L2WWS4/WtsoAb\nnApoqMuq53QaOjjWx2wTtyU1lOGoT5pSS4/c1UKxV/72Dpbu96e8MBhjwwmIZiGW\nD5fjHJzEDZxtA/YFS1UHxb8hPsMRJkb67dR1fOSDXBWLZdi0MQ1que60bXV4+a8W\nJTKzpf8yOaNkI98QqGcvbfZWcgQ/sMVduOrx1VsndFqXiJ4M5heCAU+3gKAaX9HG\nkoYtTnp+LbshZNawdyW1MtdeeP8zrVfAx+WrYcI8/XL7+tge4n6VkVoqxD6IJX3a\nZ6EPY/J/IBSQsYIeQe4QDrjR1ztbNBS4KMBlJofM3IlPY5ee9L61QBwCW9zM9FNI\n8s54O2D3nGgc5fGteB5Ze4qGDFshPKXJU5uFcSZ19202NhuPTeWkuCFXMSz41eRL\n3kog6OW5q3UNPgMAb9nmuQzDt7fALY9fzl3n6CV/lli68oP8ji8iqqTvP5tjkgQa\nVC5IY97qs0JoeEnORSMo0SdnL/4YK5eni5pZxR1pvdXV0t4Vqap0f2SEi0yL8HxA\nLtmCTYdD9e/IEFcPjoFp/M5NcPUP81S8gJUwLWo9eI2Cpe7tZBrdWHQ6Z8Kc3mQQ\nflT5wXps/H9CmVkDFIu/VuOLxHxVzl7L20a8zkZDRhqnij/IqG+UM27dZ/Rc48Vu\nG7S4um6eahANe7r2n4gDApQBlziUApR5PIeZUFpKELTNKJ4BY1Ttsmt+y3EDU8Uk\nBt38zSYs251WmKjuRwR99dny7p+jjxBdJSW5xpoSv7/DdH9UaF2PhAXetdeYRWnt\nu2lshQzrZBruQpcSCbFS3FvmlNlKc4zoSt9lNp+NgGLZzbLciSQhF5+nyz2k+K26\nZyTbjiaWhK+AfxtgWG84iuJI7DtcuP1MRuud0aV9PZV/KZ8X1AnqDsxCUsUwjtAj\nM5PTCWRL0tSkQKRue8iueN498DdzlK+QqkRGdN3j/YTmh8KZzLvjiUxAUPXByjaV\n-----END RSA PRIVATE KEY-----\n'
x509.pem_csr = '-----BEGIN CERTIFICATE REQUEST-----\nMIIC0TCCAbkCAQAwgYsxRDAJBgNVBAYTAlVTMAkGA1UECAwCQ0EwDQYDVQQKDAZD\nYXZpdW0wDQYDVQQLDAZOM0ZJUFMwDgYDVQQHDAdTYW5Kb3NlMUMwQQYDVQQDDDpI\nU006QjRGMUU4QjY3OTY3NTg2M0Y4REIzMjExMTM2NEIzOlBBUlROOjEzLCBmb3Ig\nRklQUyBtb2RlMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvDY9IZlR\nThUQ2Jfc+JWPC15WqZbMRKiEba+FICcwno+izaDza+rzpqtaU0Q5UVYGOe4vEtVj\nxsj3hdhXc2rK53vhw4EdmKojPzAy3F/TJGzSvzIlPUCdWLtbKlNEkg/VGu1YcsMV\nvQvyGFSusj8idWT4DvsZxPuEwiXE4qEPmyB1uo2lKIYWfulP9QrRdvnrBF/zBmXO\nblg3zHf1KQ8bYWW8Lc/DGcRnRvPBfDvYNS6DJPrMiM+QeqhM5Iegu7OlTOTkV72d\nmaMqTuuWOGrb6LCDr7hWGfjAE3517Jt2ia2bB8YE5Wda4mUBEmpVl5Kho547S6Sx\nMiChX3U3VCHbVwIDAQABoAAwDQYJKoZIhvcNAQELBQADggEBAKqEhDqVClGRES2C\nIwqKxPVYo5lbynEZ94qSeKzI9rgoW3kPVyro1vBxAzMwDSJd1TXmw2fJAOY7Zdiw\n+j0SMZCb81ehVNa8VRUsOrU6phC72jqUSFSWpRkCDxc9inIdUfBpqIQxsd0JpYB7\nzvyuKILMNDI3Ys7S4i1ErHv8IyDUdmVjP+qRaEAhecBEt5GVZPDg/vjEsS83hqf4\n7EZ9S9noDgnoa79W1ovFr8wW8EZ5Spi50D5hsFCMy4a4rErwneAATEm2MmtLfIy7\nCWTUET6SZN2Ncn/oM1ulVYofYTctmpiAGMMjB9joA6nW0I2QfhaSOTugU+NmwnC0\nOo+qHwM=\n-----END CERTIFICATE REQUEST-----\n'
x509.pem_hsm_cert = b'-----BEGIN CERTIFICATE-----\nMIIDVTCCAj2gAwIBAgIUGVpAlXDcW6bULCcyAPeUMgY2Hf4wDQYJKoZIhvcNAQEL\nBQAwPTELMAkGA1UEBhMCVVMxCjAIBgNVBAgMAS4xCjAIBgNVBAcMAS4xCjAIBgNV\nBAoMAS4xCjAIBgNVBAMMAS4wHhcNMjEwNTIzMTcwNDQ2WhcNMzEwNTIzMTgwNDQ2\nWjCBizFEMAkGA1UEBhMCVVMwCQYDVQQIDAJDQTANBgNVBAoMBkNhdml1bTANBgNV\nBAsMBk4zRklQUzAOBgNVBAcMB1Nhbkpvc2UxQzBBBgNVBAMMOkhTTTpCNEYxRThC\nNjc5Njc1ODYzRjhEQjMyMTExMzY0QjM6UEFSVE46MTMsIGZvciBGSVBTIG1vZGUw\nggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC8Nj0hmVFOFRDYl9z4lY8L\nXlaplsxEqIRtr4UgJzCej6LNoPNr6vOmq1pTRDlRVgY57i8S1WPGyPeF2Fdzasrn\ne+HDgR2YqiM/MDLcX9MkbNK/MiU9QJ1Yu1sqU0SSD9Ua7VhywxW9C/IYVK6yPyJ1\nZPgO+xnE+4TCJcTioQ+bIHW6jaUohhZ+6U/1CtF2+esEX/MGZc5uWDfMd/UpDxth\nZbwtz8MZxGdG88F8O9g1LoMk+syIz5B6qEzkh6C7s6VM5ORXvZ2ZoypO65Y4atvo\nsIOvuFYZ+MATfnXsm3aJrZsHxgTlZ1riZQESalWXkqGjnjtLpLEyIKFfdTdUIdtX\nAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAKAogyiwCBLFzu7k0i42NQ4AZbYkQg1k\nS6e7N3oOVwG/BEaeyt47Uc99g0cSnhtvet/Mlt4GURPc66bZY1EoHQ0N/UFF3BCB\nk4Gumu6BToIogAjiFmKLDVgeWrCtJlHxdYLe6lyiIEbGuuMBOZ6lmLxRS8Fj6/as\nblxkvdbrVjKutFJPwUI46gmGvaSP+x1lV3KyJcRgG2Q4Sw0hctMFm88jjZZ9mK5F\n3am64/bU9jIa4edirjv5fXhgQcxSlLMA1ltQtgQBypnHVUlgCAG28n8YLjoS2lQO\nbiwa/jYdJFKwyZ08Mv23ixNeACb8PNT61iHsqa6Xq6igYUwaqwIFH2Y=\n-----END CERTIFICATE-----\n'
x509.pem_ca_cert = b'-----BEGIN CERTIFICATE-----\nMIIDCDCCAfCgAwIBAgIBATANBgkqhkiG9w0BAQsFADA9MQswCQYDVQQGEwJVUzEK\nMAgGA1UECAwBLjEKMAgGA1UEBwwBLjEKMAgGA1UECgwBLjEKMAgGA1UEAwwBLjAe\nFw0yMTA1MjMxNzA0NDZaFw0zMTA1MjMxODA0NDZaMD0xCzAJBgNVBAYTAlVTMQow\nCAYDVQQIDAEuMQowCAYDVQQHDAEuMQowCAYDVQQKDAEuMQowCAYDVQQDDAEuMIIB\nIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxOECV3e8foFfXoqsWZJ+Wwo4\nRQFwOdQvWyH/dGWadbN3G/KMxOxZIcpAL0z/UmpG9hiqOem6OdmQyzdTI6ZfUCkn\nKXEinFnS+ZpA6zetrfVl5f7h3fyJAu8Da2o9eaR8BMn2ATg0QRv6aWpwuMPlIQ2h\ni4Fp0zmp2Xp3aO5wNoY9Thw6/eM1MWk0WIDvkmzEVqKhCpvGCwO0bD+NWMYlhZxM\nw9PTSVpMS5zq0ugvWP9I6vO4ZEm422e6MzdvED4LAD1FAS519I8Y+VKWVP5Wrr/2\nL2ovK6ml7mLQi9Bs0PU9HuYqh1tX8Vj5658dDu6L8t1IBR7gb8mrt2zH5fyqnwID\nAQABoxMwETAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQBtWL/g\nVoclYzrJAeAkcMPewPD5+4O3UfszRvL4EcProx1/XPsvVIjRQ4oBDrCWlmiIxq02\n97JzucooTsyVcJycR4ppoEhW/1XXHyrbBE8nVAcS0x+eQpwJQ9OtW0NM+qAaEjZd\nU/vqeYZwmeSs4aHXhPhifeazrzzaZSVhlHs2rEW1/taxIxCFYT6SipJDLqVlKt6f\nksXtdn8BOcYy1Q6ybXpN+g9D3EnM/X4uHyt3pJ0y14KZHBDd9oYwpx2SLc2SGneG\nZb5zsWluSmrtQS1U8TgT9PrgcTZGwQcurka3yzdb84IkZ0ZSJGn0sZ1TdHWeQB1j\nbix3cnyr6DF7ZD5n\n-----END CERTIFICATE-----\n'

pub_key = Mock()
pub_key.label = data.label
pub_key.handle = data.handle
pub_key.pem = data.pem
pub_key.private_key_handle = data.private_key_handle

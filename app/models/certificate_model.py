import app.utilities.x509_certificates as x509
import app.utilities.ssh as ssh
import os


class Certs:

    def __init__(self, pem_csr, passphrase, file_path, cluster_id):
        self.pem_csr = pem_csr
        self.passphrase = passphrase
        self.file_path = file_path
        self.cluster_id = cluster_id

        self._csr = self.get_csr()
        self._key = x509.private_key()
        self._ca_cert = x509.ca_cert(self._key)
        self._hsm_cert = x509.hsm_cert(self._ca_cert, self._csr, self._key)
        self.valid = x509.validate_hsm_cert(self._hsm_cert, self._ca_cert)
        self.pem_private_key = x509.pem_private_key(self._key, self.passphrase)
        self.pem_ca_cert = x509.pem_ca_cert(self._ca_cert)
        self.pem_hsm_cert = x509.pem_hsm_cert(self._hsm_cert)

    def get_csr(self):
        if type(self.pem_csr) is bytes:
            return x509.csr(self.pem_csr.decode('utf-8'))
        else:
            return x509.csr(self.pem_csr)

    def upload_customer_ca_cert(self, ec2_instance):
        ssh.upload_and_move_customer_ca_cert(
            ip_address=ec2_instance.public_ip_address,
            ssh_key_file=ec2_instance.ssh_key_file,
            file_path=self.file_path)

    def write_to_files(self):
        # TODO: Needs lots of work!
        path = f'{self.file_path}'
        cluster_id = self.cluster_id

        with open(f"{path}/customerCA.key", 'wb') as file:
            file.write(self.pem_private_key)

        with open(f"{path}/{self.cluster_id}_ClusterCsr.csr", 'wb') as file:
            csr = self.pem_csr if type(
                self.pem_csr) is bytes else self.pem_csr.encode('utf-8')
            file.write(csr)

        with open(f"{path}/{self.cluster_id}_CustomerHsmCertificate.crt", 'wb') as file:
            file.write(self.pem_hsm_cert)

        with open(f"{path}/customerCA.crt", 'wb') as file:
            file.write(self.pem_ca_cert)

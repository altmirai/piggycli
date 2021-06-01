import app.utilities.x509_certificates as x509
import app.utilities.ssh as ssh
import os


class Certs:

    def __init__(self, pem_csr, passphrase):
        breakpoint()
        self.pem_csr = pem_csr
        self.passphrase = passphrase

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

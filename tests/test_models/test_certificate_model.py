from app.models.certificate_model import Certs
import tests.data as data


def test_certs():
    certs = Certs(pem_csr=data.pem_csr,
                  passphrase=data.customer_ca_key_password)
    assert certs.valid

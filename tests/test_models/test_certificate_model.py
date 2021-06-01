from app.models.certificate_model import Certs
from unittest.mock import patch
from tests.mocks import x509
import tests.data as data


@patch('app.models.certificate_model.x509', return_value=x509, autospec=True)
def test_certs(mock_x509):
    certs = Certs(pem_csr=data.pem_csr,
                  passphrase=data.customer_ca_key_password)
    breakpoint()
    assert certs.pem_ca_cert == data.pem_ca_cert
    assert certs.pem_hsm_cert == data.pem_hsm_cert

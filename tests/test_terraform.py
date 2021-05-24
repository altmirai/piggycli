from app.utilities.terraform import Tf
from tests.test_data import CredentialsData

t = CredentialsData()


# def test_validate():
#     tf = Tf(region=t.aws_region, ssh_key_name=t.ssh_key_name)
#     resp = tf.validate()

#     assert resp

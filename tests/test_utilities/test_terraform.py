from app.utilities.terraform import Tf
from unittest import mock
from unittest.mock import Mock

test_region = 'us-east-2'
test_ssh_key_name = 'SSH_Key_1'


# def test_validate():
#     tf = Tf(region=test_region, ssh_key_name=test_ssh_key_name)
#     resp = tf.validate()

#     assert resp


class SubprocessResp:
    def __init__(self):
        self.returncode = 0


resp = SubprocessResp()


@mock.patch('subprocess.run', return_value=resp, autospec=True)
def test_build(mock_run):
    tf = Tf(region=test_region, ssh_key_name=test_ssh_key_name)
    resp = tf.build()
    assert tf.build()

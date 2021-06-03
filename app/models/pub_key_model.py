import app.utilities.ssh as ssh


class PubKey:

    def __init__(self, label, handle, private_key_handle, public_key_pem_file_name):
        self.label = label
        self.handle = handle
        self.private_key_handle = private_key_handle
        self.public_key_pem_file_name = public_key_pem_file_name

    @classmethod
    def create(cls, ip_address, ssh_key_file, eni_ip, crypto_user_username, crypto_user_password, label):

        resp = ssh.gen_ecc_key_pair(
            ip_address=ip_address,
            ssh_key_file=ssh_key_file,
            eni_ip=eni_ip,
            crypto_user_username=crypto_user_username,
            crypto_user_password=crypto_user_password,
            key_label=label
        )
        if resp['status_code'] != 200:
            breakpoint()

        return cls(
            label=resp['data']['label'],
            handle=resp['data']['public_key_handle'],
            private_key_handle=resp['data']['private_key_handle'],
            public_key_pem_file_name=resp['data']['public_key_pem_file_name']
        )

    def download_pem_file(self, ip_address, ssh_key_file, local_path):
        resp = ssh.download_file_from_instance(
            ip_address=ip_address,
            ssh_key_file=ssh_key_file,
            file=self.public_key_pem_file_name,
            local_path=local_path
        )

    def read(self):
        return

    def update(self):
        return

    def delete(self):
        return

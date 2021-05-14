import json


class Config:

    def __init__(self):
        pass

    def create(self, path, aws_access_key, **kwargs):
        config_data = {
            'aws_access_key': aws_access_key,
            'ssh_key_name': kwargs.get('ssh_key_name'),
            'ssh_key_value': kwargs.get('ssh_key_value'),
            'customer_ca_key': kwargs.get('customer_ca_key'),
            'customer_ca_crt': kwargs.get('customer_ca_crt'),
            'cluster_csr': kwargs.get('cluster_csr'),
            'customer_hsm_crt': kwargs.get('customer_hsm_crt')
        }

        breakpoint()
        with open(f'{path}/piggy_config.json', 'w') as file:
            file.write(json.dumps(config_data))

        return

    def read(self, config_file):

        return

    def update(self, config_file):

        return

    def destroy(self, config_file):

        return

import json


class ConfigData:
    def __init__(self, **kwargs):
        self.aws_access_key_id = kwargs.get('aws_access_key_id')
        self.aws_secret_access_key = kwargs.get('aws_secret_access_key')
        self.ssh_key_name = kwargs.get('ssh_key_name')
        self.ssh_key_material = kwargs.get('ssh_key_material')
        self.customer_ca_key = kwargs.get('customer_ca_key')
        self.customer_ca_crt = kwargs.get('customer_ca_crt')
        self.cluster_csr = kwargs.get('cluster_csr')
        self.customer_hsm_crt = kwargs.get('customer_hsm_crt')


class Config:

    def __init__(self, path):
        self.path = path
        pass

    def create(self, aws_access_key_id, aws_secret_access_key, **kwargs):
        data = ConfigData(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            **kwargs
        )
        with open(f'{self.path}/piggy_config.json', 'w') as file:
            file.write(json.dumps(data.__dict__))

        for k, v in data.__dict__.items():
            setattr(self, k, v)
        return

    def read(self):
        with open(f'{self.path}/piggy_config.json', 'r') as file:
            config_data = json.loads(file.read())
        for k, v in config_data.items():
            setattr(self, k, v)
        return

    def update(self, **kwargs):
        with open(f'{self.path}/piggy_config.json', 'r') as file:
            data_json = file.read()

        data = json.loads(data_json)
        config = ConfigData(**data)
        for k, v in kwargs.items():
            setattr(config, k, v)

        with open(f'{self.path}/piggy_config.json', 'w') as file:
            file.write(json.dumps(config.__dict__))

        for k, v in config.__dict__.items():
            setattr(self, k, v)

        return

    def destroy(self, config_file):
        return


class CredentialsData:
    def __init__(self):
        self.path = '/Volumes/CloudHSM'
        self.aws_region = 'us-east-2'
        self.ssh_key_name = 'Piggy_SSH_Key_cf865bae'
        self.cluster_id = 'cluster-lbtkdldygfh'
        self.instance_id = '051bdb2ae099024a5'
        self.aws_access_key_id = 'AKIA5YNNN4JH6JDQF5XH'
        self.aws_secret_access_key = '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'
        self.customer_ca_key_password = 'password1'
        self.crypto_officer_password = 'password1'
        self.crypto_user_username = 'cryptouser'
        self.crypto_user_password = 'password1'

    @property
    def credentials_kwargs(self):
        data = self.__dict__
        arguments = {}
        for k, v in data.items():
            if k != 'path':
                arguments[k] = v
        return arguments

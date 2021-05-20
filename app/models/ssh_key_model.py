import uuid


class SSHKey:

    def __init__(self, name, id, material, fingerprint):
        self.name = name
        self.id = id
        self.material = material
        self.fingerpring = fingerprint

    @classmethod
    def create(cls, client):

        name = f'Piggy_SSH_Key_{str(uuid.uuid4())[:8]}'
        resp = client.create_key_pair(KeyName=name)

        key = SSHKey(
            name=resp['KeyName'],
            id=resp['KeyPairId'],
            material=resp['KeyMaterial'],
            fingerprint=resp['KeyFingerprint']
        )

        return key

    @classmethod
    def all(cls, **kwargs):
        client = kwargs['client']
        key_pairs = client.describe_key_pairs()['KeyPairs']
        for key in key_pairs:
            if key.get('KeyFingerprint') is not None:
                del key['KeyFingerprint']
            if key.get('Tags') is not None:
                del key['Tags']
        return key_pairs

    def read(self):
        resp = self.client.describe_key_pairs(KeyPairIds=[self.id])
        return resp['KeyPairs'][0]

    def write_to_file(self, path):
        with open(f'{path}/{self.name}.pem', 'w') as file:
            file.write(self.material)
        return

    def update(self):
        return False

    def destroy(self):
        return False

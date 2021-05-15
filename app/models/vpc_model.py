

class Vpcs:
    requied_kwargs = ['client']

    def __init__(self, **kwargs):
        for kwarg in self.required_kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    @classmethod
    def all(cls, **kwargs):
        client = kwargs['client']
        resp = client.describe_vpcs()
        return resp['Vpcs']

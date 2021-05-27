import app.utilities.ssh as ssh


class Instance:

    def __init__(self, resource, id):
        self.resource = resource
        self.id = id

    @classmethod
    def all(cls, client):
        resp = client.describe_instances()
        return resp['Reservations'][0]['Instances']

    @property
    def public_ip_address(self):
        instance = self.resource.Instance(self.id)
        return instance.public_ip_address

    @property
    def state(self):
        instance = self.resource.Instance(self.id)
        return instance.state['Name']

    @property
    def ssh_key_name(self):
        instance = self.resource.Instance(self.id)
        return instance.key_name

    def install_packages(self, ssh_key_file):
        outputs = ssh.install_packages(ip_address=self.public_ip_address,
                                       ssh_key_file=ssh_key_file)

        return True

    def start(self):
        instance = self.resource.Instance(self.id)
        resp = instance.start()
        return resp

    def stop(self):
        instance = self.resource.Instance(self.id)
        resp = instance.stop()
        return resp

    def update(self):

        return

    def destroy(self):
        return False

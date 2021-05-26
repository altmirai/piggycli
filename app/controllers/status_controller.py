from app.models.cluster_model import Cluster
from app.models.hsm_model import HSM
from app.models.instance_model import Instance
import json
import os


class StatusController:
    def __init__(self, credentials_file_path, path, ec2, cloudhsmv2):
        self.path = path
        self.config = _get_config(path=credentials_file_path)
        self.ec2 = ec2
        self.cloudhsmv2 = cloudhsmv2

    def show(self):
        return json.dumps(
            {
                'instance': self.instance_state(),
                'cluster': self.cluster_state(),
                'hsm': self.hsm_state(),
                'backups': self.backups()
            }
        )

    def instance_state(self):
        ssh_key_file = os.path.join(
            self.path, self.config['cluster_id'], f"{self.config['ssh_key_name']}.pem")
        instance = Instance(id=self.config['instance_id'],
                            client=self.ec2, ssh_key_file=ssh_key_file)
        return {'id': instance.id, 'state': instance.read().state['Name']}

    def cluster_state(self):
        cluster = Cluster(client=self.cloudhsmv2, id=self.config['cluster_id'])
        return {'id': cluster.id, 'state': cluster.state}

    def hsm_state(self):
        cluster = Cluster(client=self.cloudhsmv2, id=self.config['cluster_id'])
        hsms = cluster.hsms
        if bool(hsms):
            hsm = HSM(id=cluster.hsms[0]['HsmId'],
                      cluster_id=cluster.id, client=self.cloudhsmv2)
            return {'id': hsm.id, 'state': hsm.state}
        else:
            #  TODO: Return Something Here
            return None

    def backups(self):
        resp = self.cloudhsmv2.describe_backups()
        backups = resp['Backups']
        return {'backups': len(backups)}


def _get_config(path):
    with open(path, 'r') as file:
        config_data_json = file.read()
    config_data = json.loads(config_data_json)
    return config_data

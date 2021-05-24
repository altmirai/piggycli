import json


class StatusController:
    def __init__(self, config_file_path, path):
        self.path = path
        self.config = _get_config(path=config_file_path)


def _get_config(path):
    with open(path, 'r') as file:
        config_data_json = file.read()
    config_data = json.loads(config_data_json)

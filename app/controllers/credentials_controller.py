from app.models.credentials_model import Credentials
import json


class CredentialsController:

    def __init__(self):
        pass

    def create(self, **kwargs):
        credentials = Credentials.create(**kwargs)
        return json.dumps(
            {
                'credentials_file_path': credentials.credentials_file_path,
                'data': credentials.data
            }
        )

    def show(self, credentials_file_path):
        credentials = Credentials.read(
            credentials_file_path=credentials_file_path)

        return json.dumps(
            {
                'credentials_file_path': credentials.credentials_file_path,
                'data': credentials.data
            }
        )

    def update(self, credentials_file_path, **kwargs):
        credentials = Credentials.read(
            credentials_file_path=credentials_file_path)
        credentials.update(**kwargs)

        return json.dumps(
            {
                'credentials_file_path': credentials.credentials_file_path,
                'data': credentials.data
            }
        )

    def destroy(self):
        return

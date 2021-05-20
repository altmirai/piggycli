from app.models.credentials_model import Credentials


class CredentialsController:

    def __init__(self):
        pass

    def index(self):
        return

    def new(self):
        return

    def create(self, **kwargs):
        file_path = kwargs.get('file_path')
        if bool(file_path):
            credentials = Credentials.create_from_file(file_path=file_path)
        else:
            credentials = Credentials.create(**kwargs)
        return credentials

    def show(self):
        return

    def edit(self):
        return

    def update(self):
        return

    def destroy(self):
        return

    def _read_file(self, config_file_path):
        return

    def _set_environ_varriable(self, path):
        return

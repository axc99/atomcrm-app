import os

import requests


class SharedApiClient:
    token = None
    workspace_id = None
    installation_id = None
    version = 1

    def __init__(self, installation_id):
        if self.installation_id != installation_id or not self.token:
            self.installation_id = installation_id
            self.auth()
        else:
            self.installation_id = installation_id

    def auth(self):
        url = '{}api/shared/v{}/app-auth/token'.format(os.environ.get('SHARED_API_URL'), self.version)
        headers = {}
        data = {'installation_id': self.installation_id,
                'app_secret_key': os.environ.get('APP_SECRET_KEY')}
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            print('SharedApiClient: auth - OK 200')
            response_data = response.json()
            self.token = response_data['access_token']
            self.workspace_id = response_data['workspace_id']
        else:
            print('SharedApiClient: auth - {}'.format(response.status_code), response.json())

    def create_message(self, data):
        url = '{}api/shared/v{}/workspaces/{}/messages'.format(os.environ.get('SHARED_API_URL'),
                                                               self.version,
                                                               self.workspace_id)
        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        response = requests.post(url, headers=headers, json={
            'message': data
        })

        if response.status_code == 401:
            print('SharedApiClient: create_message - 401')
            self.auth()
            self.create_messages(data)
        elif response.status_code == 201:
            print('SharedApiClient: create_message - OK 201')
        else:
            print('SharedApiClient: create_message - {}'.format(response.status_code), response.json())

    def delete_message(self):
        pass

import requests


class YougileAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def create_project(self, name, description=None):
        url = f"{self.base_url}/api-v2/projects"
        data = {'name': name}
        if description:
            data['description'] = description
        return requests.post(url, json=data, headers=self.headers)

    def get_project(self, project_id):
        url = f"{self.base_url}/api-v2/projects/{project_id}"
        return requests.get(url, headers=self.headers)

    def update_project(self, project_id, name=None, description=None):
        url = f"{self.base_url}/api-v2/projects/{project_id}"
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        return requests.put(url, json=data, headers=self.headers)
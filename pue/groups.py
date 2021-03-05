from .lights import Light


class Group:
    def __init__(self, api, id, data=None):
        self.api = api
        self.id = id

        self.load_data(data=data)

    def __repr__(self):
        return f'<Group: {self.name} ({self.type})>'

    @property
    def url(self):
        return f'{self.api.groups_url}/{self.id}'

    @property
    def action_url(self):
        return f'{self.url}/action'

    def fetch_data(self):
        return self.api.get(self.url)

    def load_data(self, data=None):
        if not data:
            data = self.fetch_data()

        self.name = data.get('name')
        self.type = data.get('type')
        self.light_ids = [int(lid) for lid in data.get('lights', [])]
        self.action = data.get('action')

    @property
    def lights(self):
        return {
            id: Light(self.api, id)
            for id in self.light_ids
        }

from .lights import Light
from .constants import ROOM_CLASSES
from .filters import GROUP_FILTERS


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
        from .lights import LightSet
        return LightSet({
            id: Light(self.api, id)
            for id in self.light_ids
        })

    @property
    def scenes(self):
        from .scenes import SceneSet
        return SceneSet({
            key: value
            for key, value in self.api.scenes.items()
            if value.group_id == self.id
        })

    def set_state(self, **state):
        if 'scene' in state:
            state['scene'] = state['scene'].id

        self.api.put(self.action_url, state)

    def delete(self):
        self.api.delete(self.url)


class GroupSet(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    # def __repr__(self):
    #     data = dict(self)
    #     return '<GroupSet\n%r\n>' % (data)

    def filter(self, **filters):
        output = dict(self)
        for f, v in filters.items():
            if f in GROUP_FILTERS:
                output = dict(filter(
                    GROUP_FILTERS[f](v),
                    output.items(),
                ))

        return GroupSet(output)

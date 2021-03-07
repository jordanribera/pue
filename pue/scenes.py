from .filters import ResultSet
from .groups import Group
from .lights import Light

from .filters import SCENE_FILTERS


class Scene:
    def __init__(self, api, id, data=None):
        self.api = api
        self.id = id

        self.load_data(data=data)

    def __repr__(self):
        return f'<Scene: {self.name} ({self.type})>'

    @property
    def url(self):
        return f'{self.api.scenes_url}/{self.id}'

    def fetch_data(self):
        return self.api.get(self.url)

    def load_data(self, data=None):
        if not data:
            data = self.fetch_data()

        self.name = data.get('name')
        self.type = data.get('type')
        self.group_id = data.get('group')
        self.light_ids = [int(lid) for lid in data.get('lights', [])]
        self.owner = data.get('owner')
        self.recycle = data.get('recycle')
        self.locked = data.get('locked')
        self.app_data = data.get('appdata', {})
        self.picture = data.get('picture')
        self.image = data.get('image')
        self.last_updated = data.get('lastupdated')
        self.version = data.get('version')

    @property
    def group(self):
        return Group(self.api, self.group_id)

    @property
    def lights(self):
        from .lights import LightSet
        return LightSet({
            id: Light(self.api, id)
            for id in self.light_ids
        })

    def apply(self):
        self.api.put(self.group.action_url, {'scene': self.id})

    def delete(self):
        self.api.delete(self.url)


class SceneSet(ResultSet):
    set_type = 'scenes'
    set_filters = SCENE_FILTERS

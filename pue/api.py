import json
import requests

from .exceptions import NotAuthenticated
from .groups import Group
from .lights import Light
from .scenes import Scene


class HueAPI:
    def __init__(self, bridge, token=None):
        self.bridge = bridge  # IP address
        self.token = token  # Hue API "username"

        self._lights = None
        self._groups = None
        self._scenes = None

    def get(self, url):
        return requests.get(url).json()

    def put(self, url, data={}):
        return requests.put(url, json.dumps(data)).json()

    # API URLs
    @property
    def base_url(self):
        return f'http://{self.bridge}/api/{self.token}'

    @property
    def lights_url(self):
        return f'{self.base_url}/lights'

    @property
    def groups_url(self):
        return f'{self.base_url}/groups'

    @property
    def scenes_url(self):
        return f'{self.base_url}/scenes'

    # Lights
    @property
    def lights(self):
        return self.get_lights(refresh=False)

    def get_lights(self, refresh=True):
        if self._lights and not refresh:
            return self._lights

        response = self.get(self.lights_url)

        self._lights = {
            int(id): Light(self, id, data)
            for id, data in response.items()
        }

        return self._lights

    # Groups
    @property
    def groups(self):
        return self.get_groups(refresh=False)

    def get_groups(self, refresh=True):
        if self._groups and not refresh:
            return self._groups

        response = self.get(self.groups_url)

        self._groups = {
            int(id): Group(self, id, data)
            for id, data in response.items()
        }

        return self._groups

    # Scenes
    @property
    def scenes(self):
        return self.get_scenes(refresh=False)

    def get_scenes(self, refresh=True):
        if self._scenes and not refresh:
            return self._scenes

        response = self.get(self.scenes_url)

        self._scenes = {
            id: Scene(self, id, data)
            for id, data in response.items()
        }

        return self._scenes

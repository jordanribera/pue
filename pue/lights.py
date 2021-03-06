from .filters import LIGHT_FILTERS


class Light:
    def __init__(self, api, id, data=None):
        self.api = api
        self.id = id

        self.load_data(data=data)

    def __repr__(self):
        return f'<Light: {self.name}>'

    @property
    def url(self):
        return f'{self.api.lights_url}/{self.id}'

    @property
    def state_url(self):
        return f'{self.url}/state'

    def fetch_data(self):
        return self.api.get(self.url)

    def load_data(self, data=None):
        if not data:
            data = self.fetch_data()

        self.type = data.get('type')
        self.name = data.get('name')
        self.model_id = data.get('modelid')
        self.manufacturer_name = data.get('manufacturername')
        self.product_name = data.get('productname')

        self.state = data.get('state', {})
        self.capabilities = data.get('capabilities', {})

    def set_state(self, **state):
        self.api.put(self.state_url, state)


class LightSet(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    # def __repr__(self):
    #     data = dict(self)
    #     return '<LightSet\n%r\n>' % (data)

    def filter(self, **filters):
        output = dict(self)
        for f, v in filters.items():
            if f in LIGHT_FILTERS:
                output = dict(filter(
                    LIGHT_FILTERS[f](v),
                    output.items(),
                ))

        return LightSet(output)

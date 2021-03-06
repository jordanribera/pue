class NameFilter:
    def __init__(self, query, **kwargs):
        self.query = query

    def __call__(self, compare):
        return self.query.lower() in compare[1].name.lower()


class OnOffFilter:
    def __init__(self, query, **kwargs):
        self.query = query

    def __call__(self, compare):
        return compare[1].state['on'] == self.query


GROUP_FILTERS = {
    'name': NameFilter,
}

LIGHT_FILTERS = {
    'name': NameFilter,
    'on': OnOffFilter,
}

SCENE_FILTERS = {
    'name': NameFilter,
}

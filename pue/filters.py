from .exceptions import InvalidType
from .exceptions import VagueQuery

from .constants import GROUP_TYPES
from .constants import SCENE_TYPES


class ResultSet(dict):
    set_type = 'results'
    set_filters = {}

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    # def __repr__(self):
    #     data = dict(self)
    #     return f'<{self.__class__}\n{data}\n>'

    def filter(self, **filters):
        output = dict(self)
        for f, v in filters.items():
            if f in self.set_filters:
                output = dict(filter(
                    self.set_filters[f](v),
                    output.items(),
                ))

        return self.__class__(output)

    def get(self, *args, **kwargs):
        if args:
            return dict.get(self, *args, **kwargs)
        output = list(self.filter(**kwargs).values())
        if len(output) > 1:
            raise VagueQuery(f'Multiple {self.set_type} match your query')
        try:
            return output[0]
        except IndexError:
            return None


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


class ReachableFilter:
    def __init__(self, query, **kwargs):
        self.query = query

    def __call__(self, compare):
        return compare[1].state['reachable'] == self.query


class BrightnessFilter:
    def __init__(self, query, **kwargs):
        self.query = query

    def __call__(self, compare):
        return compare[1].state['bri'] == self.query


class BrightnessLTEFilter:
    def __init__(self, query, **kwargs):
        self.query = query

    def __call__(self, compare):
        return compare[1].state['bri'] <= self.query


class BrightnessGTEFilter:
    def __init__(self, query, **kwargs):
        self.query = query

    def __call__(self, compare):
        return compare[1].state['bri'] >= self.query


class GroupTypeFilter:
    def __init__(self, query, **kwargs):
        if query not in GROUP_TYPES:
            raise InvalidType(f'"{query}" is not a valid group type')
        self.query = query

    def __call__(self, compare):
        return compare[1].type == self.query


class SceneTypeFilter:
    def __init__(self, query, **kwargs):
        if query not in SCENE_TYPES:
            raise InvalidType(f'"{query}" is not a valid scene type')
        self.query = query

    def __call__(self, compare):
        return compare[1].type == self.query


GROUP_FILTERS = {
    'name': NameFilter,
    'type': GroupTypeFilter,
}

LIGHT_FILTERS = {
    'name': NameFilter,
    'on': OnOffFilter,
    'bri': BrightnessFilter,
    'bri__lte': BrightnessLTEFilter,
    'bri__gte': BrightnessGTEFilter,
    'reachable': ReachableFilter,
}

SCENE_FILTERS = {
    'name': NameFilter,
    'type': SceneTypeFilter,
}

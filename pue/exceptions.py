class NotAuthenticated(Exception):
    msg = "Hue API token is missing"


class InvalidType(Exception):
    msg = "Not a valid type"


class VagueQuery(Exception):
    msg = "Multiple results match your query"

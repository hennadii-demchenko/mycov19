TIMELINE = 'timeline'

REST_HOST = "http://corona-api.com"
REST_WHERE_TEMPLATE = "/countries/%s"
DATA_FIELD = 'data'
POPULATION_FIELD = 'population'
DATE = 'date'
CONFIRMED = 'confirmed'
DECEASED = 'deaths'
NEW_CONFIRMED = 'new_confirmed'


def get_rest_url(country_code: str):
    return REST_HOST + REST_WHERE_TEMPLATE % country_code



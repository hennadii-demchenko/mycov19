DEFAULT_COUNTRY = 'turkey'

OBJECT_ID = 'OBJECTID'
COUNTRY_NAME = 'ADM0_NAME'
DATA_TIMESTAMP = 'DateOfDataEntry'
TOTAL_CASES = 'cum_conf'
NEW_CASES = 'NewCase'
FEATURES = 'features'
ATTRIBUTES = 'attributes'

ALL_FIELDS = ','.join(
    [OBJECT_ID, COUNTRY_NAME, DATA_TIMESTAMP, TOTAL_CASES, NEW_CASES])

MIN_FIELDS = ','.join(
    [DATA_TIMESTAMP, TOTAL_CASES, NEW_CASES])

REST_HOST = "https://services.arcgis.com"
REST_PATH = "/5T5nSi527N4F7luB/arcgis/rest/services" \
            "/Historic_adm0_v3/FeatureServer/0/query"
REST_QUERY_BASE = "?f=json"
REST_WHERE_TEMPLATE = "&where=ADM0_NAME=%%27%s%%27&"
REST_OUT_TEMPLATE = f"&outFields=%s"
REST_STATIC_OPTIONS = "&returnGeometry=false&resultRecordCount=2000"


def get_rest_url(country: str, fields=MIN_FIELDS):
    return REST_HOST + REST_PATH + REST_QUERY_BASE + \
          REST_WHERE_TEMPLATE % country + REST_STATIC_OPTIONS +\
          REST_OUT_TEMPLATE % fields



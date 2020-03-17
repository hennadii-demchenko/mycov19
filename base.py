import os
from pathlib import Path

BASE_DIR = Path().absolute()
REPORTS_DIR = Path().absolute() / "pdf-data"
STORED_DIR = Path().absolute() / "stored-data"

REPORTS_PAGE_URL = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports"

STORED = os.path.join(str(BASE_DIR), 'data_pickle')
EUROPE_PAGE = 3
DEFAULT_COUNTRY = 'greece'
UPDATED_CASES_OFFSET = 2

from pathlib import Path

DOWNLOADS_FOLDER = 'downloads'
LOGS_FOLDER = 'logs'
LOGS_FILE = 'parser.log'
RESULTS_FOLDER = 'results'

BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / DOWNLOADS_FOLDER
LOG_DIR = BASE_DIR / LOGS_FOLDER
LOG_FILE = LOG_DIR / LOGS_FILE
RESULTS_DIR = BASE_DIR / RESULTS_FOLDER

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
DT_LOGS_FORMAT = '%d.%m.%Y %H:%M:%S'

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_DOC_URL = 'https://peps.python.org/'

OUTPUT_FILE = 'file'
OUTPUT_PRETTY = 'pretty'
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

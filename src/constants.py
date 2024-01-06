from pathlib import Path

DOWNLOADS_FOLDERS_NAME = 'downloads'
LOGS_FOLDERS_NAME = 'logs'
LOGS_FILES_NAME = 'parser.log'
RESULTS_FOLDERS_NAME = 'results'

BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / DOWNLOADS_FOLDERS_NAME
LOG_DIR = BASE_DIR / LOGS_FOLDERS_NAME
LOG_FILE = LOG_DIR / LOGS_FILES_NAME
RESULTS_DIR = BASE_DIR / RESULTS_FOLDERS_NAME

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
DT_LOGS_FORMAT = '%d.%m.%Y %H:%M:%S'

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_DOC_URL = 'https://peps.python.org/'

OUTPUT_FILE = 'file'
OUTPTU_PRETTY = 'pretty'
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

import os
from datetime import datetime

TEST_MODE = True

TODAY_DATE = datetime.today().date()

ALLOWED_EXTENSIONS = {'csv'}

APP_HOST = 'localhost'
APP_PORT = 5000

DATE_FORMAT = '%Y-%m-%d'


UPLOAD_DIR = os.path.join('staticFiles', 'uploads')
TEMP_DATA_DIR = os.path.join('app', 'temp')
TEMP_FILE_PATH = os.path.join(TEMP_DATA_DIR, 'temp_data.json')
SAVED_FILES_PATH = os.path.join('app', 'files', 'uploaded')
BASEDIR = os.getcwd()

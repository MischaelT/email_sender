import os

from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
SHORT_NAME = os.getenv('SHORT_NAME')
FULL_NAME = os.getenv('FULL_NAME')
COMPANY_INFO = os.getenv('COMPANY_INFO')
COMPANY_NAME = os.getenv('COMPANY_NAME')
POSITION = os.getenv('POSITION')
COMPANY_WEBSITE = os.getenv('COMPANY_WEBSITE')
COMPANY_ADDRESS = os.getenv('COMPANY_ADDRESS')
COMPANY_PHONE = os.getenv('PHONE')

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

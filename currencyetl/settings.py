import os

from dotenv import find_dotenv
from dotenv import load_dotenv

load_dotenv(find_dotenv())

BASE_URL = os.getenv("BASE_URL")
CURRENCY = os.getenv("CURRENCY")
API_URL = BASE_URL + CURRENCY
OUTPUT_FILE = os.getenv("OUTPUT_FILE")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT"))
CANCEL_ON_FAILURE = os.getenv("CANCEL_ON_FAILURE") == "true"
CRON_INTERVAL_MINUTES = int(os.getenv("CRON_INTERVAL_MINUTES"))
DEBUG = os.getenv("DEBUG") == "true"

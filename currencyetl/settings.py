import os

from dotenv import find_dotenv
from dotenv import load_dotenv

load_dotenv(find_dotenv())

BASE_URL = os.getenv("BASE_URL")
CURRENCY = os.getenv("CURRENCY")
API_URL = BASE_URL + CURRENCY
OUTPUT_FILE = os.getenv("OUTPUT_FILE")
CANCEL_ON_FAILURE = os.getenv("CANCEL_ON_FAILURE") == "true"

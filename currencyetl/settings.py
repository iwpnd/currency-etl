import os
from os.path import dirname
from os.path import join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

BASE_URL = os.getenv("BASE_URL")
CURRENCY = os.getenv("CURRENCY")
API_URL = BASE_URL + CURRENCY

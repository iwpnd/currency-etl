# currencyetl

Fetch conversion rates for USD from [exchangeratesapi.io](https://exchangeratesapi.io/) and append to CSV file.

## Installation

### prerequisites

create and activate a virtual environment in your working directory:
```bash
virtualenv env
source env/bin/activate
```

create a `.env` file in your working directory:
```bash
# .env
CURRENCY="USD"
BASE_URL="https://api.exchangeratesapi.io/latest?base="
OUTPUT_FILE="output.csv"
CANCEL_ON_FAILURE=false
REQUEST_TIMEOUT=1
CRON_INTERVAL_MINUTES=60
DEBUG=true
```

### installation

clone the repository and install the repository:
```bash
git clone https://github.com/iwpnd/currency-etl.git
pip install -e /currency-etl
```

### testing
```bash
python -m pytest --cov=currency-etl/currencyetl -v
```

## Usage

```bash
currencyetl start
```

Will start a cronjob and fetch conversion rates in USD every hour (defaults to: `settings.CRON_INTERVAL_MINUTES`). Results will be stored in `settings.OUTPUT_FILE` in your working directory.

Use `currencyetl start --help` to get optional parameters:

```bash
currencyetl start --help

Usage: currencyetl start [OPTIONS]

Options:
  --timeout INTEGER         seconds until request timeout
  --output_file TEXT        csvfile to write output to
  --interval INTEGER        cron intervall in minutes
  --logfile / --no-logfile  write logs to file
  --help                    Show this message and exit.
```

import functools
import time

import click
import schedule
from loguru import logger

from currencyetl import methods
from currencyetl import settings


def catch_exceptions(cancel_on_failure: bool = False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except Exception:
                import traceback

                logger.error(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob

        return wrapper

    return catch_exceptions_decorator


@catch_exceptions(cancel_on_failure=settings.CANCEL_ON_FAILURE)
def main(timeout: int, output_file: str) -> None:

    logger.info("Fetching conversion rates for: USD")
    conversion_rates = methods.request_conversion_rates(timeout=timeout)
    logger.info(f"Saving conversion rates to: {output_file}")
    methods.write_conversion_rates_to_csv(
        conversion_rates=conversion_rates, output_file=output_file
    )


def job():
    print("I'm working...")


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--timeout",
    default=settings.REQUEST_TIMEOUT,
    help=f"seconds until request timeout (default: {settings.REQUEST_TIMEOUT})",
)
@click.option(
    "--output_file",
    default=settings.OUTPUT_FILE,
    help=f"csvfile to write output to (default: {settings.OUTPUT_FILE})",
)
@click.option(
    "--interval",
    default=settings.CRON_INTERVAL_MINUTES,
    help=f"cron intervall in minutes (default: {settings.CRON_INTERVAL_MINUTES})",
)
@click.option(
    "--logfile/--no-logfile",
    default=settings.DEBUG,
    help=f"write logs to file (default: {settings.DEBUG})",
)
def start(timeout: int, output_file: str, interval: int, logfile: bool) -> None:

    if logfile:
        logger.add("file.log", enqueue=True)

    click.echo("Initializing cronjob")
    schedule.every(interval).minutes.do(main, output_file=output_file, timeout=timeout)

    while True:
        schedule.run_pending()
        time.sleep(1)


cli.add_command(start)

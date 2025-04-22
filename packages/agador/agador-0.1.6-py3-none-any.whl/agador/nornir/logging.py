from typing import Union
import logging
from decouple import config

from umnet_napalm.utils import configure_logging

LOG_FORMAT = "%(asctime)-15s  %(levelname)8s %(name)s %(message)s"
DEFAULT_LOGFILE = f"{config('LOG_DIR')}/agador.log"

LEVELS = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class ThreadLogFilter(logging.Filter):
    """
    Stolen from StackOverflow - log filter by thread name
    """

    def __init__(self, thread_name, *args, **kwargs):
        logging.Filter.__init__(self, *args, **kwargs)
        self.thread_name = thread_name

    def filter(self, record):
        return record.threadName == self.thread_name


def normalize_log_level(level: Union[str, int]) -> int:

    if isinstance(level, int):
        return level

    if level.upper() not in LEVELS:
        raise ValueError(f"Log level must be a number or one of {LEVELS}")

    return LEVELS[level.upper()]


def filter_textfsm_extractor(record):
    """
    Don't like this error from napalm.base.helpers filling up
    our logs every time we try to run a textfsm template
    """
    if "textfsmExtractorErr01" in record.msg:
        return False
    return True


def configure_nornir_logging(
    log_level, log_globally=False, log_file: str = None, log_to_console=False
):
    """
    Configures logging for nornir.
    """
    configure_logging(log_level, log_globally, log_file, log_to_console)

    # also want to turn of this annoying napalm log
    logging.getLogger("napalm.base.helpers").addFilter(filter_textfsm_extractor)

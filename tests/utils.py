import os
from pathlib import Path
import logging
from jrotatelog.handler import RotateFileHandler


def delete_test_logs(log_prefix: str) -> None:
    for file in os.listdir():
        if Path(file).is_file and file.startswith(log_prefix):
            Path(file).unlink()


def get_log_file_names(log_prefix: str) -> list[str]:
    file_names = []
    for file in os.listdir():
        if Path(file).is_file and file.startswith(log_prefix):
            file_names.append(file)
    return file_names


def get_test_log_count(log_prefix: str) -> int:
    count = 0
    for file in os.listdir():
        if Path(file).is_file and file.startswith(log_prefix):
            count = count + 1
    return count


def get_logger(log_prefix, backup_count=10, delay=False) -> logging.Logger:
    logger = logging.getLogger("testing")
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = RotateFileHandler(log_prefix, backupCount=backup_count, delay=delay)
    fh.setLevel(logging.DEBUG)
    # add the handlers to the logger
    logger.addHandler(fh)
    return logger

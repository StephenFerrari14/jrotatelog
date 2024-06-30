from multiprocessing import Process
from pathlib import Path
from tests.utils import (
    delete_test_logs,
    get_logger,
    get_test_log_count,
)

LOG_PREFIX = "test.log"


def log_function(index: int, backup_count=10) -> None:
    logger = get_logger(LOG_PREFIX, backup_count=backup_count)
    logger.info("Logging in thread: %s", index)


def test_from_empty():
    delete_test_logs(LOG_PREFIX)
    logger = get_logger(LOG_PREFIX)
    logger.debug("Log for test_from_empty")
    logger.info("Log for test_from_empty")
    logger.warning("Log for test_from_empty")
    logger.error("Log for test_from_empty")

    assert Path(LOG_PREFIX).exists()
    num_lines = sum(1 for _ in open(LOG_PREFIX, "rb"))
    assert num_lines == 4


def test_rotate_log_runs():
    delete_test_logs(LOG_PREFIX)

    count = 3

    for i in range(count):
        process = Process(target=log_function, args=(i,))
        process.start()
        process.join()

    assert get_test_log_count(LOG_PREFIX) == count


def test_backup_count():
    delete_test_logs(LOG_PREFIX)
    count = 5
    backup_count = count - 3

    for i in range(count):
        process = Process(target=log_function, args=(i, backup_count))
        process.start()
        process.join()

    assert get_test_log_count(LOG_PREFIX) == backup_count + 1  # Count plus base

    delete_test_logs(LOG_PREFIX)

    try:
        get_logger(LOG_PREFIX, 0)
        assert False
    except ValueError:
        assert True


def test_delay():
    delete_test_logs(LOG_PREFIX)
    logger = get_logger(LOG_PREFIX, delay=True)
    logger.info("test_delay")
    assert get_test_log_count(LOG_PREFIX) == 1  # Should not have rotated yet

    logger2 = get_logger(LOG_PREFIX, delay=True)
    assert get_test_log_count(LOG_PREFIX) == 1  # Should not have rotated yet

    logger2.info("test_delay_2")
    assert get_test_log_count(LOG_PREFIX) == 2  # Should have rotated

from logging import FileHandler, LogRecord
import os
from pathlib import Path
import re
from typing import List

FILE_INDEX_SEPARATOR = "."


class RotateFileHandler(FileHandler):
    """
    A handler class which writes formatted logging records to disk files.
    Logs are rotated when the handler is initialized or can be delayed to first log emit with delay=True.
    backupCount cannot be less than 1

    Example rotation after 3 runs:
    app.log
    app.log.0
    app.log.1
    """

    hasLogged = False

    def __init__(
        self,
        filename,
        mode="a",
        encoding=None,
        delay=False,
        errors=None,
        backupCount=10,
    ):
        if backupCount < 1:
            raise ValueError("backupCount cannot be less than 1")

        self.baseFilename = filename
        self.backupCount = backupCount

        if not delay and os.path.isfile(filename):
            self._rotateLog()

        super().__init__(
            filename, mode=mode, encoding=encoding, delay=delay, errors=errors
        )

    def emit(self, record: LogRecord) -> None:
        if self.delay and not self.hasLogged:
            self.hasLogged = True
            if os.path.isfile(self.baseFilename):
                self._rotateLog()
        return super().emit(record)

    def _get_log_files(self, filename: str) -> List[tuple[str, int]]:
        """
        Get log files and sort
        """
        pattern = re.compile(f"{filename}{FILE_INDEX_SEPARATOR}(\\d)")
        logfiles = []
        for file in os.listdir():
            pmatch = pattern.match(file)
            if pmatch:
                logfiles.append((file, int(pmatch.group(1))))
        logfiles.sort()
        return logfiles

    def _rotateLog(self) -> None:
        """
        Rotate log file taking backup count into consideration
        If there would be a log that goes over the backup count after rotation then delete it.
        """
        filename = self.baseFilename

        # Get files that match log pattern
        logfiles = self._get_log_files(filename)

        filemap = {filename: f"{filename}{FILE_INDEX_SEPARATOR}0"}
        deleteList = []

        for file, oldNum in logfiles:
            if oldNum >= self.backupCount - 1:
                deleteList.append(file)
            else:
                newNum = oldNum + 1
                newName = f"{filename}{FILE_INDEX_SEPARATOR}{newNum}"
                filemap[file] = newName

        filesToApply = list(filemap.keys())
        # Reverse so we do the oldest files first
        filesToApply.reverse()

        # Apply
        for oldfile in deleteList:
            Path(oldfile).unlink()

        for oldfile in filesToApply:
            os.rename(oldfile, filemap[oldfile])

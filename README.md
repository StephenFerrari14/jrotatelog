# JRotateLog

Rotate logs with incremental generation numbers. This is similar to the RotatingFileHandler but instead of max bytes as the rotate condition its when a new python program runs. For every run of the python code rotate the logs with the backed up files indexed start at 0.

Ex.
Run python program 3 times creates 2 backups
```
app.log
app.log.0
app.log.1
```
`backup_count` can be used to limit how many logs are kept.
Ex.
Run python program 4 times with backupCount = 2
```
app.log   (from run 4)
app.log.0 (from run 3)
app.log.1 (from run 2)
app.log.2 (from run 1, deleted)
```

## Install
```
pip install jrotatelog
```

## Usage
```
from jrotatelog.handler import RotateFileHandler

logger = logging.getLogger("app")
fh = RotateFileHandler("app.log")
logger.addHandler(fh)
```


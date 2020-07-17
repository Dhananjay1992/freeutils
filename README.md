# freeutils
This is Free to use utils or code snippets created by DJDeveloper. Please feel free to fork and add your contributions.
It provides easy to use pluggable lib. you can have separation between differt logs for example Database logs can be logged by using db_logger and generic logs can be logged by using main_logger. You can use any supported logging methods for python logging module.

# Default parameters

You can change the default values. These are used at global level.

```python
LOG_FOLDER = 'logs'
LOGGER_FORMAT = "[%(levelname)s]:[%(filename)s]:[%(asctime)s]:[%(funcName)s():%(lineno)i]:[%(message)s]"
LOG_LEVEL = logging.DEBUG
```

# Example Usage

```python

from logger import logger
logger.main_logger.info('This is info message')
logger.main_logger.warn('Warning: This might lead to improper behaviour')
logger.db_logger.error('Unbale to connect to Databse')

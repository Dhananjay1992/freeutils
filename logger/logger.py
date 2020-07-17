import logging
import traceback
import os

LOG_FOLDER = 'logs'
LOGGER_FORMAT = "[%(levelname)s]:[%(filename)s]:[%(asctime)s]:[%(funcName)s():%(lineno)i]:[%(message)s]"
LOG_LEVEL = logging.DEBUG


class Logger(object):
    _instance = None
    _shared_state = {}

    def __new__(cls):
        if not cls._instance:
            if not os.path.exists(LOG_FOLDER):
                os.makedirs(LOG_FOLDER)
            cls._instance = super(Logger, cls).__new__(cls)
            cls.db_logger = logging.getLogger('db_logger')
            cls.db_logger.setLevel(LOG_LEVEL)
            formatter = logging.Formatter(LOGGER_FORMAT)
            file_handler = logging.FileHandler(LOG_FOLDER + '/db_logs.log')
            file_handler.setFormatter(formatter)
            # add formatter to ch
            cls.db_logger.addHandler(file_handler)

            cls.main_logger = logging.getLogger('main_logger')
            cls.main_logger.setLevel(LOG_LEVEL)
            file_handler = logging.FileHandler(LOG_FOLDER + '/main_logs.log')
            file_handler.setFormatter(formatter)
            cls.main_logger.addHandler(file_handler)
            cls.main_logger.info("Main Logger initialized...")
            cls.db_logger.info("DB Logger initialized...")
            cls._instance.__dict__ = cls._shared_state
        return cls._instance

    def __init__(self):
        if Logger._instance is None:
            Logger.__new__(self)

    def log_with_traceback_error(self, logger_name='main'):
        try:
            if logger_name.lower() == 'main':
                self.main_logger.error(traceback.format_exc())
            else:
                self.db_logger.error(traceback.format_exc())

        except Exception:
            pass


logger = Logger()

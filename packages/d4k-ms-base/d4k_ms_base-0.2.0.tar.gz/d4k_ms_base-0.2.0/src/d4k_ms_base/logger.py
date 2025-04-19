import logging
import traceback

class Logger():

    FORMAT = '{levelname:<9s} {message}'
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
  
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, level=logging.INFO):
        if not Logger._initialized:
            logging.basicConfig(format=self.FORMAT, style='{')
            self.logger = logging.getLogger("application")
            self.logger.setLevel(level)
            Logger._initialized = True

    def set_level(self, level):
        self.logger.setLevel(level)

    def get_level(self):
        return self.logger.getEffectiveLevel()

    def get_level_str(self):
        return logging.getLevelName(self.logger.getEffectiveLevel())

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message, e, exception=None):
        self.logger.error(f"{message}\n\nDetails: '{e}'\n\nTrace:\n\n{traceback.format_exc()}")
        if exception:
            raise exception(message)
  
application_logger = Logger()
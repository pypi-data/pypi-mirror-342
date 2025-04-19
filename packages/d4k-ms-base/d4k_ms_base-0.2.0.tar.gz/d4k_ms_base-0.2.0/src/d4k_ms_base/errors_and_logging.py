import traceback
import warnings
from d4k_ms_base.logger import application_logger
from d4k_sel.errors import Errors
from d4k_sel.error_location import ErrorLocation


class ErrorsAndLogging():

  WARNING = Errors.WARNING
  ERROR = Errors.ERROR
  DEBUG = Errors.DEBUG
  INFO = Errors.INFO

  def __init__(self):
    self.errors = Errors()

  def debug(self, message: str, location: ErrorLocation):
    application_logger.debug(self._format(message, location.format()))

  def info(self, message: str, location: ErrorLocation):
    application_logger.info(self._format(message, location.format()))

  def exception(self, message: str, e: Exception, location: ErrorLocation):
    self.errors.add(f"Exception. {message}. See log for additional details.", location, self.errors.ERROR)
    application_logger.error(f"Exception '{e}' raised\n\n{self._format(message, location)}\n\n{traceback.format_exc()}")

  def warning(self, message: str, location: ErrorLocation):
    self.errors.add(message, location, self.errors.WARNING)
    application_logger.warning(self._format(message, location.format()))

  def error(self, message: str, location: ErrorLocation):
    self.errors.add(message, location, self.errors.ERROR)
    application_logger.error(self._format(message, location.format()))

  def deprecated(self, message):
    warnings.warn(message, DeprecationWarning)    
    application_logger.warning(self._format(message, '[no location reference]'))

  def _format(self, message, location: str):
    return f"{location}: {message}"

import os
from dotenv import load_dotenv
from d4k_ms_base.logger import application_logger

class ServiceEnvironment():
  
  def __init__(self):
    self.load()

  def environment(self):
    if 'PYTHON_ENVIRONMENT' in os.environ:
      return os.environ['PYTHON_ENVIRONMENT']
    else:
      return "development"

  def production(self):
    return self.environment() == "production"

  def get(self, name):
    if name in os.environ:
      return os.environ[name]
    else:
      application_logger.error(f"Missing environment variable '{name}' requested")
      return ""

  def load(self):
    filename = f".{self.environment()}_env"
    application_logger.debug(f"Environment file '{filename}' read")
    load_dotenv(filename)
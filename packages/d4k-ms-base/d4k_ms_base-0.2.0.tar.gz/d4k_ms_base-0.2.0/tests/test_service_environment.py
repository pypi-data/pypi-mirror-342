import os
from d4k_ms_base.service_environment import ServiceEnvironment

def test_environment_set():
  assert ServiceEnvironment().environment() == "test"

def test_environment_invalid():
  preserve = os.environ['PYTHON_ENVIRONMENT']
  os.environ['PYTHON_ENVIRONMENT'] = "X"
  assert ServiceEnvironment().environment() == "X"
  os.environ['PYTHON_ENVIRONMENT'] = preserve

def test_environment_not_set():
  preserve_all = os.environ
  preserve = preserve_all.pop('PYTHON_ENVIRONMENT')
  assert ServiceEnvironment().environment() == "development"
  preserve_all['PYTHON_ENVIRONMENT'] = preserve
  os.environ = preserve_all

def test_environment_get():
  preserve = os.environ
  os.environ['SOMETHING1'] = "X"
  assert ServiceEnvironment().get('SOMETHING1') == "X"
  os.environ = preserve

def test_production():
  assert ServiceEnvironment().production() == False
  
def test_environment_missing():
  assert ServiceEnvironment().get('SOMETHING2') == ""

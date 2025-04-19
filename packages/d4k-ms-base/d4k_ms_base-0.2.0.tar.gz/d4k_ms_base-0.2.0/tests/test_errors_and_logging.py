import pytest
from unittest.mock import patch
from d4k_ms_base.errors_and_logging import ErrorsAndLogging
from d4k_sel.error_location import ErrorLocation

class MockErrorLocation(ErrorLocation):
    def format(self):
        return 'Mock Location'

    def to_dict(self):
        return {'mock_key': 'mock_value'}

def test_errors_and_logging_initialization():
    eal = ErrorsAndLogging()
    assert eal.errors.count() == 0  # Ensure the Errors instance is initialized correctly

@patch('d4k_ms_base.errors_and_logging.application_logger')
def test_errors_and_logging_debug(mock_logger):
    eal = ErrorsAndLogging()
    location = MockErrorLocation()
    eal.debug('Debug message', location)
    mock_logger.debug.assert_called_once_with('Mock Location: Debug message')

@patch('d4k_ms_base.errors_and_logging.application_logger')
def test_errors_and_logging_info(mock_logger):
    eal = ErrorsAndLogging()
    location = MockErrorLocation()
    eal.info('Info message', location)
    mock_logger.info.assert_called_once_with('Mock Location: Info message')

@patch('d4k_ms_base.errors_and_logging.application_logger')
def test_errors_and_logging_exception(mock_logger):
    eal = ErrorsAndLogging()
    location = MockErrorLocation()
    try:
        raise ValueError("Test exception")
    except ValueError as e:
        eal.exception('An error occurred', e, location)
    
    assert eal.errors.count() == 1  # Ensure the error was added
    mock_logger.error.assert_called()  # Ensure the error was logged

@patch('d4k_ms_base.errors_and_logging.application_logger')
def test_errors_and_logging_warning(mock_logger):
    eal = ErrorsAndLogging()
    location = MockErrorLocation()
    eal.warning('Warning message', location)
    assert eal.errors.count() == 1  # Ensure the warning was added
    mock_logger.warning.assert_called_once_with('Mock Location: Warning message')

@patch('d4k_ms_base.errors_and_logging.application_logger')
def test_errors_and_logging_error(mock_logger):
    eal = ErrorsAndLogging()
    location = MockErrorLocation()
    eal.error('Error message', location)
    assert eal.errors.count() == 1  # Ensure the error was added
    mock_logger.error.assert_called_once_with('Mock Location: Error message')

def test_errors_and_logging_deprecated():
    eal = ErrorsAndLogging()
    with pytest.warns(DeprecationWarning):
        eal.deprecated('This is deprecated')
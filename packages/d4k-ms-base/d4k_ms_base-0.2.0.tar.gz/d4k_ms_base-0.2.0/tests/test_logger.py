import pytest
import logging
from d4k_ms_base.logger import Logger, application_logger

def test_singleton():
    instance_1 = Logger()
    instance_2 = Logger()
    assert instance_1 == instance_2

def test_default_level():
    instance_1 = Logger()
    assert instance_1.logger.getEffectiveLevel() == logging.INFO

def test_default_initialization():
    instance_1 = Logger()
    instance_1.set_level(application_logger.DEBUG)
    assert instance_1.logger.getEffectiveLevel() == logging.DEBUG
    instance_2 = Logger()
    assert instance_2.logger.getEffectiveLevel() == logging.DEBUG

def test_default(caplog):
    application_logger.set_level(application_logger.INFO)
    application_logger.debug("LOGGING MESSAGE DEBUG")
    application_logger.error("LOGGING MESSAGE ERROR")
    application_logger.warning("LOGGING MESSAGE WARNING")
    application_logger.info("LOGGING MESSAGE INFO")
    assert "LOGGING MESSAGE DEBUG" not in caplog.text
    assert "LOGGING MESSAGE ERROR" in caplog.text
    assert "LOGGING MESSAGE WARNING" in caplog.text
    assert "LOGGING MESSAGE INFO" in caplog.text

def test_set_level(caplog):
    assert application_logger.logger.getEffectiveLevel() == logging.INFO
    application_logger.set_level(application_logger.DEBUG)
    assert application_logger.logger.getEffectiveLevel() == logging.DEBUG

def test_get_level(caplog):
    application_logger.set_level(application_logger.INFO)
    assert application_logger.get_level() == logging.INFO
    assert application_logger.get_level_str() == "INFO"
    application_logger.set_level(application_logger.DEBUG)
    assert application_logger.get_level() == logging.DEBUG
    assert application_logger.get_level_str() == "DEBUG"

def test_debug(caplog):
    application_logger.set_level(application_logger.DEBUG)
    application_logger.debug("LOGGING MESSAGE")
    for record in caplog.records:
        assert record.levelname == "DEBUG"
    assert "LOGGING MESSAGE" in caplog.text

def test_info(caplog):
    application_logger.set_level(application_logger.INFO)
    application_logger.info("LOGGING MESSAGE")
    for record in caplog.records:
        assert record.levelname == "INFO"
    assert "LOGGING MESSAGE" in caplog.text

def test_warning(caplog):
    application_logger.set_level(application_logger.WARNING)
    application_logger.warning("LOGGING MESSAGE")
    for record in caplog.records:
        assert record.levelname == "WARNING"
    assert "LOGGING MESSAGE" in caplog.text

def test_error(caplog):
    application_logger.set_level(application_logger.ERROR)
    application_logger.error("LOGGING MESSAGE")
    for record in caplog.records:
        assert record.levelname == "ERROR"
    assert "LOGGING MESSAGE" in caplog.text

def test_exception(caplog):
    try:
        result = 12 / 0
    except Exception as e:
        application_logger.exception("Divide by zero", e)
    for record in caplog.records:
        assert record.levelname == "ERROR"
    assert "Divide by zero" in caplog.text

def test_exception_with_raise(caplog):
    with pytest.raises(Exception):
        try:
            result = 12 / 0
        except Exception as e:
            application_logger.exception("Divide by zero", e, Exception)
        for record in caplog.records:
            assert record.levelname == "ERROR"
        assert "Divide by zero" in caplog.text

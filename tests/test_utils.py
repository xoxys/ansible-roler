import six
import os
import logging
import ansibleroler.utils as utils


def test_setup_logging():
    assert utils.setup_logging(log_level='WARNING') is None
    assert logging.getLogger("ansibleroler").getEffectiveLevel() == 30
    assert utils.setup_logging(log_level=10) is None
    assert logging.getLogger("ansibleroler").getEffectiveLevel() == 10


def test_update_log_level():
    assert utils.update_log_level(log_level='WARNING') is None
    assert logging.getLogger("ansibleroler").getEffectiveLevel() == 30
    assert utils.update_log_level(log_level=10) is None
    assert logging.getLogger("ansibleroler").getEffectiveLevel() == 10


def test_normalize_path():
    assert os.path.exists(utils.normalize_path('~')) is True


def test_convert_bool():
    assert utils.convert_bool(True) is True
    assert utils.convert_bool('True') is True
    assert utils.convert_bool('yes') is True
    assert utils.convert_bool(False) is False
    assert utils.convert_bool('False') is False
    assert utils.convert_bool('no') is False
    assert type(utils.convert_bool('string')) is six.text_type
    assert utils.convert_bool('string') == 'string'


def test_settings_object():
    settings = utils.Settings()
    assert settings.log_level == 'WARNING'

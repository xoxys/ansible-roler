import pytest
import os
from pkg_resources import resource_filename
from argparse import Namespace
from ansiblerole.utils.settings import get_settings
from ansiblerole.utils.settings import _validate_config
from ansiblerole.utils import Settings


@pytest.fixture()
def test_options():
    return Namespace(config_file="empty.ini", role_name="testrole", base_path="/tmp/ansible", log_level=10)


def simple_validate_config(settings):
    return settings


def simple_update_log_level(log_level):
    return True


def simple_convert_bool(obj):
    return obj


def simple_normalize_path(path):
    return path


def test_get_settings(mocker, test_options):
    mocker.patch('ansiblerole.utils.settings._validate_config', side_effect=simple_validate_config)
    mocker.patch('ansiblerole.utils.settings.update_log_level', side_effect=simple_update_log_level)
    mocker.patch('ansiblerole.utils.settings.convert_bool', side_effect=simple_convert_bool)
    mocker.patch('ansiblerole.utils.settings.normalize_path', side_effect=simple_normalize_path)
    result = get_settings(test_options)
    template = os.path.join(resource_filename('ansiblerole', 'static'), 'templates', 'main.yml.j2')

    assert type(result) is Settings
    assert result.config_file == "empty.ini"
    assert result.role_name == "testrole"
    assert result.base_path == "/tmp/ansible"
    assert result.log_level == 10
    assert result.subdir_template == template

    result = get_settings(Namespace(config_file="tests/testconfig.ini"))
    assert type(result) is Settings
    assert result.template_vars['meta']['bool'] == 'yes'
    assert result.log_level == 'warning'


def test_validate_config():
    settings = _validate_config(Settings(config_file='empty.ini'))
    default = Settings()
    assert type(settings) is Settings

    setattr(settings, 'log_level', 'info')
    assert _validate_config(settings).log_level == 'INFO'

    setattr(settings, 'log_level', 'unnown')
    assert _validate_config(settings).log_level == default.log_level

    setattr(settings, 'enable_templating', True)
    assert _validate_config(settings).enable_templating is True

    setattr(settings, 'enable_templating', 'true')
    assert _validate_config(settings).enable_templating is False

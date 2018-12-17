from ansibleroler.utils import Settings
from ansibleroler.utils import template

try:
    from unittest.mock import call
except ImportError:
    from mock import call


def simple_render_template(template, path, context):
    return True


def jinja_dump_to_string(path):
    return path


def test_add_role(mocker):
    mocker.patch('os.makedirs')
    mocker.patch('ansibleroler.utils.template._render_template', side_effect=simple_render_template)
    settings = Settings(enable_templating=True, role_name='myrole')

    assert template.add_role(settings) is None
    assert template.os.makedirs.call_count == 8

    template._render_template.reset_mock()
    assert template.add_role(settings) is None
    assert template._render_template.call_count == 5

    setattr(settings, 'root_template', '')
    template._render_template.reset_mock()
    assert template.add_role(settings) is None
    assert template._render_template.call_count == 4

    setattr(settings, 'subdir_template', '')
    template._render_template.reset_mock()
    assert template.add_role(settings) is None
    assert template._render_template.call_count == 0


def test_render_template(mocker):
    mocker.patch('jinja2.environment.TemplateStream.dump', side_effect=jinja_dump_to_string)
    result = template._render_template('tests/main.yml.j2', 'tmp', {})

    assert result == "tmp/main.yml"

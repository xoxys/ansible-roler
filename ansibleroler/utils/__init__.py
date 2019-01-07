import os
import yaml
import logging
import logging.config
from appdirs import AppDirs
from pkg_resources import resource_filename


def setup_logging(log_level):
    log_config_file = os.path.join(resource_filename('ansibleroler', 'static'), 'config', 'logging.yml')
    level = logging.getLevelName(log_level)
    with open(log_config_file, 'rt') as f:
        log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    if level:
        logging.getLogger("ansibleroler").setLevel(level)
    return


def update_log_level(log_level):
    level = logging.getLevelName(log_level)
    if level:
        logging.getLogger("ansibleroler").setLevel(level)
    return


def normalize_path(path):
    normalized = os.path.abspath(os.path.expanduser(path))

    return normalized


def convert_bool(obj):
    true_values = (True, 'True', 'true', 'yes', '1')
    false_values = (False, 'False', 'false', 'no', '0')

    if obj in true_values:
        return True
    elif obj in false_values:
        return False
    else:
        return obj


class Settings(object):
    def __init__(
        self,
        config_file=os.path.join(AppDirs("ansible-roler").user_config_dir, "config.ini"),
        role_name=None,
        base_path=os.getcwd(),
        log_level='ERROR',
        subdir_template=os.path.join(resource_filename('ansibleroler', 'static'), 'templates', 'main.yml.j2'),
        root_template=os.path.join(resource_filename('ansibleroler', 'static'), 'templates', '.drone.yml.j2'),
        enable_templating=False,
        template_vars={}
    ):

        self.config_file = config_file
        self.role_name = role_name
        self.base_path = base_path
        self.log_level = log_level
        self.subdir_template = subdir_template
        self.root_template = root_template
        self.enable_templating = enable_templating
        self.template_vars = template_vars

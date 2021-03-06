import os
import six
import logging
from configparser import ConfigParser
from collections import defaultdict
from ansibleroler.utils import Settings
from ansibleroler.utils import normalize_path
from ansibleroler.utils import convert_bool
from ansibleroler.utils import update_log_level


def get_settings(options):
    logger = logging.getLogger("ansibleroler")
    defaults = Settings()
    config_file = normalize_path(options.config_file)

    config = ConfigParser()
    config.read(config_file)

    template_vars = defaultdict(dict)

    for section in config.sections():
        for key, value in config.items(section):
            if not section == "template-vars":
                setattr(defaults, key, convert_bool(value))
            else:
                split = key.split("_", 1)
                template_vars[split[0]].update({split[1]: convert_bool(value)})
    setattr(defaults, 'template_vars', template_vars)

    # Merge CLI options with config options. CLI options wins (if set).
    for key, value in options.__dict__.items():
        if value:
            setattr(defaults, key, value)

    # Transform loglevel string
    if isinstance(defaults.log_level, six.text_type):
        defaults.log_level = defaults.log_level.upper()

    # Transform string to array for exclude_subdirs
    if isinstance(defaults.exclude_subdirs, six.text_type):
        defaults.exclude_subdirs = [x.strip() for x in defaults.exclude_subdirs.split(",")]
    elif not defaults.exclude_subdirs:
        defaults.exclude_subdirs = []

    settings = _validate_config(defaults)
    update_log_level(log_level=settings.log_level)

    if not os.path.exists(config_file):
        logger.info("Config file '{}' not found. Use default settings.".format(config_file))

    return settings


def _validate_config(settings):
    logger = logging.getLogger("ansibleroler")
    defaults = Settings()
    log_level_allowed = ('WARNING', 'ERROR', 'INFO', 'DEBUG', 10, 20, 30, 40)

    if settings.log_level not in log_level_allowed:
        logger.warning(
            "Misconfigured value for 'log_level'. Set to default '{}'".format(defaults.log_level))
        settings.log_level = defaults.log_level

    if not isinstance(settings.enable_templating, bool):
        logger.warning(
            "Misconfigured value for 'enable_templating'. Set to default '{}'".format(defaults.enable_templating))
        settings.enable_templating = defaults.enable_templating

    return settings

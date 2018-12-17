#!/usr/bin/env python
"""Setup script for the package."""

import re
import os
from setuptools import find_packages
from setuptools import setup

PACKAGE_NAME = "ansibleroler"


def get_property(prop, project):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
                       open(os.path.join(current_dir, project, '__init__.py')).read())
    return result.group(1)


setup(
    name=get_property("__project__", PACKAGE_NAME),
    version=get_property("__version__", PACKAGE_NAME),
    description=("Command line tool to template the structure of a new ansible role."),
    keywords="ansible cli role template",
    author=get_property("__author__", PACKAGE_NAME),
    author_email=get_property("__email__", PACKAGE_NAME),
    license=get_property("__license__", PACKAGE_NAME),
    url="https://github.com/xoxys/ansible-role",
    packages=find_packages(exclude=["tests", "tests.*"]),
    # include_package_data=True,
    package_dir={'ansibleroler': 'ansibleroler'},
    package_data={
        'ansibleroler': [
            'static/config/*.ini',
            'static/config/*.yml',
            'static/templates/*'
        ],
    },
    zip_safe=False,
    install_requires=[
        "appdirs",
        "jinja2",
        "PyYAML"
    ],
    entry_points={
        'console_scripts': [
            'ansible-roler = ansibleroler.__main__:main'
        ]
    }
)

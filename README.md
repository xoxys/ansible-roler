# ansible-roler

[![Build Status](https://cloud.drone.io/api/badges/xoxys/ansible-roler/status.svg)](https://cloud.drone.io/xoxys/ansible-roler)
[![](https://img.shields.io/pypi/pyversions/ansible-roler.svg)](https://pypi.org/project/ansible-roler/)
[![](https://img.shields.io/pypi/status/ansible-roler.svg)](https://pypi.org/project/ansible-roler/)
[![](https://img.shields.io/pypi/v/ansible-roler.svg)](https://pypi.org/project/ansible-roler/)

`ansible-roler` is a simple command line tool to setup the recommendet folder structure for a new ansible role.

## Table of Content

- [Setup](#setup)
- [Usage](#usage)
- [Configuration](#configuration)
  - [Defaults](#defaults)
  - [Base configuration](#base-configuration)
  - [Templating](#templating)
- [License](#license)
- [Maintainers and Contributors](#maintainers-and-contributors)

---

### Setup

```Shell
# From internal pip repo as user
pip install ansible-roler --user

# .. or as root
sudo pip install ansible-roler
```

### Usage

```Shell
$ ansible-roler --help
usage: ansible-roler [-h] [-c CONFIG_FILE] [-n NAME] [-p PATH] [-v]

Manage ansible role environments

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE        Location of configuration file:
                        [/Users/rkau2905/Library/Application Support/ansible-
                        role/config.ini]
  -n NAME, --name NAME  Name of the new role
  -p PATH, --path PATH  Path where the new role will be created
  -v, --verbose         Show more verbose output
```

### Configuration

#### Defaults

`ansible-roler` will create the the minimal recommended folder structure:

```Text
common/
    tasks/
        main.yml
    handlers/
        main.yml
    templates/
    files/
    vars/
    defaults/
        main.yml
    meta/
        main.yml
```

The main.yml files will be created only if you enable the [templating feature](#templating). Otherwise
the folders will be left empty.

#### Base configuration

In addition to the command line options there are parameters you can adjust in a config file. The default location
for your config file is `~/ansible-roler/config.ini` but you can place it anywhere and
specifiy the path with `ansible-roler -c /path/to/config.ini`.

```INI
[base]
# base path ansible-roler will use to create new roles
base_path=~/ansibleroles

[logging]
# error | warning | info | debug
# you can also control this with commandline attribute -vvv
log_level=warning
```

#### Templating

In special cases it can be helpfule to add templated files to each new role. The templating function
can be used to place in customized meta/main.yml or a default config file for your CI in each new role.
The templating is disabled by default and must be enabled in the config file befor you can use it.

```INI
[templating]
# enable template functionality
enable_templating=false
# path to your own subdir template file
# if not in config file default one will be used
# if added empty 'subdir_template=' subdir templating is disabled
subdir_template=/home/jdoe/ansible/custom/main.yaml.j2
# if you like you can exclude some subdirs from templating
# these folders will be left empty
exclude_subdirs=templates,vars,files
# path to your own ci template file
# if not in config file default one will be used
# if added empty 'ci_template=' ci templating is disabled
root_template=/home/jdoe/ansible/custom/.drone.yaml.j2

[template-vars]
# define some variables you want to use in your template
meta_author=John Doe
meta_license=MIT
```

`ansible-roler` comes with simple default template file but as you can see in the config you can
customize and use your own. The default file looks as follows:

```HTML+Django
---
{% if subdir == 'tasks' %}
# Contains the main list of tasks to be executed by the role.
# Don't add tasks directly to the main.yml use includes instead
- include_tasks: setup.yml
{% endif %}
{% if subdir == 'handlers' %}
# Contains handlers, which may be used by this role or
# even anywhere outside this role.
{% endif %}
{% if subdir == 'defaults' %}
# Default variables for the role.
{% endif %}
{% if subdir == 'meta' %}
galaxy_info:
  author: {{ vars.meta.author | default('UNKNOWN') }}
  description: Deploy some application
  license: {{ vars.meta.author | default('MIT') }}
  min_ansible_version: 2.4
  platforms:
    - name: EL
      versions:
        - 7
  galaxy_tags:
    - myapp
dependencies: []
{% endif %}
```

Currently, you can set two template files:

- `subdir_template`: template will be deployed to the folders, tasks, handlers, defaults and meta.
  This can be used to provide a pre-configured main.yml in each of these folders.
- `root_template`: tempate will be deployed to the root of your role.
  This can be used to provide a default config for your ci system.

Templating in `ansible-roler` works only with two static jinja2 files but you can control the content
of the destination file with variables. Following variables will be automatically passed to the template
processor:

- subdir_template
  - `rolename`: these variable holds the rolename you have passed to `ansible-roler`
    If you have prefixed your role with prexix.myrole only the second part will be used.
  - `subdir`: these variable holds the current subdir which is processed at this time.
    This is a good option to add differen content to your destination file in relation to
    the current directory. You look at the usage in the build-in example above.
- root_template
  - `rolename`

There is also an option to set custom variables. These variables will be accessable throug `vars`.
This variable is an empty dictionary as long as you don't set some variables. Therefore you have to
define variables under the `template-vars' section in config file.

```INI
[template-vars]
# define some variables you want to use in your template
meta_author=John Doe
meta_license=MIT
```

Variable names will be split at the first underscore. The first part is used as the name
of a sub-dict under `vars` the other part is used as the of your variable. The result of the
these small example looks as follows:

```Python
{
  'meta': {
    'author': 'John Doe',
    'license': 'MIT'
  }
}
```

If you want to access your variables in a template, here is an example `{{ vars.meta.author }}`.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Maintainers and Contributors

[Robert Kaussow](https://github.com/xoxys)

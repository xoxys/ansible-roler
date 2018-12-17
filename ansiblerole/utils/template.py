import jinja2
import os
from ansiblerole.utils import normalize_path


def add_role(settings):
    subdirs = ['tasks', 'handlers', 'templates', 'files', 'vars', 'defaults', 'meta']
    base = normalize_path(os.path.join(settings.base_path, settings.role_name))
    os.makedirs(base)

    template_context = {
        'rolename': settings.role_name.split(".", 1)[-1],
        'vars': settings.template_vars
    }

    if settings.enable_templating and settings.root_template:
        _render_template(settings.root_template, base, template_context)

    for subdir in subdirs:
        path = os.path.join(base, subdir)
        os.makedirs(path)

        template_context.update({'subdir': subdir})
        if subdir not in ['templates', 'files', 'vars'] \
           and settings.enable_templating \
           and settings.subdir_template:
            _render_template(settings.subdir_template, path, template_context)
    return


def _render_template(file, render_dir, context):
    path, filename = os.path.split(file)
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path),
        trim_blocks=True
    )
    jinja_stream = jinja_env.get_template(filename).stream(context)
    return jinja_stream.dump(os.path.join(render_dir, filename.rsplit('.j2', 1)[0]))

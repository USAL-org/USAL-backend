import os

from jinja2 import Environment, FileSystemLoader


def render_template(template_path: str, data: dict[str, str]) -> str:
    template_dir = os.path.dirname(template_path)
    template_file = os.path.basename(template_path)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)
    rendered_template = template.render(**data)
    return rendered_template

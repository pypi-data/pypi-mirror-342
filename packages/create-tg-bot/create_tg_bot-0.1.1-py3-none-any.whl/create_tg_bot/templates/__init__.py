from jinja2 import Environment, FileSystemLoader
import os.path
import click

templates_path = os.path.join(os.path.dirname(__file__))
env = Environment(loader=FileSystemLoader(templates_path))


def create_file_from_template(project_path, template_name, **kwargs):
    template = env.get_template(template_name)
    rendered = template.render(**kwargs)

    file_name = template_name.replace(".jinja", "")
    file_path = os.path.join(project_path, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    click.echo(f"✅ File {file_path} created.")

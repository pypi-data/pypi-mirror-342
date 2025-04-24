import click
import os

from create_tg_bot.templates import create_file_from_template
from create_tg_bot.constants import ROOT_DIRS


def create_python_folder(folder_path):
    os.makedirs(folder_path)
    init_file_path = os.path.join(folder_path, "__init__.py")
    open(init_file_path, "w").close()
    click.echo(f"✅ Python folder {folder_path} created.")


def create_project_structure(project_name, project_path, token, token_dev, db_url):
    os.makedirs(project_path)
    for folder_name in ROOT_DIRS:
        folder_path = os.path.join(project_path, folder_name)
        create_python_folder(folder_path)

    create_file_from_template(project_path, "requirements.txt.jinja")
    create_file_from_template(project_path, "alembic.ini.jinja")
    create_file_from_template(project_path, ".gitignore.jinja")
    create_file_from_template(project_path, "config.py.jinja")
    create_file_from_template(project_path, "main.py.jinja")

    create_file_from_template(project_path, "migrations/script.py.mako.jinja")
    create_file_from_template(project_path, "migrations/env.py.jinja")
    os.makedirs(os.path.join(os.path.join(project_path, "migrations"), "versions"))

    create_file_from_template(project_path, "core/module_loader.py.jinja")

    create_file_from_template(project_path, "models/base.py.jinja")
    create_file_from_template(project_path, "models/User.py.jinja")
    create_file_from_template(project_path, "services/db.py.jinja")
    create_file_from_template(project_path, "crud/find_or_create_user.py.jinja")

    create_file_from_template(project_path, "commands/start.py.jinja")
    create_file_from_template(project_path, "texts/hello.py.jinja")

    create_file_from_template(
        project_path,
        ".github/workflows/ci-cd.yml.jinja",
        project_name=project_name
    )

    create_file_from_template(project_path, ".github/workflows/ci-cd.yml.jinja")

    create_file_from_template(
        project_path,
        ".env.jinja",
        token_dev=token_dev,
        token=token,
        db_url=db_url
    )

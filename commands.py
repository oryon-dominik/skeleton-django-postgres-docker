#!/usr/bin/env python3
# coding: utf-8

"""Typer cli interface to manage the dev-environment"""

import subprocess
import webbrowser
from pathlib import Path
import typer

from rich.console import Console
from rich.markdown import Markdown


#----------CONFIG--------------------------------------------------------------
cli = typer.Typer()
DEBUG = True
CWD = '.'
COMPOSE_FROM = "docker-compose.yml"
MANAGE = f"docker compose -f {COMPOSE_FROM} run django python manage.py"


# ---------HELPERS-------------------------------------------------------------
def echo(
    message: str,
    fg_color: str = typer.colors.WHITE,
    bg_color: str = typer.colors.BLACK,
    bold: bool = False
    ):
    """colors:
        "bright_" + black, red, green, yellow, blue, magenta, cyan, white
    """
    typer.echo(
        typer.style(
            message,
            fg=fg_color,
            bg=bg_color,
            bold=bold,
        )
    )

def delete_folder(path: Path):
    for element in path.iterdir():
        if element.is_dir():
            delete_folder(element)
        else:
            element.unlink()
    path.rmdir()

def clean_build():
    echo(f"Unlinking build-files: build/; dist/ *.egg-info; __pycache__;", fg_color=typer.colors.RED)
    cwd = Path(CWD)
    [delete_folder(p) for p in cwd.rglob('build')]
    [delete_folder(p) for p in cwd.rglob('*.egg-info')]
    [delete_folder(p) for p in cwd.rglob('__pycache__')]
    try:
        [delete_folder(p) for p in cwd.rglob('dist')]
    except OSError as err:
        echo(f"Error deleting dist-folder: {err}", fg_color=typer.colors.RED)

def clean_pyc():
    echo(f"Unlinking caches: *.pyc; *pyo; *~;", fg_color=typer.colors.RED)
    [p.unlink() for p in Path(CWD).rglob('*.py[co]')]
    [p.unlink() for p in Path(CWD).rglob('*~')]

def create_vital_files_and_directories():
    echo(f"Creating vital files and directories for dev:", fg_color=typer.colors.GREEN)
    echo(" ... : './logs', './media', '.envs/.production.env'", fg_color=typer.colors.GREEN)

    cwd = Path('.')
    # directories
    assets = cwd / "assets"
    logs = cwd / "logs"
    media = cwd / "backend" / "media"
    # files
    production_dotenv = cwd / ".envs" / ".production.env"

    [path.mkdir(parents=True, exist_ok=True) for path in (logs, media, assets)]
    [path.touch(exist_ok=True) for path in (production_dotenv,)]


def run_command(command, debug=False, cwd=CWD, env=None, shell=False):
    if debug:
        echo(f">>> Running command: {command}")
    try:
        subprocess.run(command.split(), cwd=cwd, env=env, shell=shell)
    except FileNotFoundError:
        echo(f'The command {command} threw a FileNotFoundError', fg_color=typer.colors.RED)


#----------GENERAL COMMANDS----------------------------------------------------
@cli.command()
def clean():
    """Cleaning pycache, buildfiles"""
    clean_build()
    clean_pyc()

@cli.command()
def black(path: str = typer.Argument(None)):
    """black <path>"""
    command = "black"
    if path is not None:
        command = f"{command} {path}"
    run_command(command, debug=DEBUG)

@cli.command()
def pytest(test_path: str = typer.Argument(None)):
    """pytest <path>"""
    command = "pytest"
    if test_path is not None:
        command = f"{command} {test_path}"
    run_command(command, debug=DEBUG)

@cli.command()
def run_coverage(skip: bool = False):
    """test coverage"""
    commands = [
        "coverage run --source=./application --module pytest",
        "coverage report -mi",
        "coverage html"
    ]
    # TODO: fixme, this is broken: commands[0] += " --skip-empty" if skip else ""
    for command in commands:
        run_command(command, debug=DEBUG)
    coverage_index_file_url = f'file://{Path("./htmlcov/index.html").resolve()}'
    webbrowser.open_new_tab(coverage_index_file_url)

@cli.command()
def coverage(skip: bool = False):
    """= run-coverage"""
    run_coverage(skip=skip)

@cli.command()
def test(test_path: str = typer.Argument(None), coverage: bool = False, skip: bool = False):
    """test --coverage"""
    if coverage:
        run_coverage(skip=skip)
    else:
        pytest(test_path)

@cli.command()
def rebuild():
    """= clean + initialize"""
    clean()
    initialize()

@cli.command()
def initialize():
    """Initialize the skeleton-application thing server..."""
    echo(f'{initialize.__doc__}...', fg_color=typer.colors.GREEN)

    # ... TODO: reset database, makemigrations, migrate

    echo(f'Successfully initialized the project...', fg_color=typer.colors.GREEN)


# ---------- ABBREVIATIONS ----------------------------------------------------
@cli.command()
def rb():
    "= rebuild"
    rebuild()

@cli.command()
def init():
    "= initialize"
    initialize()

@cli.command()
def mm():
    """= makemigrations"""
    makemigrations()

@cli.command()
def mig():
    """= migrate"""
    migrate()

@cli.command()
def mmm():
    """= makemigrations + migrate"""
    makemigrations()
    migrate()

@cli.command()
def up(orphans: bool = False):
    """= run (start the devserver)"""
    run(orphans=orphans)

@cli.command()
def serve(orphans: bool = False):
    """= run (start the devserver)"""
    run(orphans=orphans)


# ---------- INTROSPECTION ----------------------------------------------------
@cli.command()
def readme():
    """README"""
    console = Console()
    with open("README.md") as readme:
        markdown = Markdown(readme.read())
    console.print(markdown)


# ---------- MANAGE THE DATABASE ----------------------------------------------
@cli.command()
def makemigrations():
    """
    Django Makemigrations .
    """
    command = f"{MANAGE} makemigrations"
    run_command(command, debug=DEBUG)

@cli.command()
def migrate(revision: str = "head"):
    """
    Django Migrate.
    """
    command = f"{MANAGE} makemigrations"
    run_command(command, debug=DEBUG)

@cli.command()
def resetschema():
    """ deletes data in tables"""
    command = f"{MANAGE} reset_schema --noinput"
    run_command(command, debug=DEBUG)

@cli.command()
def resetdb():
    """ deletes database tables, close all sesisons if connected"""
    command = f"{MANAGE} reset_db --noinput --close-sessions"
    run_command(command, debug=DEBUG)

@cli.command()
def restore(backup_file_path: str, develop: bool = False):
    if not Path(backup_file_path).exists():
        echo(f"Backup file not found: {backup_file_path}", fg_color=typer.colors.RED)
        return
    echo(f"We STOP the running containers to restore a postgres backup!", fg_color=typer.colors.YELLOW)
    commands = [
        f"docker compose -f {COMPOSE_FROM} down",
        f"docker compose -f {COMPOSE_FROM} up -d postgres",
        f"docker compose -f {COMPOSE_FROM} exec postgres restore {backup_file_path}",
        f"docker compose -f {COMPOSE_FROM} down",
    ]
    for command in commands:
        run_command(command, debug=DEBUG)

@cli.command()
def backup():
    command = "docker compose -f {COMPOSE_FROM} run postgres backup"
    run_command(command, debug=DEBUG)

@cli.command()
def backuplist():
    command = "docker-compose -f {COMPOSE_FROM} run postgres list-backups"
    run_command(command, debug=DEBUG)


# ---------- MANAGE THE USERS -------------------------------------------------
@cli.command()
def create_user(
    superuser: bool = False,
):
    """
    Example:
    cc create-user --superuser
    """
    if superuser:
        command = f"{MANAGE} createsuperuser"
        run_command(command, debug=DEBUG)
        return
    echo(f"Can't create non-superusers via this CLI (yet?)")

# ---------- MANAGE THE SERVER -------------------------------------------------
@cli.command()
def shell():
    """
    Open a shell in the server container.
    """
    command = f"{MANAGE} shell"
    run_command(command, debug=DEBUG)

@cli.command()
def run(orphans: bool = False):
    """
    Run the dev server.

    Via docker.

    """
    command = f"docker compose {COMPOSE_FROM} up"
    if orphans:
        command += " --remove-orphans"
    run_command(command, debug=DEBUG)

@cli.command()
def down():
    command = "docker compose down"
    run_command(command, debug=DEBUG)

@cli.command()
def rebuild(nocache: bool = False, static: bool = False):
    clean_build()
    clean_pyc()
    create_vital_files_and_directories()
    run_command("poetry install", debug=DEBUG)
    build(nocache=nocache)
    initialize(static=static)

@cli.command()
def build(nocache: bool = False):
    command = "docker compose build"
    if nocache:
        command = f"{command} --no-cache"
    run_command(command, debug=DEBUG)

@cli.command()
def collectstatic():
    command = f"{MANAGE} collectstatic --noinput --clear --verbosity 0"
    echo(f'Collecting static files and clearing the old clutter.. ', fg_color=typer.colors.GREEN)
    run_command(command, debug=DEBUG)
    echo(f'Staticfiles collected.', fg_color=typer.colors.GREEN)

@cli.command()
def initialize(static: bool = False):
    """Initializing things"""
    echo(f'{initialize.__doc__}...', fg_color=typer.colors.GREEN)
    if static or not Path("staticfiles").exists():
        echo(f'Collecting staticfiles...', fg_color=typer.colors.GREEN)
        collectstatic()

    echo(f"WARNING: Reset the database... (Don't do this in production)", fg_color=typer.colors.RED)
    resetdb()
    echo(f'Makemigrations...', fg_color=typer.colors.GREEN)
    makemigrations()
    echo(f'Migrate...', fg_color=typer.colors.GREEN)
    migrate()

    echo(f'Creating pytest DB and running TESTS...', fg_color=typer.colors.GREEN)
    run_command("pytest --quiet --create-db", debug=DEBUG)

    echo(f'Successfully initialized the project...', fg_color=typer.colors.GREEN)


if __name__ == "__main__":
    cli()

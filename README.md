# README

## installation

1. clone the repo, delete .git, create a new git repo
2. setup name & description in `pyproject.toml`
3. setup `.env` (debug=on)
4. replace `thing` and `Thing` (even the foldernames apps/`things`/templates/`things`) to better suit your app
5. switch to a shell in your venv (e.g: `poetry shell`)
6. `poetry install`
7. `docker-compose build`
8. `docker-compose -f docker-compose.yml run --rm django python manage.py makemigrations`
9. `docker-compose -f docker-compose.yml run --rm django python manage.py migrate`
10. start all containers with `docker-compose up`
11. happy-coding

## notebooks

to start a notebook `docker-compose up notebook`

## production

fix the settings in settings.py, don't use the `.env`

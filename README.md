# README

## installation

1. clone the repo, delete .git, create a new git repo
2. setup name & description in `pyproject.toml`
3. rename and config your `sekeleton.code-workspace` settings
4. create `logs/requests.log` and setup `.env` (debug=on)
5. replace `thing` and `Thing` (even the foldernames apps/`things`/templates/`things`) to better suit your app
6. `docker-compose build`
7. `docker-compose -f docker-compose.yml run --rm django python manage.py makemigrations`
8. `docker-compose -f docker-compose.yml run --rm django python manage.py migrate`
9. start all containers with `docker-compose up`
10. happy-coding

## notebooks

to start a notebook `docker-compose up notebook`

## production

fix the settings in settings.py, don't use the `.env`

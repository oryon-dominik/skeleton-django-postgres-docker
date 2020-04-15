# README

## installation

1. clone the repo, delete .git, create a new git repo
2. setup name & description in `pyproject.toml`
3. `poetry install`
4. rename and config your `sekeleton.code-workspace` settings
5. create `logs/requests.log` and setup `.env` (debug=on)
6. replace `thing` and `Thing` (even the foldernames apps/`things`/templates/`things`) to better suit your app
7. `python manage.py makemigrations`
8. `python manage.py migrate`
9. happy-coding

## notebooks

to work with notebooks, set
`DJANGO_ALLOW_ASYNC_UNSAFE=true` in your `.env`

to start a notebook `.\manage.py shell_plus --notebook`

## production

fix the settings in settings.py, don't use the `.env`

## for docker, postgreSQL, redis & celery see the more advanced skeleton (still tba)

#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -o errexit

# The return value of a pipeline is the status of the last command to exit with
# a non-zero status, or zero if no command exited with a non-zero status
set -o pipefail

# Treat unset variables as an error when substituting.
set -o nounset

# Print commands and their arguments as they are executed.
set -o xtrace

# prepare the environment
cd /app
python manage.py migrate

# production start via gunicorn
# mkdir -p ./staticfiles
# python manage.py collectstatic --noinput
# gunicorn config.wsgi:application --bind 0.0.0.0:8000 --timeout 300

# develop start via runserver_plus
while true; do
  echo "Re-starting Django runserver"
    # regular start
  # python manage.py runserver 0.0.0.0:8000

  # django-extensions start
  python manage.py runserver_plus 0.0.0.0:8000
done

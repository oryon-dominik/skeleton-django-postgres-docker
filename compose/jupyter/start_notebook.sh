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


JUPYTER_CONFIG_DIR="/app/.ipython" && python manage.py shell_plus --notebook

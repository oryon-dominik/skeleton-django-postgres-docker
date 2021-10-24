FROM python:3.10-slim

# ---- SYSTEM & BUILD-REQUIREMENTS --------------------------------------------
RUN export DEBIAN_FRONTEND=noninteractive && \
    # get rid of ERROR: debconf: unable to initialize frontend: Dialog
    # upgrade the system
    apt-get update && apt-get --quiet --assume-yes dist-upgrade && \
    # install build requirements
    # - build-essential: dependencies for building Python packages
    # - git: to be able to install modules directly from github
    # - libffi-dev: to successfully build wheels for cffi (poetry dependency)
    # - libpq-dev: to successfully build psycopg2
    # - postgresql-client: postgres client psql for python manage.py dbshell
    # - curl: poetry dependency
    apt-get update && apt-get --quiet --assume-yes install build-essential git libffi-dev libpq-dev postgresql-client curl

# Cleaning up unused files
RUN apt-get purge --assume-yes --auto-remove --option APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# ---- USER CREATION ----------------------------------------------------------
# Edit these lines, to match the groups for your server, to have consistent user + group-ids. This enhances security.
ARG USER=thing
ARG USERID=1010
ARG GROUPID=1010

RUN groupadd --system --gid $GROUPID $USER \
    && useradd --system --uid $USERID --gid $GROUPID --create-home $USER

# Switch to the current user
USER $USER

# ---- APPLICATION ------------------------------------------------------------
WORKDIR /app
# Transfer ownership of the application to the user
RUN chown -R $USER:$GROUPID /app

# Add container's scripts
# Django
COPY --chown=$USER:$USER ./compose/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY --chown=$USER:$USER ./compose/django/start.sh /start.sh
RUN chmod +x /start.sh

# Jupyter notebook
RUN mkdir --parents /app/.ipython
COPY --chown=$USER:$USER ./compose/jupyter/jupyter_notebook_config.py /app/.ipython
COPY --chown=$USER:$USER ./compose/jupyter/start_notebook.sh /start_notebook.sh
RUN chmod +x /start_notebook.sh

# ---- PYTHON -----------------------------------------------------------------
# Application python requirements
COPY --chown=$USER:$USER poetry.lock pyproject.toml /app/

# Force the python stdout and stderr streams to be unbuffered. (send to terminal, not written)
ENV PYTHONUNBUFFERED 1
ENV PATH=/usr/local/bin/:$PATH

# Just to make sure we're on current pip
RUN python -m pip install --upgrade --user pip

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH=/home/$USER/.local/bin/:$PATH
# BUG: poetry completions need sudo privileges
# RUN user/local/bin/poetry completions bash > /etc/bash_completion.d/poetry.bash-completion

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry config  virtualenvs.path .venv \
    && poetry config  virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi --no-root  # $(test ! "$DEBUG" && echo "--no-dev")

ENTRYPOINT ["/entrypoint.sh"]

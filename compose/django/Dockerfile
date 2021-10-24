FROM python:3.10-slim

# Set development mode. (poetry packages install..)
ARG DEBUG=true

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
    apt-get update && apt-get --quiet --assume-yes install build-essential git libffi-dev libpq-dev postgresql-client


# ---- USER CREATION ----------------------------------------------------------
# Edit these lines, to match the groups for your server
ARG USER=thing
ARG USERID=1010
ARG GROUPID=1010

RUN groupadd --system --gid $GROUPID $USER \
    && useradd --system --uid $USERID --gid $GROUPID --create-home $USER

# ---- APPLICATION ------------------------------------------------------------
# Add container's scripts
# Django
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed --in-place 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chown $USER:$GROUPID /entrypoint.sh

COPY ./compose/django/start.sh /start.sh
RUN sed --in-place 's/\r//' /start.sh
RUN chmod +x /start.sh
RUN chown $USER:$GROUPID /start.sh

# Jupyter notebook
RUN mkdir --parents /root/.jupyter
COPY ./compose/jupyter/jupyter_notebook_config.py /app/.ipython
COPY ./compose/jupyter/start_notebook.sh /start_notebook.sh
RUN sed --in-place 's/\r//' /start_notebook.sh
RUN chmod +x /start_notebook.sh

# ---- PYTHON -----------------------------------------------------------------
# Application python requirements
COPY poetry.lock pyproject.toml /app/

# Force the python stdout and stderr streams to be unbuffered. (send to terminal, not written)
ENV PYTHONUNBUFFERED 1

# Just to make sure we're on current pip
RUN python -m pip install --upgrade --user pip

# Install Poetry
RUN apt-get update && apt-get install --no-install-recommends -y curl \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
RUN root/.local/bin/poetry completions bash > /etc/bash_completion.d/poetry.bash-completion
ENV PATH=root/.local/bin/:$PATH

RUN python -m ipykernel install --user --name $USER --display-name $USER

# Cleaning up unused files
RUN apt-get purge --assume-yes --auto-remove --option APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
RUN /root/.local/bin/poetry config virtualenvs.create false \
    && /root/.local/bin/poetry install $(test ! "$DEBUG" && echo "--no-dev") --no-interaction --no-ansi --no-root

# Transfer ownership of the application to the user
RUN chown -R $USER:$GROUPID /app

# Switch to the current user
USER $USER

ENTRYPOINT ["/entrypoint.sh"]

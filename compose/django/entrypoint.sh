#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -o errexit

# The return value of a pipeline is the status of the last command to exit with
# a non-zero status, or zero if no command exited with a non-zero status
set -o nounset

cmd="$@"

# the official postgres image uses 'postgres' as default user if not set explictly.
if [ -z "${POSTGRES_USER}" ]; then
    base_postgres_image_default_user='postgres'
    export POSTGRES_USER="${base_postgres_image_default_user}"
fi

if [ -z "$POSTGRES_DB" ]; then
    echo "env: POSTGRES_DB not set"
    exit 1
fi

if [ -z "$POSTGRES_PASSWORD" ]; then
    echo "env: POSTGRES_PASSWORD not set"
    exit 1
fi

if [ -z "$POSTGRES_HOST" ]; then
    echo "env: POSTGRES_HOST not set"
    exit 1
fi

if [ -z "$POSTGRES_PORT" ]; then
    echo "env: POSTGRES_PORT not set"
    exit 1
fi

if [ -z "$DATABASE_URL" ]; then
    export DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB
fi


function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect("$DATABASE_URL")
    # install pg-extensions like this:
    # cur = conn.cursor()
    # cur.execute("create extension IF NOT EXISTS pg_trgm;")
    # cur.execute("select * from pg_extension;")
    # cur.fetchone()
    # conn.commit()
except psycopg2.OperationalError as e:
    sys.exit(-1)
sys.exit(0)

END
}

until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available... starting django'

exec "$@"

# README

## Installation

The repository setup.

1. Use this [repo as a template](https://github.com/oryon-dominik/skeleton-django-postgres-docker/generate) for your own, then clone it `git clone <repository-address> <target>`.
2. Setup name & description in `pyproject.toml`. If you're using vscode (like me) rename and customize the `skeleton.code-workspace` to suit your needs.
3. Create a dotenv `touch ./.envs/.production.env` where the projects environment variables will get set to. (you may use the example `cp ./.envs/.production.example.env ./.envs/.production.env`).
4. For dependency-management I use [poetry](https://python-poetry.org/). If poetry is installed, install the dependencies with `poetry install`.
5. Activate the venv just created with `poetry shell` or `workon <venv-name>` (I recommend using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)).

The django-part, using docker-containers.

After you've built the containers with a `docker compose build` you can exec all neccessary commands.

> `docker compose run django <command>`

Commands:

6. Create migrations for your models `python manage.py makemigrations` (repeat this anytime you change your models).
7. Apply the migrations to the database `python manage.py migrate`.
8. If you need an adminuser also create it with `python manage.py createsuperuser`.

We can use notebooks for an easy access to an interactive django-shell. (To debug, develop or create model-instances on the fly)  

> `docker compose up` exposes the application server on localhost:8000 and a notebook on localhost:8888.

Happy coding =)


## Management Commands

I'm aliasing `python commands.py` -> `cc` to *call* management *commands* in all my projects.  
It's a CLI interface using the python library `typer`. All available commands are defined in `commands.py`  
(Trivia: I'm never aliasing `gcc` or any other c-compilers to `cc`, so: no conflicts here).  

`cc up`: start all containers.  
`cc rebuild`: re-build the containers. Neccessary, if you added a package via poetry.  
`cc shell`: if the server is already running, you can debug your application in a django-db-shell. `from apps.users.models import User; User.objects.all()`  

There are also some abbreviations available.
`cc mmm`: _makemigrations_ & _migrate_. 

Look up all other control-commands for the project via `cc --help` or glimpse into the `commands.py` yourself.  

Example implementation of the `cc <command>` alias in a `powershell` script:

    ```powershell
    function cc () {
        $commands = ".\commands.py"
        $cwd = (Get-Location)
        $parent = Split-Path -Path $cwd
        if (Test-Path $commands -PathType leaf) {
            python commands.py $args
        }
        elseif (Test-Path (Join-Path -Path $parent -ChildPath $commands) -PathType leaf) {
            Set-Location $parent
            python commands.py $args
            Set-Location $cwd
        }
        else {
            Write-Host "commands.py not found" 
        }
    }
    ```

## other skeletons

[django minimal sqlite](https://github.com/oryon-dominik/skeleton-django-sqlite-minimal)  
[django with postgres & docker](https://github.com/oryon-dominik/skeleton-django-postgres-docker) (this repo)  
[fastAPI](https://github.com/oryon-dominik/skeleton-fastapi)  

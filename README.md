# README

## Dependencies

Dependencies are managed via [poetry](https://python-poetry.org/) and a `pyproject.toml`.


## Installation

1. Setup project's name & description in the `pyproject.toml`
2. Setup `.envs/.production.env`
3. Replace `thing` and `Thing` (even the foldernames apps/`things`/templates/`things`) to better suit your app
4. Install dependecies and build the docker container (`poetry install`, `docker compose build`).
5. Use my management commands: `cc up`.


## Notebooks

To start a notebook `docker-compose up notebook`


## Management Commands

I'm using an easy management alias `cc` for all my projects. Easy control-commands for the project using the python library `typer` (trivia: I'm never aliasing `gcc` or any other c-compilers to `cc`). All available commands are defined in `commands.py`  

Example:

    python commands.py up
    # after adding the alias will be executed as:
    cc up

For a full list of commands just run `commands.py --help` (`cc --help`) or glimpse into the file itself.  
To implement the `cc <command>` alias with powershell:

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

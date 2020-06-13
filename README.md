# Website

Minimalist website.

<https://scrub000.herokuapp.com/>

## Installing

### Pre-requisites

- Install Git
- Install Python 3
- Install PostgreSQL
- Install the `invoke` Python package
  - `pip install --user invoke`
- Clone this repository
  - `git clone https://github.com/scrub000/website.git && cd website`

### Steps

- Set up virtual environment
  - `python3 -m venv .env`
  - `source .env/bin/activate`
- Install all dependencies
  - `inv install`
- Configure environment variables
  - `vim src/website/.env`
- Launch website
  - `inv run` (`--prod` for production), or
  - `FLASK_APP=src/website/ flask run`, or
  - `python3 src/wsgi.py`

## Developing

### Pre-requisites

- Follow all steps in the 'Installing' section
- Install the development packages
  - `inv install --dev`, or
  - `inv install-python-deps --dev`

### Notes

- When testing emails, ensure you have the default mail environment settings, then run:
  - `inv run-debug-mail-server`

### Tools

- Run Flask shell
  - `FLASK_APP=src/website/ flask shell`
- Create database migration file
  - `FLASK_APP=src/website/ flask db migrate -m "Describe change here"`

### Testing and linting

- Run black linting
  - `inv run-python-black-linter`
- Run isort linting
  - `inv run-python-isort-linter`
- Run flake8 linting
  - `inv run-python-flake8-linter`
- Run unit tests
  - `inv run-unit-tests`
- Run integration tests
  - `inv run-integration-tests`
- Run functional tests
  - `inv run-functional-tests`

### Integrated Development Environment settings

Potentially useful settings for development.

#### Visual Studio Code

`.vscode/settings.json` - for general development.

```json
{
    "[python]": {
        "editor.rulers": [79],
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },

    "python.pythonPath": ".env/bin/python3",
    "python.linting.enabled": true,
    "python.linting.lintOnSave": true,
    "python.linting.ignorePatterns": [
        ".env/*.py",
        "migrations/*.py"
    ],

    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": ["--load-plugins", "pylint-flask"],

    "python.formatting.provider": "black",
    "python.formatting.blackArgs": [
        "-l",
        "79"
    ],
}
```

`.vscode/launch.json` - for debugging.

```json
{
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "src/wsgi.py",
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "0"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true
        }
    ]
}
```

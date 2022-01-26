# safe-config-service

[![Coverage Status](https://coveralls.io/repos/github/gnosis/safe-config-service/badge.svg)](https://coveralls.io/github/gnosis/safe-config-service)

The `safe-config-service` is a service that provides configuration information in the context of the Safe clients environment (eg.: list of available safe apps and chain metadata).

## Requirements

- `docker-compose` – https://docs.docker.com/compose/install/
- Python 3

## Setup

### 1. Configuration

The environment variables are set via the `.env` file. The configuration in `.env.example` is meant to be production ready. You can copy it and adjust it to your development needs (refer to the file for the explanation about each environment variable).

```shell
cp .env.example .env
```

**Important:** Some variables are required to be set before running the application: `SECRET_KEY`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.
They can be set either locally on your environment or (as a provided example) by uncommenting these variables from the `.env` file.

### 2. Running the service image

The project relies on `nginx` and `postgres` services. If you are running this locally this is already set in the `docker-compose.yml` file:

```shell
docker compose up
```

The service will then be available under `localhost:$NGINX_HOST_PORT`.

## Development

If you wish to develop locally without running an image for the Django service you can do the following:

1. Install the required Python dependencies. Eg.: With a python virtual environment:

```shell
python -m venv venv # creates a virtual environment venv in the local directory
source venv/bin/activate
pip install -r requirements-dev.txt
```

2. Export the environment variables of `.env` to the local shell/environment (some [shells](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) might require you to `allexport` before doing that)

```shell
source .env
```

3. Run a PostgreSQL database locally. Check your `.env` to see the user, host and port details which are expected by the Django application.
You can also run the bundled Postrges image with Docker.
   
```shell
docker-compose up -d db # postgres will be listening on port $POSTGRES_PORT
```

4. Launch the service:

```shell
python src/manage.py runserver
```


#### b) with Docker

1. Override the docker-compose for local development – by default the Django application won't reload when the codebase changes (restarting the images is required).
In order to see our changes without restarting the docker images:
   
```shell
cp docker-compose.override.yml.example docker-compose.override.yml
```

2. Set the mount point to `/app` in the `.env` file

```dotenv
DOCKER_WEB_VOLUME=.:/app
```

You need to configure the network that you want to use also. You can create it manually by running this command:
```cmd
docker network create moonbase-net # or whatever name than you want
```

After that edit the env file.
```dotenv
DOCKER_NETWORK_NAME=moonbase-net
```

3. Launch images

```shell
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```
or 
```shell
./run up
```

This will start the Nginx proxy server, the `safe-config-service` and a postgres database. Nginx exposes the port `8080` to the host which is the port used to interact with the application.

Once you have the images up and running the service can be reached via `localhost:8080`.

4. `./run` script

The `./run` script is meant to be used as an utility to interact with the running image. You can execute `./run help` to see the available commands.

Example: if you want to issue a command to the image which is running the Django service from your host you can do the following:

```shell
./run manage <django-command>
```

5. If it's the first time that you build the container it's probable that there is a need to load the chain's information into the database.

```shell
./run loadchain
```

## Development Tools

The project uses a variety of tools to make sure that the styling, health and correctness are validated on each change.
These tools are available via `requirements-dev.txt` so to have them available in your virtual environment run:

```shell
pip install -r requirements-dev.txt
```

### Testing

Pytest is used to run the available tests in the project. **Some of these tests validate the integration with the database
so having one running is required** (you can have one running in the background with `docker compose up -d db`). From the project root:

```shell
pytest src
```

### Code Style Formatter and Linter

[Black](https://black.readthedocs.io/en/stable/), [Flake8](https://flake8.pycqa.org/en/latest/) and [isort](https://pycqa.github.io/isort/) are the tools used to validate the style of the changes being pushed. You can refer to the documentation
of these tools to check how to integrate them with your editor/IDE.

```shell
isort --profile black src # sorts imports according to the isort spec with a profile compatible with Black
black src # formats the files in the src folder using Black
flake8 src # runs flake8 Linter in the src folder
```

There's also a pre-commit hook that you can install locally via `pre-commit` so that it formats the files changed on each commit automatically:

```shell
pre-commit install # installs commit hook under .git/hooks/pre-commit
git commit # Initially this can take a couple minutes to setup the environment (which will be reused in following commits)
```

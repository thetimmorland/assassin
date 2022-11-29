# Assassin

Assassin is a web app created to facilitate a building-wide game of
[Assassin](https://en.wikipedia.org/wiki/Assassin_(game)) in Queen's
University's largest residence building: Victoria Hall.

The app is written in Python using Flask and SQLite. Authentication is
implemented using single sign-on with Azure AD. Deployments and monitoring are
handled with docker-compose.

## Development

```sh
# install dependencies
$ poetry install
# activate virtual environment
$ poetry shell
# run tests/checks
$ ./scripts/check
# format code
$ ./scripts/fmt
# setup environment variables
$ cp example.env .env
# run development server
$ flask --debug --app assassin run
# run production server localy
$ docker-compose up --build
```

## Deployment

Deployments are handled by `./scripts/prod` which is a thin wrapper around
docker-compose.

```sh
# setup environment variables
$ cp example.env prod.env
# set remote host
export PROD_DOCKER_HOST=ssh://user@example.com
# build script
./scripts/prod up --build -d
# initialize database
./scripts/prod exec assassin flask --app assassin init-db
# monitor logs
./scripts/prod logs -f
```

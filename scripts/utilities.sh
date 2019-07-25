#!/usr/bin/env bash
DIRECTORY="$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

ROOT_DIRECRORY=$(dirname $DIRECTORY)

# colors
red=$(tput setaf 1)
green=$(tput setaf 76)
tan=$(tput setaf 3)

success() {
  printf "${green}===> %s${reset}\n" "$@"
}

error() {
  printf "${red}===> %s${reset}\n" "$@"
}

warning() {
  printf "${tan}===> %s${reset}\n" "$@"
}

function addEnvFile() {
    ENV_FILE=$ROOT_DIRECRORY/.env
    SAMPLE_ENV_FILE=$ROOT_DIRECRORY/.env.sample
    warning "Adding .env file to django project directory"
    echo " "

    if [ ! -f "$ENV_FILE" ]; then
        cat $SAMPLE_ENV_FILE > $ENV_FILE
        success "Environment file has been created successfully"
        return
    fi

    warning "Skipping, Environment file already exist"
}

function isActivate() {
  if [[ "$VIRTUAL_ENV" != "" ]]
  then
    success "virtualenv is activated"
    return
  else
    error "run source virtualenv/bin/activate first"
    return
  fi
}

function create_venv() {
  if [ -d "virtualenv" ]; then
    success "virtualenv is already created"
    return
  else
    virtualenv virtualenv
    return
  fi
}

function create_db() {
  if psql -lqt | cut -d \| -f 1 | grep -qw airtech_development; then
    warning "Running database migrations"
	  flask db upgrade
  else
    warning "Creating 'airtech_development' postgres database"
	  createdb airtech_development

    warning "Running database migrations"
	  flask db upgrade
  fi
  success "SUCCESS: DB Migrations"
}

function create_test_db() {
  if psql -lqt | cut -d \| -f 1 | grep -qw airtech_test; then
    success "test db created"
  else
    warning "Creating 'airtech_test' postgres database"
	  createdb airtech_test
    success "test db created"
  fi
}


"$@"

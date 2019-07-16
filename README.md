[![Build Status](https://travis-ci.org/victorjambo/airtech.svg?branch=master)](https://travis-ci.org/victorjambo/airtech)
[![Coverage Status](https://coveralls.io/repos/github/victorjambo/airtech/badge.svg?branch=master)](https://coveralls.io/github/victorjambo/airtech?branch=master)

## Airtech Flight Booking API

Flight Booking System

# Description
Company Airtech has had their challenges using spreadsheets to manage their flight booking system. They are ready to automate their processes with an application and have reached out to you to build a flight booking application for the company.

## Key Application features
  • log in
  • upload passport photographs
  • book tickets
  • receive tickets as an email
  • check the status of their flight
  • make flight reservations
  • purchase tickets

## Development set up
- Check that python 3 is installed:
    ```
    python --v
    >> Python 3.7
    ```

- Install virtualenv:
    ```
    pip install virtualenv
    ```

- Check pipenv is installed:
    ```
    virtualenv --version
    >> 16.6.0
    ```

- Check that postgres is installed:
    ```
    postgres --version
    >> postgres (PostgreSQL) 11.4

    ```

- Clone the airtech-api repo and cd into it:
    ```
    git clone https://github.com/victorjambo/airtech

    ```

- Create and activate the virtualenv:
    ```
    virtualenv virtualenv && source virtualenv/bin/activate
    ```

- Install dependencies:
    ```
    pip install -r requirements.txt
    ```

- Rename the .env.sample file to .env and update the variables accordingly:
    ```
    FLASK_ENV = "development" # Takes either development, production, testing
    DATABASE_URI = "postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@YOUR_HOST/YOUR_DATABASE_NAME" # Development and production postgres db uri
    TEST_DATABASE_URI = "postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@YOUR_HOST/YOUR_TEST_DATABASE_NAME" # Testing postgres db uri
    ```

- Apply migrations:
    ```
    flask db upgrade
    ```

- If you'd like to seed initial data to the database:
    ```
    flask seed_database
    ```

- Run the application:
    ```
    flask run
    ```

- Should you make changes to the database models, run migrations as follows
    - Migrate database:
        ```
        flask db migrate
        ```

    - Upgrade to new structure:
        ```
        flask db upgrade
        ```

- Deactivate the virtual environment once you're done:
    ```
    exit
    ```

## Running the API

Manually Test the endpoints with postman

<!-- TODO: Change url to hosted documentation -->
[![Postman](https://run.pstmn.io/button.svg)](https://www.getpostman.com/apps)

**EndPoint** | **Functionality**
--- | ---
POST `/api/v1/users` | Creates a user account
GET `/api/v1/users` | List users
PUT `/api/v1/users` | Update Password or username
POST  `/api/v1/flights` | Creates a flight
PUT `/api/v1/flights/<flight_id>` | Updates a flight
DELETE `/api/v1/flight/<flight_id>` | Remove a flight
GET  `/api/v1/flights` | List flights
GET  `/api/v1/flights/<flight_id>` | Get a flight
POST  `/api/v1/flights/<flight_id>/tickets` | Create ticket on a flight
GET  `/api/v1/flights/<flight_id>/tickets` | Get tickets for a flight


## Testing

To run your tests use

```bash
$ pytest
```

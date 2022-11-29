[![Build Status](https://github.com/dominikheinisch/swapi_explorer/actions/workflows/CI_test.yml/badge.svg)](https://github.com/dominikheinisch/swapi_explorer/actions/workflows/CI_test.yml)

## The Solution

SWAPI is currently down, so I used a mirror: https://swapi.dev/

### Main features
- Fetching data from SWAPI (combined people and planets data)
- Displaying list of fetched files 
- Displaying data from file, `Load more` button
- Displaying counted data from file, buttons for choose 
- Displaying partially loaded file (file is accessible immediately after clicking `Fetch`, just access main page again)
- Using pagination
- Using async requests (grequest), default 10 requests at a time
- Using generators for batch of requests processing (batch is saved to file, before fetching next one)
- Dev and Prod configurations

### Main technologies
- Django
- PostgreSQL
- petl


## Docker

Setup and run the environment:
```
make build
make up
```
Access: http://127.0.0.1:8000/

Run test:
```
make pytest
```
Prod is a default, use `DEV=true` to run using Dev config, eg.:
```
make build DEV=true
make up DEV=true
```


## Locally

### Prerequisites
Python 3.8, Virtualenv, sqlite

### Setup & Run
Setup:
```
git clone
cd swapi_explorer
virtualenv venv
source venv/bin/activate
cd swapi_explorer
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
```
Run the server:
```
python3 manage.py runserver
```
Access: http://127.0.0.1:8000/

Run test:
```
python -m pytest -v -s
```
Run flake8:
```
flake8 .
```


## Github Action

Running flake8 and tests:
https://github.com/dominikheinisch/swapi_explorer/actions/workflows/CI_test.yml


## TODOs and improvement:

- Create REST API (currently using templates for simplicity)
- Improve ETL strategy, especially planet/homeland storing (I considered use of noSQL, but thought it would be over engineering)
- Celery for background jobs (like fetching, processing files, etc.)
- Errors handling (connection fail, api change, etc.)
- Loading files partially (n/a for aggregation)
- Improve testing, add view testing, coverage
- Add logging
- Add Sentry

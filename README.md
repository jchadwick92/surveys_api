# surveys_api
A simple API built using Python, Django and Django-Rest-Framework

## Quickstart
Follow these steps in order to run the application:
- `$ git clone git@github.com:jchadwick92/surveys_api.git`
- `$ cd surveys_api`
- `$ python3 -m venv venv`
- `$ source venv/bin/activate`
- `$ python -m pip install --upgrade pip`
- `$ pip install -r requirements.txt`
- `$ python manage.py makemigrations surveys`
- `$ python manage.py migrate`
- `$ python manage.py runserver`

## Testing
In order to run the tests for the application run
`$ python manage.py test`

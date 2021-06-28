set FLASK_ENV=development

set FLASK_APP=app.py
fl
flask run

## create a migration repository
flask db init

## add a migrations folder to your application
flask db migrate -m "Initial migration."

## apply the migration to the database
flask db upgrade

$ flask db stamp head
$ flask db migrate
$ flask db upgrade
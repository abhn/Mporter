web: gunicorn app:app --log-file -
release: flask db upgrade
heroku ps:scale web=1
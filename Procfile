release: chmod u+x release.sh && ./release.sh
web: gunicorn app:app --log-file -
heroku ps:scale web=1
web: gunicorn config.wsgi --log-file -
celery: celery worker -A config -l info -c 4
web: python manage.py collectstatic --noinput && python manage.py migrate && gunicorn safezone_project.wsgi --bind 0.0.0.0:$PORT --workers 2 --threads 4

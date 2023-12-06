web: gunicorn barkbuddies.wsgi
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn barkbuddies.wsgi

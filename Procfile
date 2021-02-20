release: python manage.py migrate
config:set DISABLE_COLLECTSTATIC=1
web: gunicorn src.token_server.wsgi
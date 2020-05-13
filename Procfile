web: gunicorn instagram_clone_django.wsgi --log-file -
worker1: celery worker -A instagram_clone_django --beat -l info --pool=solo

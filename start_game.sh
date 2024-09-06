python manage.py runserver
celery -A game_server worker -l info --pool=solo
celery -A game_server beat -l info
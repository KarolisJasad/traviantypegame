# traviantypegame
Work in progress
Travian inspired game(Mostly a clone, just trying out django capabilities)
# Requirements
Redis: https://redis.io/download/
Django
Celery
Django-Celery-Beat
Django-Celery-Results
# Installation/Running
1. py -m venv venv
2. venv\scripts\activate
3. pip install redis
4. pip install django
5. pip install django-celery-beat
6. pip install django-celery-results
7. cd travian_project
8. py manage.py makemigrations
9. py manage.py migrate
10. py manage.py createsuperuser
11. Open 3 different terminals pathed to travian_project
11.1. python manage.py runsever
12.2. celery -A travian_project.celery worker --pool=solo -l info
13.3. celery -A travian_project.celery beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

Currently you have to go to admin panel and make a village through there and all the functionalities that are included now will work then.

# Working Functions
1. Creating new buildings(Only superuser/staff)
2. Resource building/upgrading(Limited to 4 buildings of each resource).
3. Resource generation each second according to your resource buildings and their level.
4. Infrastructure building/upgrading(Increased capacity of resource you can have based on building level)

# TO-DO List
Fix Design to be more friendly/prettier
Make a village creation screen after registration/ask to make a village if user skips village creation
Add more functionalities.
Priority:
1. Baracks/Stable building
2. Allow troops building in each building(Atleast 2 kind of troops in each)
3. Player list/attacking players(Taking resources away from enemy if succeeded)
4. Bug fixing/debuging


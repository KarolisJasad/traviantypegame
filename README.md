# traviantypegame
Work in progress
Travian inspired game(Mostly a clone, just trying out django capabilities)
# Requirements
Redis: https://redis.io/download/ /
Django /
Celery /
Django-Celery-Beat /
Django-Celery-Results /
# Installation/Running 
1. py -m venv venv
2. venv\scripts\activate
3. pip install redis
4. pip install django
5. pip install celery
6. pip install django-celery-beat
7. pip install django-celery-results
8. cd travian_project
9. py manage.py makemigrations
10. py manage.py migrate
11. py manage.py createsuperuser
12. Open 3 different terminals pathed to travian_project
12.1. python manage.py runsever
12.2. celery -A travian_project.celery worker --pool=solo -l info
12.3. celery -A travian_project.celery beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

Currently you have to go to admin panel and make a village through there and all the functionalities that are included now will work then.

# Working Functions
1. Creating new buildings(Only superuser/staff)
2. Resource building/upgrading(Limited to 4 buildings of each resource).
3. Resource generation each second according to your resource buildings and their level.
4. Infrastructure building/upgrading(Increased capacity of resource you can have based on building level)
5. Baracks/Stable building
6. Allow troops building in each building(Atleast 2 kind of troops in each)
7. Player list/attacking players(Taking resources away from enemy if succeeded)

# TO-DO List
Fix Design to be more friendly/prettier
Make a village creation screen after registration/ask to make a village if user skips village creation
Add more functionalities.
Priority:
1. Bug fixing/debuging
2. Design
3. Add time based constructions/troop building
4. Add more functionalities


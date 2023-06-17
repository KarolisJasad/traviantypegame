import os
from celery import Celery
from django.db.models import F

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travian_project.settings')

app = Celery('travian_project')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Configure Celery settings...

app.conf.update(
    # Broker URL
    broker_url='redis://localhost:6379/0',

    # Result backend (set to None if you don't use any)
    result_backend=None,

    # Number of worker processes (adjust as needed)
    worker_concurrency=1,

    # Additional configuration options...
)

if __name__ == '__main__':
    app.start()
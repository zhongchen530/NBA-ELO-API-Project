from __future__ import absolute_import,unicode_literals
from celery import shared_task
from NBA.update import Update

@shared_task
def update_date():
    Update.update_data()

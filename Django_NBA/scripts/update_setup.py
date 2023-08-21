from django_celery_beat.models import PeriodicTask, IntervalSchedule
from NBA.update import Update


# executes every 3600 seconds.
def run():
    print("Updating ranking")
    Update.update_player_ranking()
    Update.update_team_ranking()
    print("Update setup finished")
    
    if PeriodicTask.objects.filter(name = "update database"):
        return
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=300,
        period=IntervalSchedule.SECONDS,
    )

    update_task = PeriodicTask.objects.create(
        interval=schedule,                  # we created this above.
        name='update database',          # simply describes this periodic task.
        task='NBA.tasks.update_data',  # name of task.
    )

    update_task.save()


from celery import shared_task


@shared_task
def cron_synchro():
    print("test synchro beat")

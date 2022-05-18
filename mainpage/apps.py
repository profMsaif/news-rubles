from django.apps import AppConfig


class MainpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainpage'

    def ready(self):
        print("start schedule ...")
        from mainpage_schedule import mainpage_scheduler
        mainpage_scheduler.start()

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Отобразить текст'

    def handle(self, *args, **kwargs):
        self.stdout.write("Welcome!")
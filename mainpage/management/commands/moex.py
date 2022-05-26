from django.core.management.base import BaseCommand
from mainpage.all_parsers.parsers import Currency, Resources
from mainpage.all_parsers import parsers
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.conf import settings
from django_apscheduler.util import close_old_connections

MOEX_USD_PARSER = parsers.MoexCurrencyExchangeRateParser(Currency.usd, Resources.moex)
MOEX_EUR_PARSER = parsers.MoexCurrencyExchangeRateParser(Currency.eur, Resources.moex)
CB_USD_PARSER = parsers.CbCurrencyExchangeRateParser(Currency.usd, Resources.cb)
CB_EUR_PARSER = parsers.CbCurrencyExchangeRateParser(Currency.eur, Resources.cb)


@close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            MOEX_USD_PARSER.parse,
            trigger=CronTrigger(hour="*/1"),  # example Every 10 minute
            id="moex_usd_rub_parser",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            MOEX_EUR_PARSER.parse,
            trigger=CronTrigger(hour="*/1"),  # example Every 10 minute
            id="moex_eur_rub_parser",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            CB_USD_PARSER.parse,
            trigger=CronTrigger(day="*/1"), 
            id="cb_usd_rub_parser",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            CB_EUR_PARSER.parse,
            trigger=CronTrigger(day="*/1"), 
            id="cb_eur_rub_parser",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        # start
        scheduler.start()

from django.core.management.base import BaseCommand
from mainpage.all_parsers.parsers import Currencies, Resources
from mainpage.all_parsers import parsers
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.conf import settings
from django_apscheduler.util import close_old_connections

MOEX_USD_PARSER = parsers.MoexCurrencyExchangeRateParser(Currencies.usd, Resources.moex)
MOEX_EUR_PARSER = parsers.MoexCurrencyExchangeRateParser(Currencies.eur, Resources.moex)
CB_USD_PARSER = parsers.CbCurrencyExchangeRateParser(Currencies.usd, Resources.cb)
CB_EUR_PARSER = parsers.CbCurrencyExchangeRateParser(Currencies.eur, Resources.cb)
CB_NEWS_PARSER = parsers.NewsParser("https://cbr.ru/rss/eventrss", Resources.cb)
MOEX_NEWS_PARSER = parsers.NewsParser("https://www.moex.com/export/news.aspx?cat=100", Resources.moex)


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
            trigger=CronTrigger(
                minute="*/31",
                hour="8-19",
                day_of_week="1-5"),
            id="moex_usd_rub_parser",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            MOEX_EUR_PARSER.parse,
            trigger=CronTrigger(
                minute="*/31",
                hour="8-19",
                day_of_week="1-5"),
            id="moex_eur_rub_parser",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            CB_USD_PARSER.parse,
            args=['USD'],
            trigger=CronTrigger(
                minute="*/31",
                hour="8-19",
                day_of_week="1-5"
            ),
            id="cb_usd_rub_parser",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            CB_EUR_PARSER.parse,
            args=['EUR'],
            trigger=CronTrigger(
                minute="*/31",
                hour="8-19",
                day_of_week="1-5"
            ),
            id="cb_eur_rub_parser",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            CB_NEWS_PARSER.run,
            trigger=CronTrigger(
                hour="*/1"
            ),
            id="cb_news_parser",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            MOEX_NEWS_PARSER.run,
            trigger=CronTrigger(
                hour="*/1"
            ),
            id="moex_news_parser",
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

from apscheduler.schedulers.background import BackgroundScheduler
from AllParsers import parsers
from AllParsers.parsers import Currency

def start():
   scheduler = BackgroundScheduler()
   parser = parsers()

   scheduler.add_job(parser.MoexCurrencyExchangeRateParser
   (
      Currency.usd),
      "interval",
      minutes = 1,
      id="parser_001",
      replace_existing=True
   )

   scheduler.start()
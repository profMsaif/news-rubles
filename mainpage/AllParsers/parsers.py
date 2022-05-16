from datetime import datetime
import requests
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum

from mainpage.models import EUR

class Currency(Enum):
    usd: str = "USD000000TOD"
    eur: str = "EUR_RUB__TOD"


@dataclass
class Quote:
    price: float
    timestamp: str
    id_resource: int
    id_currency: int


class Parser(ABC):
    resource_id: int = 1
    name: str = "MOEX"
    base_url: str = "https://iss.moex.com"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.2.644 Yowser/2.5 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }

    def _get(self, url):
        with requests.session() as session:
            resp = session.get(url, headers=self.headers)
            resp.encoding = "utf-8"
            if resp.status_code == 200:
                return resp.json()
            print("error", resp.text)

    @abstractmethod
    def parse(self):
        pass


class MoexCurrencyExchangeRateParser(Parser):
    def __init__(self, currency: Currency):
        path = f"iss/engines/currency/markets/selt/boardgroups/13/securities/{currency.value}.json?marketdata.columns=LAST,SECID,UPDATETIME&iss.meta=off"
        self.url = f"{self.base_url}/{path}"
        self.currency = currency
        self.currencyId = 1 if currency == Currency.usd else 2 

    def convert_to_quote(self, resp):
        data = resp['marketdata']['data'][0]
        return Quote(price=data[0], timestamp=f"{datetime.date(datetime.now())} {data[2]}", id_resource=self.resource_id, id_currency = self.id_currency)

    def parse(self):
        resp = self._get(self.url)
        return self.convert_to_quote(resp)

    def save_to_usd_table(self, quote):
       EUR.save(quote)


# for usd parser
# usd_rub_parser = MoexCurrencyExchangeRateParser(Currency.usd)
# usd_rub_quote = usd_rub_parser.parse()
# # convert usd_rub_quote to db usd model and save


# # for eur parser
# eur_rub_parser = MoexCurrencyExchangeRateParser(Currency.eur)
# eur_rub_quote = eur_rub_parser.parse()
# convert eur_rub_quote to db eur model and save

# print(usd_rub_quote)
# print(eur_rub_quote)

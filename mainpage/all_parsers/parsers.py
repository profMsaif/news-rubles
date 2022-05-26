from datetime import datetime
import requests
from dataclasses import dataclass
from abc import ABC, abstractmethod
from xml.dom import minidom
from enum import Enum

from mainpage.models import EUR, USD
from mainpage.models import Currency as db_model_currecny
from mainpage.models import Resource as db_model_resource


class Currency(Enum):
    usd: str = "USD000000TOD"
    eur: str = "EUR_RUB__TOD"

    @property
    def model(self):
        if self.name == "usd":
            return USD
        return EUR

    @property
    def id(self):
        return db_model_currecny.objects.get(name=self.name.upper())


class Resources(Enum):
    moex: str = "MOEX"
    cb: str = "CB"

    @property
    def model(self):
        return db_model_resource

    @property
    def id(self):
        return db_model_resource.objects.get(name=self.value.upper())


@dataclass
class Quote:
    price: float
    timestamp: str
    id_resource: int
    id_currency: int

@dataclass
class News:
    text: str
    timestamp: str
    url: str
    id_resource: int


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
    def __init__(self, currency: Currency, resource: Resources):
        path = f"iss/engines/currency/markets/selt/boardgroups/13/securities/{currency.value}.json?marketdata.columns=LAST,SECID,UPDATETIME&iss.meta=off"
        self.url = f"{self.base_url}/{path}"
        self.currency = currency
        self.resource = resource

    def convert_to_quote(self, resp):
        data = resp['marketdata']['data'][0]
        return Quote(price=data[0],
                     timestamp=f"{datetime.date(datetime.now())} {data[2]}",
                     id_resource=self.resource.id,
                     id_currency=self.currency.id)

    def save_to_table(self, quote):
        model = self.currency.model.objects.create(**quote.__dict__)
        model.save()
        return model

    def parse(self):
        resp = self._get(self.url)
        quote = self.convert_to_quote(resp)
        return self.save_to_table(quote)

    def __repr__(self) -> str:
        return f"MoexParser<{self.currency.name}>"


class CbCurrencyExchangeRateParser():
    def __init__(self, currency: Currency, resource: Resources):
        self.path = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.currency = currency
        self.resource = resource
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.2.644 Yowser/2.5 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }

    def convert_to_quote(self):
        data = requests.get(self.path, self.headers).json()
        return Quote(
            price=data['Valute']['EUR']['Value'],
            timestamp=datetime.now(),
            id_resource=self.resource.id,
            id_currency=self.currency.id)

    def save_to_table(self, quote):
        model = self.currency.model.objects.create(**quote.__dict__)
        model.save()
        return model

    def parse(self):
        quote = self.convert_to_quote()
        return self.save_to_table(quote)

    

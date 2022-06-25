from datetime import datetime
from itertools import islice
import requests
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum
from urllib.request import urlopen
from xml.etree.ElementTree import parse
from django.db.models import Max

from mainpage import models

class Currencies(Enum):
    usd: str = "USD000000TOD"
    eur: str = "EUR_RUB__TOD"

    @property
    def model(self):
        if self.name == "usd":
            return models.USD
        return models.EUR

    @property
    def id(self):
        return models.Currency.objects.get(name=self.name.upper())


class Resources(Enum):
    moex: str = "MOEX"
    cb: str = "CB"

    @property
    def model(self):
        return models.Resource

    @property
    def id(self):
        return models.Resource.objects.get(name=self.value.upper())


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
    def __init__(self, currency: Currencies, resource: Resources):
        path = f"iss/engines/currency/markets/selt/boardgroups/13/securities/{currency.value}.json?marketdata.columns=LAST,SECID,UPDATETIME&iss.meta=off"
        self.url = f"{self.base_url}/{path}"
        self.currency = currency
        self.resource = resource

    def convert_to_quote(self, resp):
        data = resp['marketdata']['data'][0]
        return Quote(price=data[0],
                     timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
    def __init__(self, currency: Currencies, resource: Resources):
        self.path = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.currency = currency
        self.resource = resource
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.2.644 Yowser/2.5 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }

    def convert_to_quote(self, valute):
        data = requests.get(self.path, self.headers).json()
        return Quote(
            price=data['Valute'][valute]['Value'],
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            id_resource=self.resource.id,
            id_currency=self.currency.id)

    def save_to_table(self, quote):
        model = self.currency.model.objects.create(**quote.__dict__)
        model.save()
        return model

    def parse(self, *args):
        quote = self.convert_to_quote(args[0])
        return self.save_to_table(quote)

class NewsParser():
    def __init__(self, url, resource: Resources):
        self.url = url
        self.resource = resource

    def convert_to_models(self):
        news_url = urlopen(self.url)
        xmldoc = parse(news_url)

        last_date = self.get_last_news_update(self.resource.id).get('timestamp__max')

        news_models = []
        for item in xmldoc.iterfind('channel/item'):

            date_time = datetime.strptime(item.findtext('pubDate'), "%a, %d %b %Y %H:%M:%S %z")

            if(last_date is None):
                news_models.append(models.News(
                    text=item.findtext('title'),
                    timestamp=date_time,
                    urls=item.findtext('link'),
                    id_resource=self.resource.id
                ))

            elif (last_date.timestamp() is not None and date_time.timestamp() > last_date.timestamp()):
                news_models.append(models.News(
                    text=item.findtext('title'),
                    timestamp=date_time,
                    urls=item.findtext('link'),
                    id_resource=self.resource.id
                ))

        return news_models
    
    def get_last_news_update(self, id_resource):

        filtered_models = models.News.objects.filter(id_resource = id_resource)
        return filtered_models.aggregate(Max('timestamp'))

    def save_to_table(self, objects, batch_size):
        while True:
            batch = list(islice(objects, batch_size))
            if not batch:
                break
            models.News.objects.bulk_create(batch, batch_size)
    
    def run(self, batch_size=400):
        news_models = self.convert_to_models()
        self.save_to_table(news_models, batch_size)
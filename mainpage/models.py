from django.db import models


class USD(models.Model):
    price = models.FloatField(verbose_name='Стоимость')
    id_currency = models.ForeignKey(
        "Currency", verbose_name='Идентификатор валюты', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(verbose_name='Время')
    id_resource = models.ForeignKey(
        "Resource", verbose_name='Идентификатор источника', on_delete=models.CASCADE)

    def str(self):
        return self.price


class EUR(models.Model):
    price = models.FloatField(verbose_name='Стоимость')
    id_currency = models.ForeignKey(
        "Currency", verbose_name='Идентификатор валюты', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(verbose_name='Время')
    id_resource = models.ForeignKey(
        "Resource", verbose_name='Идентификатор источника', on_delete=models.CASCADE)

    def str(self):
        return self.price


class Currency(models.Model):
    name = models.CharField(
        verbose_name='Сокращённое наименование', max_length=30)
    full_name = models.CharField(
        verbose_name='Полное наименование', max_length=50)

    def str(self):
        return self.name


class News(models.Model):
    id_resource = models.ForeignKey(
        "Resource", verbose_name='Идентификатор источника', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст статьи')
    timestamp = models.DateTimeField(verbose_name='Время')
    urls = models.TextField(verbose_name='Текст ссылки')

    def str(self):
        return self.text


class Resource(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=30)

    def str(self):
        return self.name


class Forecast(models.Model):
    id_currency = models.ForeignKey(
        "Currency", verbose_name='Идентификатор валюты', on_delete=models.CASCADE)
    forecast = models.FloatField(verbose_name='Прогнозируемый курс')
    timestamp = models.DateField(verbose_name='День прогноза')

    def str(self):
        return self.forecast

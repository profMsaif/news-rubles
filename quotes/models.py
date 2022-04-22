from django.db import models


# Create your models here.

class USD(models.Model):
    price = models.FloatField('Стоимость')
    id_currency = models.ForeignKey("Currency", on_delete=models.CASCADE)
    timestamp = models.DateField('Время')
    id_resource = models.ForeignKey("Resource", on_delete=models.CASCADE)

    def __str__(self):
        return self.price


class EUR(models.Model):
    price = models.FloatField('Стоимость')
    id_currency = models.ForeignKey("Currency", on_delete=models.CASCADE)
    timestamp = models.DateField('Время')
    id_resource = models.ForeignKey("Resource", on_delete=models.CASCADE)

    def __str__(self):
        return self.price


class Currency(models.Model):
    name = models.CharField('Сокращённое наименование', max_length=30)
    full_name = models.CharField('Полное наименование', max_length=50)

    def __str__(self):
        return self.name


class News(models.Model):
    id_currency = models.ForeignKey("Currency", on_delete=models.CASCADE)
    id_resource = models.ForeignKey("Resource", on_delete=models.CASCADE)
    text = models.TextField('Текст статьи')
    time_stamp = models.DateField()

    def __str__(self):
        return self.text


class Resource(models.Model):
    name = models.CharField('Наименование', max_length=30)

    def __str__(self):
        return self.name


class Forecast(models.Model):
    id_currency = models.ForeignKey("Currency", on_delete=models.CASCADE)
    forecast = models.FloatField('Прогноз')

    def __str__(self):
        return self.forecast

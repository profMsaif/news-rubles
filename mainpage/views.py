from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import USD
from .models import EUR
import json
from json import loads
from decimal import Decimal
from datetime import date, datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
import pytz
import datetime



# offset = datetime.timezone(datetime.timedelta(hours=5))

# print(datetime.datetime.now(offset))

def index(request):
    # ПОЛУЧЕНИЕ ДАННЫХ USD ДЛЯ ГРАФИКА (МОЕХ/ЦБ)
    currencyUSD = USD.objects.all()\
        .values("timestamp", "id_currency", "price", "id_resource")\
        .order_by("timestamp")

    dates_list = list()
    currencyUSD_dict = dict()
    currencyUSD_CB_dict = dict()

    
    for order_by_id in currencyUSD:
        if not order_by_id["timestamp"] in dates_list:
            dates_list.append(order_by_id["timestamp"])
        if order_by_id["id_resource"] == 1:
            if order_by_id["timestamp"] in currencyUSD_dict:
                currencyUSD_dict[order_by_id["timestamp"]] += order_by_id["price"]
            else:
                currencyUSD_dict[order_by_id["timestamp"]] = order_by_id["price"]
        if order_by_id["id_resource"] == 2:
            if order_by_id["timestamp"] in currencyUSD_CB_dict:
                currencyUSD_CB_dict[order_by_id["timestamp"]] += order_by_id["price"]
            else:
                currencyUSD_CB_dict[order_by_id["timestamp"]] = order_by_id["price"]
        print(dates_list)
        
        all_currencyUSD_date = list()
        for date_item in dates_list:
            if date_item in currencyUSD_dict:
                all_currencyUSD_date.append(currencyUSD_dict[date_item])
            else:
                all_currencyUSD_date.append(0)

        
        CB_currencyUSD_date = list()
        for date_item in dates_list:
            if date_item in currencyUSD_CB_dict:
                CB_currencyUSD_date.append(currencyUSD_CB_dict[date_item])
            else:
                CB_currencyUSD_date.append(0)
    
    
    charts_data = dict()
    charts_data["charts_currency"] = dict()
    charts_data["charts_currency"]["dates_list"] = dates_list
    charts_data["charts_currency"]["series"] = [
        {"name": "MOEX", "data": all_currencyUSD_date},
        {"name": "CentralBank", "data": CB_currencyUSD_date}
    ]

    # ПОЛУЧЕНИЕ ДАННЫХ EUR ДЛЯ ГРАФИКА (МОЕХ/ЦБ)
    currencyEUR = EUR.objects.all()\
        .values("timestamp", "id_currency", "price", "id_resource")\
        .order_by("timestamp")

    dates_list_eur = list()
    currencyEUR_dict = dict()
    currencyEUR_CB_dict = dict()


    for order_by_id in currencyEUR:
        if not order_by_id["timestamp"] in dates_list_eur:
            dates_list_eur.append(order_by_id["timestamp"])
        if order_by_id["id_resource"] == 1:
            if order_by_id["timestamp"] in currencyEUR_dict:
                currencyEUR_dict[order_by_id["timestamp"]] += order_by_id["price"]
            else:
                currencyEUR_dict[order_by_id["timestamp"]] = order_by_id["price"]
        if order_by_id["id_resource"] == 2:
            if order_by_id["timestamp"] in currencyEUR_CB_dict:
                currencyEUR_CB_dict[order_by_id["timestamp"]] += order_by_id["price"]
            else:
                currencyEUR_CB_dict[order_by_id["timestamp"]] = order_by_id["price"]

        # print(currencyEUR_dict)
        all_currencyEUR_date = list()
        for date_item in dates_list_eur:
            if date_item in currencyEUR_dict:
                all_currencyEUR_date.append(currencyEUR_dict[date_item])
            else:
                all_currencyEUR_date.append(0)

        
        CB_currencyEUR_date = list()
        for date_item in dates_list_eur:
            if date_item in currencyEUR_CB_dict:
                CB_currencyEUR_date.append(currencyEUR_CB_dict[date_item])
            else:
                CB_currencyEUR_date.append(0)
    
    print(all_currencyEUR_date)
    charts_data_eur = dict()
    charts_data_eur["charts_currency_eur"] = dict()
    charts_data_eur["charts_currency_eur"]["dates_list_eur"] = dates_list_eur
    charts_data_eur["charts_currency_eur"]["series_eur"] = [
        {"name": "MOEX", "data": all_currencyEUR_date},
        {"name": "CentralBank", "data": CB_currencyEUR_date}
    ]

    
    
    def custom_serializer(obj):
        if isinstance(obj, (date)):
            serial = obj.isoformat()
            return serial
        if isinstance(obj, Decimal):
            return float(obj)


    charts_data = json.dumps(charts_data, default=custom_serializer)
    charts_data_eur = json.dumps(charts_data_eur, default=custom_serializer)
    print(charts_data)  
    print(charts_data_eur)


    return render(request, 'mainpage/index.html', locals())


def newspage(request):
    return render(request, 'mainpage/news.html')
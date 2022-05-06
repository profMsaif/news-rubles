from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import USD
import json
from json import loads
from decimal import Decimal
from datetime import date, datetime
from django.core.serializers.json import DjangoJSONEncoder



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
    
    def custom_serializer(obj):
        if isinstance(obj, (datetime, date)):
            serial = obj.isoformat()
            return serial
        if isinstance(obj, Decimal):
            return float(obj)


    charts_data = json.dumps(charts_data, default=custom_serializer)
    print(charts_data)  


    return render(request, 'mainpage/index.html', locals())


def newspage(request):
    return render(request, 'mainpage/news.html')
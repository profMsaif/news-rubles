from django.shortcuts import render
from .models import USD, EUR, News, Forecast
from django.http import HttpResponse
from .models import USD
from .models import EUR
from .models import News
from .models import Forecast
import json
from decimal import Decimal
from datetime import date
from datetime import date, datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
import pytz
import datetime
from tzlocal import get_localzone
import numpy as np

# tz = get_localzone()
# tz
# print(tz)
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

    all_currencyUSD_date = list()
    CB_currencyUSD_date = list()
    all_currencyEUR_date = list()
    CB_currencyEUR_date = list()
    for order_by_id in currencyUSD:
        
        if not order_by_id["timestamp"] in dates_list:
            dates_list.append(order_by_id["timestamp"])

        if order_by_id["id_resource"] == 1:

            if order_by_id["timestamp"] in currencyUSD_dict:
                currencyUSD_dict[order_by_id["timestamp"]] = order_by_id["price"]

            else:
                currencyUSD_dict[order_by_id["timestamp"]] = order_by_id["price"]
                
        if order_by_id["id_resource"] == 2:

            if order_by_id["timestamp"] in currencyUSD_CB_dict:
                currencyUSD_CB_dict[order_by_id["timestamp"]] = order_by_id["price"]

            else:
                currencyUSD_CB_dict[order_by_id["timestamp"]] = order_by_id["price"]
        
        
        
        for date_item in dates_list:
            if date_item in currencyUSD_dict:
                all_currencyUSD_date.append(currencyUSD_dict[date_item])
            # else:
            #     all_currencyUSD_date.append(NULL)

        
       
        for date_item in dates_list:
            if date_item in currencyUSD_CB_dict:
                CB_currencyUSD_date.append(currencyUSD_CB_dict[date_item])
            # else:
            #     CB_currencyUSD_date.append(currencyUSD_dict[date_item])
            # else:
            #     CB_currencyUSD_date.append(NULL)
    

    print(dates_list)
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

        for date_item in dates_list_eur:
            if date_item in currencyEUR_dict:
                all_currencyEUR_date.append(currencyEUR_dict[date_item])
            # else:
            #     all_currencyEUR_date.append(currencyEUR_CB_dict[date_item])

        
        for date_item in dates_list_eur:
            if date_item in currencyEUR_CB_dict:
                CB_currencyEUR_date.append(currencyEUR_CB_dict[date_item])
            # else:
            #     CB_currencyEUR_date.append(currencyEUR_dict[date_item])
    
    
    # print(dates_list_eur)

    charts_data_eur = dict()
    charts_data_eur["charts_currency_eur"] = dict()
    charts_data_eur["charts_currency_eur"]["dates_list_eur"] = dates_list_eur
    charts_data_eur["charts_currency_eur"]["series_eur"] = [
        {"name": "MOEX", "data": all_currencyEUR_date},
        {"name": "CentralBank", "data": CB_currencyEUR_date}
    ]

    

 # ПОЛУЧЕНИЕ ДАННЫХ ВАЛЮТ ДЛЯ ГРАФИКА С ПРЕДСКАЗАНИЕМ (USD/EUR)
    currencyFC = Forecast.objects.all()\
        .values("timestamp", "id_currency", "forecast")\
        .order_by("timestamp")

    dates_list_forecast = list()
    currencyFC_USD_dict = dict()
    currencyFC_EUR_dict = dict()

    
    for order_by_id in currencyFC:
        
        if not order_by_id["timestamp"] in dates_list_forecast:
            dates_list_forecast.append(order_by_id["timestamp"])

        if order_by_id["id_currency"] == 1:

            if order_by_id["timestamp"] in currencyFC_USD_dict:
                currencyFC_USD_dict[order_by_id["timestamp"]] = order_by_id["forecast"]

            else:
                currencyFC_USD_dict[order_by_id["timestamp"]] = order_by_id["forecast"]
                
        if order_by_id["id_currency"] == 2:

            if order_by_id["timestamp"] in currencyFC_EUR_dict:
                currencyFC_EUR_dict[order_by_id["timestamp"]] = order_by_id["forecast"]

            else:
                currencyFC_EUR_dict[order_by_id["timestamp"]] = order_by_id["forecast"]
        
        
        FC_currencyUSD_date = list()
        for date_item in dates_list_forecast:
            if date_item in currencyFC_USD_dict:
                FC_currencyUSD_date.append(currencyFC_USD_dict[date_item])


        
        FC_currencyEUR_date = list()
        for date_item in dates_list_forecast:
            if date_item in currencyFC_EUR_dict:
                FC_currencyEUR_date.append(currencyFC_EUR_dict[date_item])

    # date_l_seven = np.take(dates_list_forecast, [-7, -6, -5, -4, -3, -2, -1])
    
    # price_USD_l_seven = np.take(FC_currencyUSD_date, [-7, -6, -5, -4, -3, -2, -1])
    
    # price_EUR_l_seven = np.take(FC_currencyEUR_date, [-7, -6, -5, -4, -3, -2, -1])

    predict_USD = FC_currencyUSD_date[-1]
    predict_EUR = FC_currencyEUR_date[-1]


    # charts_data_forecast = dict()
    # charts_data_forecast["charts_currency_forecast"] = dict()
    # charts_data_forecast["charts_currency_forecast"]["dates_list_forecast"] = date_l_seven
    # charts_data_forecast["charts_currency_forecast"]["series_forecast"] = [
    #     {"name": "USD", "data": price_USD_l_seven},
    #     {"name": "EUR", "data": price_EUR_l_seven}
    # ]

    # ПОЛУЧЕНИЕ НОВОСТЕЙ С MOEX 
    newsMoex = News.objects.all()\
        .values("timestamp", "id_resource", "text", "urls")\
        .order_by("timestamp")

    dates_list_news_moex = list()
    newsMoex_dict = dict()
    newsCB_dict = dict()

    dates_list_news_moex_urls = list()
    newsMoex_dict_urls = dict()
    newsCB_dict_urls = dict()

    
    for order_by_id in newsMoex:
        if not order_by_id["timestamp"] in dates_list_news_moex:
            dates_list_news_moex.append(order_by_id["timestamp"])
        if order_by_id["id_resource"] == 1:
            if order_by_id["timestamp"] in newsMoex_dict:
                newsMoex_dict[order_by_id["timestamp"]] += order_by_id["text"]
            else:
                newsMoex_dict[order_by_id["timestamp"]] = order_by_id["text"]
        if order_by_id["id_resource"] == 2:
            if order_by_id["timestamp"] in newsCB_dict:
                newsCB_dict[order_by_id["timestamp"]] += order_by_id["text"]
            else:
                newsCB_dict[order_by_id["timestamp"]] = order_by_id["text"]

        
        moex_news_date = list()
        for date_item in dates_list_news_moex:
            if date_item in newsMoex_dict:
                moex_news_date.append(newsMoex_dict[date_item])
            # else:
            #     moex_news_date.append(newsMoex_dict[date_item])


        
        CB_news_date = list()
        for date_item in dates_list_news_moex:
            if date_item in newsCB_dict:
                CB_news_date.append(newsCB_dict[date_item])

    # ПОЛУЧЕНИЕ  С MOEX 

    for order_by_id in newsMoex:
        if not order_by_id["timestamp"] in dates_list_news_moex_urls:
            dates_list_news_moex_urls.append(order_by_id["timestamp"])
        if order_by_id["id_resource"] == 1:
            if order_by_id["timestamp"] in newsMoex_dict_urls:
                newsMoex_dict_urls[order_by_id["timestamp"]] += order_by_id["urls"]
            else:
                newsMoex_dict_urls[order_by_id["timestamp"]] = order_by_id["urls"]
        if order_by_id["id_resource"] == 2:
            if order_by_id["timestamp"] in newsCB_dict_urls:
                newsCB_dict_urls[order_by_id["timestamp"]] += order_by_id["urls"]
            else:
                newsCB_dict_urls[order_by_id["timestamp"]] = order_by_id["urls"]

        moex_news_date_urls = list()
        for date_item in dates_list_news_moex_urls:
            if date_item in newsMoex_dict_urls:
                moex_news_date_urls.append(newsMoex_dict_urls[date_item])
            # else:
            #     moex_news_date.append(newsMoex_dict[date_item])


        
        CB_news_date_urls = list()
        for date_item in dates_list_news_moex:
            if date_item in newsCB_dict:
                CB_news_date_urls.append(newsCB_dict[date_item])


    def custom_serializer(obj):
        if isinstance(obj, (date)):
            serial = obj.ctime()
            return serial
        if isinstance(obj, Decimal):
            return float(obj)


    charts_data = json.dumps(charts_data, default=custom_serializer)
    charts_data_eur = json.dumps(charts_data_eur, default=custom_serializer)
    try:
        currency_math_USD_MOEX = all_currencyUSD_date[-1] - all_currencyUSD_date[-2]
        currency_math_USD_CB = CB_currencyUSD_date[-1] - CB_currencyUSD_date[-2]
        currency_math_EUR_MOEX = all_currencyEUR_date[-1] - all_currencyEUR_date[-2]
        currency_math_EUR_CB = CB_currencyEUR_date[-1] - CB_currencyEUR_date[-2]
    
        news_math_MOEX_1 = moex_news_date[-1]
        news_math_MOEX_2 = moex_news_date[-2]
        news_math_MOEX_3 = moex_news_date[-3]
        news_math_MOEX_4 = moex_news_date[-4]
        news_math_MOEX_5 = moex_news_date[-5]

        news_math_MOEX_1_urls = moex_news_date_urls[-1]
        news_math_MOEX_2_urls = moex_news_date_urls[-2]
        news_math_MOEX_3_urls = moex_news_date_urls[-3]
        news_math_MOEX_4_urls = moex_news_date_urls[-4]
        news_math_MOEX_5_urls = moex_news_date_urls[-5]

        news_math_MOEX_1_time = dates_list_news_moex[-1]
        news_math_MOEX_2_time = dates_list_news_moex[-2]
        news_math_MOEX_3_time = dates_list_news_moex[-3]
        news_math_MOEX_4_time = dates_list_news_moex[-4]
        news_math_MOEX_5_time = dates_list_news_moex[-5]
    except:
        pass
    return render(request, 'mainpage/index.html', locals())


def newspage(request):

    # ПОЛУЧЕНИЕ НОВОСТЕЙ С MOEX 
    newsMoex = News.objects.all()\
        .values("timestamp", "id_resource", "text", "urls")\
        .order_by("timestamp")
        

    dates_list_news_moex = list()
    newsMoex_dict = dict()
    newsCB_dict = dict()

    dates_list_news_moex_urls = list()
    newsMoex_dict_urls = dict()
    newsCB_dict_urls = dict()

    
    for order_by_id in newsMoex:
        if not order_by_id["timestamp"] in dates_list_news_moex:
            dates_list_news_moex.append(order_by_id["timestamp"])
        if order_by_id["id_resource"] == 1:
            if order_by_id["timestamp"] in newsMoex_dict:
                newsMoex_dict[order_by_id["timestamp"]] += order_by_id["text"] 
            else:
                newsMoex_dict[order_by_id["timestamp"]] = order_by_id["text"]
        if order_by_id["id_resource"] == 2:
            if order_by_id["timestamp"] in newsCB_dict:
                newsCB_dict[order_by_id["timestamp"]] += order_by_id["text"]
            else:
                newsCB_dict[order_by_id["timestamp"]] = order_by_id["text"]

        
        moex_news_date = list()
        
        CB_news_date = list()
        for date_item in dates_list_news_moex:
            if date_item in newsCB_dict:
                CB_news_date.append(newsCB_dict[date_item])

    # ПОЛУЧЕНИЕ  С MOEX 

    for order_by_id in newsMoex:
        if not order_by_id["timestamp"] in dates_list_news_moex_urls:
            dates_list_news_moex_urls.append(order_by_id["timestamp"])
        if order_by_id["id_resource"] == 1:
            if order_by_id["timestamp"] in newsMoex_dict_urls:
                newsMoex_dict_urls[order_by_id["timestamp"]] += order_by_id["urls"]
            else:
                newsMoex_dict_urls[order_by_id["timestamp"]] = order_by_id["urls"]
        if order_by_id["id_resource"] == 2:
            if order_by_id["timestamp"] in newsCB_dict_urls:
                newsCB_dict_urls[order_by_id["timestamp"]] += order_by_id["urls"]
            else:
                newsCB_dict_urls[order_by_id["timestamp"]] = order_by_id["urls"]

        moex_news_date_urls = list()
        for date_item in dates_list_news_moex_urls:
            if date_item in newsMoex_dict_urls:
                moex_news_date_urls.append(newsMoex_dict_urls[date_item])
            # else:
            #     moex_news_date.append(newsMoex_dict[date_item])


        
        CB_news_date_urls = list()
        for date_item in dates_list_news_moex:
            if date_item in newsCB_dict:
                CB_news_date_urls.append(newsCB_dict[date_item])

    

    all_news = []
    charts_data_news = dict()
    charts_data_news["charts_data_news"] = dict()
    charts_data_news["charts_data_news"]["dates_list_news"] = newsMoex_dict_urls
    charts_data_news["charts_data_news"]["series_news"] = moex_news_date
    # charts_data_news["charts_data_news"]["series_news"] = [
    #     {"name": "MOEX", "data": moex_news_date},
    #     {"name": "CentralBank", "data": CB_news_date}
    # ]

    news_list = list()
    news_Moex = list()



    for order_by_news in newsMoex:
        if order_by_news["timestamp"] in news_Moex:
            news_Moex = order_by_news["timestamp"], order_by_news["text"], order_by_news["urls"]
        else:
            news_Moex = order_by_news["timestamp"], order_by_news["text"], order_by_news["urls"]

            data = {
                'time':order_by_news["timestamp"],
                'title':order_by_news["text"],
                'urls':order_by_news["urls"]
            }
            all_news.append(data)
             
 
    all_news.reverse()
   

    return render(request, 'mainpage/news.html', locals())
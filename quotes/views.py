from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'quotes/index.html')


def news(request):
    return render(request, 'quotes/news.html')

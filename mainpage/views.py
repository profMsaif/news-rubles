from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'mainpage/index.html')


def newspage(request):
    return render(request, 'mainpage/news.html')
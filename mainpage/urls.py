from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('News', views.newspage, name='newsp')
]

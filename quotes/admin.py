from django.contrib import admin
from .models import USD
from .models import EUR
from .models import News
from .models import Forecast
from .models import Resource
from .models import Currency

admin.site.register(USD)
admin.site.register(EUR)
admin.site.register(News)
admin.site.register(Forecast)
admin.site.register(Resource)
admin.site.register(Currency)

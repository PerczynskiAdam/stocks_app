from django.contrib import admin

from .models import VMarketInfo, VTransactions
# Register your models here.

admin.site.register(VMarketInfo)
admin.site.register(VTransactions)

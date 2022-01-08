from django.contrib import admin
from django.utils import translation

from .models import Transactions, Balance, Positions, StockTrade, Tag
# Register your models here.

admin.site.register(Transactions)
admin.site.register(Balance)
admin.site.register(Positions)
admin.site.register(StockTrade)
admin.site.register(Tag)


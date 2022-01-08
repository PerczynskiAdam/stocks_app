from django.forms import ModelForm
from journal.models import StockTrade

class StockTradeForm(ModelForm):
    class Meta:
        model = StockTrade
        fields = '__all__'

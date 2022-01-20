from django.forms import ModelForm
from journal.models import StockTrade

class StockTradeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ticker'].widget.attrs.update({'class': 'form-control'})
        self.fields['exchange'].widget.attrs.update({'class': 'form-select'})
        self.fields['buy_point'].widget.attrs.update({'class': 'form-control'})
        self.fields['stop_loss'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['tags'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = StockTrade
        # setting order for form fields
        fields = ['ticker', 'exchange', 'buy_point', 'stop_loss', 'description', 'tags', 'image']

from django.urls import reverse
from django.test import TestCase, Client

from journal.forms import StockTradeForm
from journal.models import Tag, StockTrade

class TestForms(TestCase):

    def setUp(self):

        # imitacja witryny
        self.client = Client()

        self.tag = Tag.objects.create(
            name='Bull flag'
        )

        self.data = {
            'ticker': 'FB',
            'exchange': 'NASDAQ',
            'buy_point': 121,
            'stop_loss': 120,
            'description': 'ciamciaramcia',
            'tags': [self.tag]
        }

        self.form = StockTradeForm(self.data)

    def test_stock_trade_form_valid_data(self):

        self.assertTrue(self.form.is_valid()) # OK

        self.form.save()
        self.assertEqual(StockTrade.objects.count(), 1) # OK after self.form.save()
        self.assertTrue(StockTrade.objects.filter(ticker='FB').exists()) # OK after self.form.save()

    def test_stock_trade_form_valid_redirect(self):

        response = self.client.post(reverse('create-trade'), self.data)
        print(response) # print result: .<HttpResponse status_code=200, "text/html; charset=utf-8">

        self.assertTemplateUsed(response, 'journal/create_trade.html') # OK
        self.assertEquals(response.status_code, 200) # OK

        self.assertRedirects(
            response, reverse('index'),
            status_code=200
        ) # Failure:
#         in assertRedirects
#     url = response.url
# AttributeError: 'HttpResponse' object has no attribute 'url'


    

        
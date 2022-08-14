from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, time, datetime
from journal.forms import StockTradeForm

from journal.views import display_trade, update_trade, create_trade, index
from journal.models import Balance, Positions, Transactions, StockTrade, Tag

class TestViews(TestCase):

    def setUp(self):
        # imitacja witryny
        self.client = Client()

        # utworzenie instancji klasy Balance, Positions, Transactions oraz StockTrade,
        # aby móc przetestować widok
        self.balance_29_01_2022 = Balance.objects.create(
            date=date.fromisoformat('2022-01-29'),
            balance=2000
        )

        self.position_FB = Positions.objects.create(
            balance=self.balance_29_01_2022,
            symbol='FB',
            open_date=date.fromisoformat('2022-01-29'),
            open_time=time.fromisoformat('09:15:00'),
            open_price=2200,
            close_price=2300,
            net_profit=100
        )

        self.transaction_FB = Transactions.objects.create(
            symbol='FB',
            open_time=datetime.fromisoformat('2022-01-29 09:15:00'),
            pct_net_profit=float(0.04545)
        )

        self.tag = Tag.objects.create(
            name='Bull flag'
        )

        self.trade_FB = StockTrade.objects.create(
            ticker='FB',
            exchange='NASDAQ',
            buy_point=float(2200),
            stop_loss=float(2150)
        )

        self.trade_FB.tags.add(self.tag)

        self.index_url = reverse('index')
        self.create_trade_url = reverse('create-trade')
        self.update_trade_url = reverse('update-trade', kwargs={'pk': self.trade_FB.id})
        self.display_trade_url = reverse('display-trade', kwargs={'pk': self.trade_FB.id})


    def test_index(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/index.html')

    def test_create_trade(self):
        response = self.client.get(self.create_trade_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/create_trade.html') 

    def test_update_trade(self):
        response = self.client.get(self.update_trade_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/create_trade.html')

    def test_display_trade(self):
        response = self.client.get(self.display_trade_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/trade.html')

    def test_create_trade_uses_stock_trade_form(self):
        response = self.client.get(self.create_trade_url)
        self.assertIsInstance(response.context['form'], StockTradeForm)
from django.test import TestCase
from datetime import date, time

from .models import Positions, Balance

# Create your tests here.
class PositionsTestCase(TestCase):

    def setUp(self):
        Positions.objects.create(
            symbol='FB',
            open_date=date.fromisoformat('2022-01-20'), open_time=time.fromisoformat('16:00:00'),
            open_price=121.6, close_price=134.5, net_profit=12.9
        )
        Positions.objects.create(
            symbol='PEO',
            open_date=date.fromisoformat('2022-01-24'), open_time=time.fromisoformat('09:21:00'),
            open_price=140, close_price=137, net_profit=-3
        )

        Balance.objects.create(
            date=date.fromisoformat('2022-01-20'),
            balance=2500
        )

        Balance.objects.create(
            date=date.fromisoformat('2022-01-24'),
            balance=3200
        )

        fb_trade = Positions.objects.get(symbol='FB')
        fb_balance = Balance.objects.get(date=date.fromisoformat('2022-01-20'))

        fb_trade.balance = fb_balance
        fb_trade.save()

        peo_trade = Positions.objects.get(symbol='PEO')
        peo_balance = Balance.objects.get(date=date.fromisoformat('2022-01-24'))

        peo_trade.balance = peo_balance
        peo_trade.save()
    
    def test_positions_pct_net_profit_pos(self):
        fb = Positions.objects.get(symbol='FB')
        peo = Positions.objects.get(symbol='PEO')
        self.assertEqual(fb.pctNetProfitPos, 10.61)
        self.assertEqual(peo.pctNetProfitPos, -2.14)
    
    def test_positions_pct_pos_size(self):
        fb = Positions.objects.get(symbol='FB')
        peo = Positions.objects.get(symbol='PEO')
        self.assertEqual(fb.pctPosSize, 4.86)
        self.assertEqual(peo.pctPosSize, 4.38)

    def test_positions_pct_net_profit_balance(self):
        fb = Positions.objects.get(symbol='FB')
        peo = Positions.objects.get(symbol='PEO')
        self.assertEqual(fb.pctNetProfitBalance, 0.52)
        self.assertEqual(peo.pctNetProfitBalance, -0.09)

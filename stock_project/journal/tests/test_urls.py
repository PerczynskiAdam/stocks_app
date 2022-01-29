from django.test import TestCase
from django.urls import reverse, resolve

from journal.views import index, create_trade, update_trade, display_trade

class UrlsTestCase(TestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_create_trade_url_resolves(self):
        url = reverse('create-trade')
        self.assertEquals(resolve(url).func, create_trade)
    
    def test_update_trade_url_resolves(self):
        url = reverse('update-trade', kwargs={'pk': 'some-uuid'})
        self.assertEquals(resolve(url).func, update_trade)

    def test_display_trade_url_resolves(self):
        url = reverse('display-trade', kwargs={'pk': 'some-uuid'})
        self.assertEquals(resolve(url).func, display_trade)
from decimal import Decimal

from bs4 import BeautifulSoup
from django.db.transaction import atomic

from djmoney import settings
from .base import BaseExchangeBackend


class NBKRBackend(BaseExchangeBackend):
    name = 'nbkr.kg'
    url = settings.NBKR_URL

    def __init__(self, url=settings.NBKR_URL, access_key=None):
        self.url = url
        self.access_key = access_key  # not used

    def get_rates(self, **params):
        response = self.get_response(**params)
        return dict(self.parse_xml(response))

    def parse_xml(self, response):
        soup = BeautifulSoup(response)
        for currency in soup.currencyrates.find_all('currency'):
            value = Decimal(currency.value.text.replace(',', '.'))
            yield (currency.get('isocode'), value)

    @atomic
    def update_rates(self, base_currency='KGS', **kwargs):
        # force base currency of the NBKR to KGS
        return super(NBKRBackend, self).update_rates('KGS', **kwargs)

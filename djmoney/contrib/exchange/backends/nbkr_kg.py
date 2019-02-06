from __future__ import division

import ssl
from decimal import Decimal

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError('NBKR.kg backend requires to have a beautifulsoup4')
from django.db.transaction import atomic

from djmoney import settings
from .base import BaseExchangeBackend

# noinspection PyProtectedMember
ssl._create_default_https_context = ssl._create_unverified_context


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
        soup = BeautifulSoup(response, 'lxml-xml')
        for currency in soup.currencyrates.find_all('currency'):
            nominal = Decimal(currency.nominal.text.replace(',', '.'))
            value = Decimal(currency.value.text.replace(',', '.'))
            yield (currency.get('isocode'), nominal / value)

    @atomic
    def update_rates(self, base_currency='KGS', **kwargs):
        # force base currency of the NBKR to KGS
        return super(NBKRBackend, self).update_rates('KGS', **kwargs)

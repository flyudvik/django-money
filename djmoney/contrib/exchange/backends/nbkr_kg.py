from bs4 import BeautifulSoup

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
            yield (currency.get('isocode'), currency.value.text)

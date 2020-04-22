
from pyews.utils.exchangeversion import ExchangeVersion
from pyews.utils.exceptions import ExchangeVersionError


class Endpoint(object):

    def __init__(self, exchangeVersion, domain=None):
        self.domain = domain
        self.exchangeVersion = exchangeVersion
        self.endpoint = exchangeVersion

    @property
    def exchangeVersion(self):
        return self._exchangeVersion

    @exchangeVersion.setter
    def exchangeVersion(self, value):
        exchange_ver_list = []
        if isinstance(value, list):
            for ver in value:
                if ExchangeVersion.valid_version(ver):
                    exchange_ver_list.append(ver)
        else:
            exchange_ver_list.append(value)
        self._exchangeVersion = exchange_ver_list

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        self._domain = value

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        endpoint_list = []
        if self.domain:
            endpoint_list.append("https://{}/autodiscover/autodiscover.svc".format(self.domain))
            endpoint_list.append("https://autodiscover.{}/autodiscover/autodiscover.svc".format(self.domain))

        endpoint_list.append('https://outlook.office365.com/autodiscover/autodiscover.svc')
        self._endpoint = endpoint_list
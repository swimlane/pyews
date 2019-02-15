from bs4 import BeautifulSoup
from exchangeversion import ExchangeVersion

class UserConfiguration(object):

    def __init__(self, config):
        if config:
            self.create_config(config)
            self.get_exchange_version()

    def create_config(self, config):
        if config.find('ErrorCode').string == 'NoError':
            for item in config.find_all('UserSetting'):
                setting_name = item.Name.string
                setting_value = item.Value.string
                setattr(self, setting_name, setting_value)

    def get_exchange_version(self):
        self.exchangeVersion = ExchangeVersion(self.CasVersion).exchangeVersion
           



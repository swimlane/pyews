import xmltodict
from exchangeversion import ExchangeVersion

class UserConfiguration(object):

    def __init__(self, config):
        if config:
            self.create_config(config)
            self.get_exchange_version()

    def create_config(self, config):
        #self.user_settings = {}
        for setting in config['s:Envelope']['s:Body']['GetUserSettingsResponseMessage']['Response']['UserResponses']['UserResponse']['UserSettings']['UserSetting']:
            setting_name = setting['Name']
            setting_value = setting['Value']
            setattr(self, setting_name, setting_value)

    def get_exchange_version(self):
        self.exchangeVersion = ExchangeVersion(self.CasVersion).exchangeVersion
           



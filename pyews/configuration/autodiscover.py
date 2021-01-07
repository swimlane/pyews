import logging
import requests
from ..core import Core
from .endpoint import Endpoint
from ..service.getusersettings import GetUserSettings
from ..utils.exchangeversion import ExchangeVersion

__LOGGER__ = logging.getLogger(__name__)


class Autodiscover(Core):
    '''A class used to connect to Exchange Web Services using the Autodiscover service endpoint
    
    The Autodiscover class can be used with both Office 365 and on-premises Exchange 2010 to 2019.
    Currently, it has been thoroughly tested with Office 365 but not so much with the on-premises versions of Exchange.
    
    Example:
    
    There two typical methods of using the Autodiscover class.  These behave slightly differently depending on your needs.
    
    1. If you know the Autodiscover URL for your on-premises or Office 365 Exchange Autodiscover service then you can provide this directly
    
    ```python
    Autodiscover(
        credentialObj, 
        endpoint='https://outlook.office365.com/autodiscover/autodiscover.svc',
        exchangeVersion='Office365'
    )
    ```

    2. If you do not know the Autodiscover URL then you can set create_endpoint_list to True to have the Autodiscover class attempt to generate URL endpoints for you
    
    ```python
    Autodiscover(
        credentialObj,
        create_endpoint_list=True
    )
    ```

    Args:
        credentials (Credentials): An object created using the Credentials class
        endpoint (str, optional): Defaults to None. If you want to specify a different Autodiscover endpoint then provide the url here
        exchangeVersion (str, optional): Defaults to None. An exchange version string
        create_endpoint_list (bool, optional): Defaults to False. If you want the Autodiscover class to generate a list of endpoints to try based on a users email address
    '''
    def __init__(self, userconfiguration):
        super(Autodiscover, self).__init__(userconfiguration)
        if not getattr(self.userconfiguration, 'ews_url'):
            self.ews_url = Endpoint(domain=self.userconfiguration.credentials.domain).get()
        self.exchange_version = self.userconfiguration.exchange_version

    def run(self):
        for version in self.exchange_version:
            for endpoint in self.ews_url:
                try:
                    requests.get(endpoint)
                    self.userconfiguration.ews_url = endpoint
                    self.userconfiguration.exchange_version = version
                    autodiscover = GetUserSettings(self.userconfiguration).run(endpoint, version)
                except:
                    continue
                if autodiscover:
                    return autodiscover

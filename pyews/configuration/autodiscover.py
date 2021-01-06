import requests, logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .endpoint import Endpoint
from ..service.getusersettings import GetUserSettings
from ..utils.exchangeversion import ExchangeVersion
from ..utils.exceptions import IncorrectParameters, ExchangeVersionError, SoapResponseHasError, SoapResponseIsNoneError, SoapConnectionRefused, SoapConnectionError

__LOGGER__ = logging.getLogger(__name__)


class Autodiscover:
    '''A class used to connect to Exchange Web Services using the Autodiscover service endpoint
    
    The Autodiscover class can be used with both Office 365 and on-premises Exchange 2010 to 2019.
    Currently, it has been thoroughly tested with Office 365 but not so much with the on-premises versions of Exchange.
    
    Example:
        There two typical methods of using the Autodiscover class.  These behave slightly differently depending on your needs.
            1. If you know the Autodiscover URL for your on-premises or Office 365 Exchange Autodiscover service then you can provide this directly
            
            .. code-block:: python

               Autodiscover(
                   credentialObj, 
                   endpoint='https://outlook.office365.com/autodiscover/autodiscover.svc',
                   exchangeVersion='Office365'
               )

            2. If you do not know the Autodiscover URL then you can set create_endpoint_list to True to have the Autodiscover class attempt to generate URL endpoints for you
            
            .. code-block:: python

               Autodiscover(
                   credentialObj,
                   create_endpoint_list=True
               )

    Args:
        credentials (Credentials): An object created using the Credentials class
        endpoint (str, optional): Defaults to None. If you want to specify a different Autodiscover endpoint then provide the url here
        exchangeVersion (str, optional): Defaults to None. An exchange version string
        create_endpoint_list (bool, optional): Defaults to False. If you want the Autodiscover class to generate a list of endpoints to try based on a users email address
    
    Raises:
        IncorrectParameters: An error occurred by not passing the correct parameters into this class
        ExchangeVersionError: An error occurred when passing in an exchange version that is not supported
        SoapResponseHasError: An error occurred when parsing the SOAP response

    '''
    def __init__(self, userconfiguration):
        self.userconfiguration = userconfiguration
        if not getattr(userconfiguration, 'ews_url'):
            self.ews_url = Endpoint(domain=self.userconfiguration.credentials.domain).get()
        else:
            self.ews_url = self.userconfiguration.ews_url

    def invoke(self):
        '''Used to invoke an Autodiscover SOAP request
        
        Returns:
            str: Returns response from SOAP request
        '''
        for version in self.userconfiguration.exchange_version:
            for endpoint in self.ews_url:
                __LOGGER__.debug("Determining if Exchange Version of {ver} and {ep} is a valid endpoint".format(ver=version,ep=endpoint))
                try:
                    requests.get(endpoint)
                    self.userconfiguration.ews_url = endpoint
                    self.userconfiguration.exchange_version = version
                    autodiscover_result = GetUserSettings(self.userconfiguration).run()
                    __LOGGER__.debug(autodiscover_result)
                    if autodiscover_result:
                        return autodiscover_result
                except requests.RequestException as e:
                    __LOGGER__.debug(
                        "An Error {err} occurred when checking if Exchange Version {ver} and Autodiscover endpoint of {ep} is accessible.".format(
                            err=e.__class__.__name__,
                            ver=version,
                            ep=endpoint
                        )
                    )
                    continue
        return None

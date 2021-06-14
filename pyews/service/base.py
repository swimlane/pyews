import abc
import requests
from lxml.builder import ElementMaker
from lxml import etree
from bs4 import BeautifulSoup

from ..core import Core, Authentication


class Base(Core):
    """The Base class is used by all endpoints and network
    communications. It defines the base structure of all namespaces.
    It is inherited by the Autodiscover & Operation classes
    """

    SOAP_REQUEST_HEADER = {'content-type': 'text/xml; charset=UTF-8'}
    NAMESPACE_MAP = {
        'soap': "http://schemas.xmlsoap.org/soap/envelope/", 
        'm': "http://schemas.microsoft.com/exchange/services/2006/messages", 
        't': "http://schemas.microsoft.com/exchange/services/2006/types", 
        'a': "http://schemas.microsoft.com/exchange/2010/Autodiscover",
    }
    SOAP_MESSAGE_ELEMENT = ElementMaker(
        namespace=NAMESPACE_MAP['soap'],
        nsmap={
            'soap': NAMESPACE_MAP['soap'], 
            'm': NAMESPACE_MAP['m'], 
            't': NAMESPACE_MAP['t']
        }
    )
    SOAP_NAMESPACE = ElementMaker(namespace=NAMESPACE_MAP['soap'],nsmap={'soap': "http://schemas.xmlsoap.org/soap/envelope/"})
    M_NAMESPACE =  ElementMaker(namespace=NAMESPACE_MAP['m'],nsmap={'m': "http://schemas.microsoft.com/exchange/services/2006/messages"})
    T_NAMESPACE = ElementMaker(namespace=NAMESPACE_MAP['t'], nsmap={'t': "http://schemas.microsoft.com/exchange/services/2006/types"})
    XML_ENVELOPE = SOAP_MESSAGE_ELEMENT = ElementMaker(
        namespace=NAMESPACE_MAP['soap'],
        nsmap={
            'soap': NAMESPACE_MAP['soap'], 
            'm': NAMESPACE_MAP['m'], 
            't': NAMESPACE_MAP['t'],
            'xsi': "http://www.w3.org/2001/XMLSchema-instance",
            'xs': "http://www.w3.org/2001/XMLSchema"
        }
    )
    NULL_ELEMENT = ElementMaker()
    HEADER_ELEMENT = ElementMaker(
        namespace=NAMESPACE_MAP['soap'],
        nsmap={
            'soap': NAMESPACE_MAP['soap'], 
            't': NAMESPACE_MAP['t']
        }
    )
    BODY_ELEMENT = SOAP_MESSAGE_ELEMENT.Body
    EXCHANGE_VERSION_ELEMENT = T_NAMESPACE.RequestServerVersion

    @property
    def raw_xml(self):
        return self.__raw_xml

    @raw_xml.setter
    def raw_xml(self, value):
        self.__raw_xml = value

    @abc.abstractmethod
    def get(self):
        raise NotImplementedError

    def _impersonation_header(self):
        if hasattr(Authentication, 'impersonate_as') and Authentication.impersonate_as:
            return self.T_NAMESPACE.ExchangeImpersonation(
                self.T_NAMESPACE.ConnectingSID(
                    self.T_NAMESPACE.PrimarySmtpAddress(Authentication.impersonate_as)
                )
            )
        return ''

    def __parse_convert_id_error_message(self, error_message):
        result = error_message.split('Please use the ConvertId method to convert the Id from ')[1].split(' format.')[0]
        return result.split(' to ')

    def __process_response(self, response):
        self.__logger.debug('SOAP REQUEST: {}'.format(response))
        self.raw_xml = response
        namespace = self.NAMESPACE_MAP
        namespace_dict = {}
        for key,val in namespace.items():
            namespace_dict[val] = None
        return self.parse_response(response, namespace_dict=namespace_dict)

    def run(self):
        """The Base class run method is used for all SOAP requests for
        every endpoint defined

        Returns:
            BeautifulSoup: Returns a BeautifulSoup object or None.
        """
        for item in Authentication.__dict__.keys():
            if not item.startswith('_'):
                if hasattr(Authentication, item):
                    setattr(self, item, getattr(Authentication, item))

        for version in Authentication.exchange_versions:
            for endpoint in Authentication.ews_url:
                if self.__class__.__base__.__name__ == 'Operation' and 'autodiscover' in endpoint:
                    self.__logger.debug('{} == Operation so skipping endpoint {}'.format(self.__class__.__base__.__name__, endpoint))
                    continue
                elif self.__class__.__base__.__name__ == 'Autodiscover' and 'autodiscover' not in endpoint:
                    self.__logger.debug('{} == Autodiscover so skipping endpoint {}'.format(self.__class__.__base__.__name__, endpoint))
                    continue
                try:
                    self.__logger.info('Sending SOAP request to {}'.format(endpoint))
                    self.__logger.info('Setting Exchange Version header to {}'.format(version))
                    body = self.get(version).decode("utf-8")
                    self.__logger.debug('EWS SOAP Request Body: {}'.format(body))
                    if Authentication.auth_header:
                        header_dict = Authentication.auth_header
                        header_dict.update(self.SOAP_REQUEST_HEADER)
                    else:
                        header_dict = self.SOAP_REQUEST_HEADER
                    self.__logger.debug(f"Headers: {header_dict}")
                    response = requests.post(
                        url=endpoint,
                        data=body,
                        headers=header_dict,
                        auth=Authentication.credentials,
                        verify=True
                    )

                    self.__logger.debug('Response HTTP status code: {}'.format(response.status_code))
                    self.__logger.debug('Response text: {}'.format(response.text))

                    parsed_response = BeautifulSoup(response.content, 'xml')
                    if not parsed_response.contents:
                        self.__logger.warning(
                            'The server responded with empty content to POST-request '
                            'from {current}'.format(current=self.__class__.__name__))

                    response_code = getattr(parsed_response.find('ResponseCode'), 'string', None)
                    error_code = getattr(parsed_response.find('ErrorCode'), 'string', None)
                    message_text = getattr(parsed_response.find('MessageText'), 'string', None)
                    error_message = getattr(parsed_response.find('ErrorMessage'), 'string', None)
                    fault_message = getattr(parsed_response.find('faultcode'), 'string', None)
                    fault_string = getattr(parsed_response.find('faultstring'), 'string', None)

                    if 'NoError' in (response_code, error_code):
                        return self.__process_response(parsed_response)
                    elif error_message:
                        self.__logger.warning(
                            'The server responded with "{response_code}" '
                            'response code to POST-request from {current} with error message "{error_message}"'.format(
                                current=self.__class__.__name__,
                                error_message=error_message,
                                response_code=response_code))
                    elif 'ErrorAccessDenied' in (response_code, error_code):
                        self.__logger.warning(
                            'The server responded with "ErrorAccessDenied" '
                            'response code to POST-request from {current} with error message "{message_text}"'.format(
                                current=self.__class__.__name__,
                                message_text=message_text))
                    elif 'ErrorInvalidIdMalformed' in (response_code, error_code):
                        self.__logger.warning(
                            'The server responded with "ErrorInvalidIdMalformed" '
                            'response code to POST-request from {current} with error message "{message_text}"'.format(
                                current=self.__class__.__name__,
                                message_text=message_text))
                        if 'ConvertId' in message_text:
                            return self.__parse_convert_id_error_message(message_text)
                    elif fault_message or fault_string:
                        self.__logger.warning(
                            'The server responded with a "{fault_message}" '
                            'to POST-request from {current} with error message "{fault_string}"'.format(
                                current=self.__class__.__name__,
                                fault_message=fault_message,
                                fault_string=fault_string))
                    else:
                        self.__logger.warning(
                            'The server responded with unknown "ResponseCode" '
                            'and "ErrorCode" from {current} with error message "{message_text}"'.format(
                                current=self.__class__.__name__,
                                message_text=message_text))
                        continue
                except:
                    pass

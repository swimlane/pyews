#import pyews.service.serviceendpoint
#from .serviceendpoint import ServiceEndpoint
#from pyews import userconfiguration as UC
#from pyews.utils.exceptions import ObjectType, SoapResponseHasError
from bs4 import BeautifulSoup
import requests


class ServiceConfiguration(object):

    def __init__(self, username, password):
        '''Child class of ServiceEndpoint that is used to resolve names based on the provided UserConfiguration object.  This class is used as an alternative to Autodiscover
        since ResolveNames endpoint is a common endpoint across all versions of Microsoft Exchange & Office 365.
        
        Args:
            userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
        
        Raises:
            ObjectType: An incorrect object type has been used
        '''
        self.SOAP_REQUEST_HEADER = {'content-type': 'text/xml; charset=UTF-8'}

     #   self.userconfiguration = userconfiguration
        self.username = username
        self.password = password

        self._response = ''
        self.invoke()

    @property
    def raw_soap(self):
        '''Returns the raw SOAP response
        
        Returns:
            str: Raw SOAP XML response
        '''
        return self._raw_soap

    @raw_soap.setter
    def raw_soap(self, value):
        '''Sets the raw soap and response from a SOAP request
        
        Args:
            value (str): The response from a SOAP request
        '''
        self.response = value
        self._raw_soap = value

    @property
    def response(self):
        '''ResolveNames SOAP response
        
        Returns:
            str: Returns the ResolveNames response
        '''
        return self._response

    @response.setter
    def response(self, value):
        '''Creates and sets a response object

        Args:
            value (str): The raw response from a SOAP request
        '''
        self._response = value

    def invoke(self):
        '''Used to invoke an ResolveNames SOAP request
        
        Raises:
            SoapResponseHasError: Raises an error when unable to parse a SOAP response
        '''
       # config = self.userconfiguration
        soap_payload = self.soap()
        r = requests.post(
            'https://autodiscover-s.outlook.com/EWS/Exchange.asmx',
            data=soap_payload, 
            headers=self.SOAP_REQUEST_HEADER, 
            auth=(self.username, self.password)
        )
        parsed_response = BeautifulSoup(r.content, 'xml')
        print(parsed_response)
        if parsed_response.find('ResponseCode').string == 'NoError':
            self.raw_soap = parsed_response
        else:
            raise AttributeError('Unable to parse response from ResolveNames')

    def soap(self):

        return '''<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Header>
      <h:ServerVersionInfo xmlns:h="http://schemas.microsoft.com/exchange/services/2006/types" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" MajorBuildNumber="1750" MajorVersion="15" MinorBuildNumber="15" MinorVersion="20" Version="V2018_01_08" />
   </s:Header>
   <s:Body>
      <GetServiceConfigurationResponse xmlns="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ResponseClass="Success">
         <ResponseCode>NoError</ResponseCode>
         <ResponseMessages>
            <ServiceConfigurationResponseMessageType ResponseClass="Success">
               <ResponseCode>NoError</ResponseCode>
               <m:MailTipsConfiguration xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
                  <t:MailTipsEnabled xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">true</t:MailTipsEnabled>
                  <t:MaxRecipientsPerGetMailTipsRequest xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">50</t:MaxRecipientsPerGetMailTipsRequest>
                  <t:MaxMessageSize xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">36700160</t:MaxMessageSize>
                  <t:LargeAudienceThreshold xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">25</t:LargeAudienceThreshold>
                  <t:ShowExternalRecipientCount xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">false</t:ShowExternalRecipientCount>
                  <t:InternalDomains xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
                     <t:Domain IncludeSubdomains="false" Name="swimlaneresearchdev.onmicrosoft.com" />
                  </t:InternalDomains>
                  <t:PolicyTipsEnabled xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">false</t:PolicyTipsEnabled>
                  <t:LargeAudienceCap xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">1000</t:LargeAudienceCap>
               </m:MailTipsConfiguration>
            </ServiceConfigurationResponseMessageType>
         </ResponseMessages>
      </GetServiceConfigurationResponse>
   </s:Body>
</s:Envelope>'''


        return '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <soap:Header>
    <t:RequestServerVersion Version="Exchange2010" />
  </soap:Header>
  <soap:Body>
    <m:GetUserConfiguration>
      <m:UserConfigurationName Name="TestConfig">
        <t:DistinguishedFolderId Id="drafts"/>
      </m:UserConfigurationName>
      <m:UserConfigurationProperties>Dictionary</m:UserConfigurationProperties>
    </m:GetUserConfiguration>
  </soap:Body>
</soap:Envelope>'''

        return '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <soap:Header>
    <t:RequestServerVersion Version="Exchange2016" />
  </soap:Header>
  <soap:Body>
    <m:GetServiceConfiguration>
        <m:ActingAs>
            <t:EmailAddress>someguy@swimlaneresearchdev.onmicrosoft.com</t:EmailAddress>
            <t:RoutingType>SMTP</t:RoutingType>
        </m:ActingAs>
      <m:RequestedConfiguration>
        <m:ConfigurationName>MailTips</m:ConfigurationName>
      </m:RequestedConfiguration>
    </m:GetServiceConfiguration>
  </soap:Body>
</soap:Envelope>'''


print(ServiceConfiguration('first.last@dev.onmicrosoft.com','password!'))
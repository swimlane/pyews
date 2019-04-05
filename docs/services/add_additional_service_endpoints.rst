
###################################################
Adding Additional EWS Service Endpoints
###################################################

As I stated above I will continue to add additional EWS Service Endpoints, but I wanted to share documentation on how to add your own support for additional service endpoints.

All services are child classes of :doc:`serviceendpoint` to add a new EWS endpoint, you will first create a class that is a child class of ServiceEndpoint.

I have provided a template class to expand or add new additional service endpoints:

.. code-block:: python

   from .serviceendpoint import ServiceEndpoint

   class NewEndpointName(ServiceEndpoint):
       
       def __init__(self, userconfiguration):

           # Call the parent class to verify that the userconfiguration object is a correct object and has the necessary properties
           super(NewEndpointName, self).__init__(userconfiguration)

           # if you ned additional parameters for your service endpoint, then add them to the __init__ method and add logic here as needed

           # Create your SOAP XML message body
           self._soap_request = self.soap()

           # Call the ServiceEndpoint invoke() method with your new SOAP XML body
           super(DeleteItem, self).invoke(self._soap_request)

           # Transform the raw SOAP XML response body to a formatted dictionary or list in this classes response property
           self.response = self.raw_soap

       @property
       def response(self):
           return self._response

       @response.setter
       def response(self, value):
           return_list = []
        
           # Add some logic here to create your response list or dictionary

           self._response = return_list      

       def soap(self, item):
           if (self.userconfiguration.impersonation):
               impersonation_header = self.userconfiguration.impersonation.header
           else:
               impersonation_header = ''

           # create a SOAP XML formatted string here to return
        
           return '''<?xml version="1.0" encoding="UTF-8"?>
                     <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                                    xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
                                    xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
                         <soap:Header>
                             <t:RequestServerVersion Version="%s" />
                             %s
                         </soap:Header>
                         <soap:Body >
                         # Add your body elements here
                         </soap:Body>
                     </soap:Envelope>''' % (self.userconfiguration.exchangeVersion, impersonation_header)
        

   
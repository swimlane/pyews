# Autodiscover

Exchange Web Services can be accessed using a direct URL or using Autodiscover.  If your on-premises Exchange infrastructure is fairly large, you will need to ensure you are connecting to the correct server.  Typically you would provide a specific address that you would want to communicate with, but with Exchange they offer an Autodiscover service. 

Autodiscover is exactly what it sounds like, it will auto discover which server you should be communicating with all through a central endpoint/url.

This documentation provides details about the Autodiscover class within the `pyews` package.  If you would like to find out more information about Exchange's Autodiscover service, please refer to Microsoft's documentation.

This class is used in the `UserConfiguration` class when you decide to use Exchange Web Services Autodiscover service endpoints.

```eval_rst
.. automodule:: pyews.Autodiscover
   :members:
   :undoc-members:
```
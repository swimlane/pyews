# Service Classes

The Service sub-package defines the structure and ultimately makes it easier to build SOAP requests for all classes inherited from these modules.

All endpoints inherit from either the Autodiscover or Operation classes. These classes make extensibility much easier and allows users of this package to define new endpoints easily.


```eval_rst
.. toctree::
   :maxdepth: 2

   autodiscover
   base
   operation
   add_additional_service_endpoints
```
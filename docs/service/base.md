# Base

The Base class is used by both the Autodiscover and Operation classes. Each of these classes inherit from this class which defines static values for namespaces and other elements using the ElementMaker factory pattern.

This class defines the SOAP Envelope, namespaces, headers, and body definitions for Autodiscover and Operation classes.

Additionally, the Base class performs all HTTP requests and response validation.

```eval_rst
.. automodule:: pyews.service.base.Base
   :members:
   :undoc-members:
```
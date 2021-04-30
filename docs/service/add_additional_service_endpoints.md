# Adding Additional EWS Service Endpoints

As I stated above I will continue to add additional EWS Service Endpoints, but I wanted to share documentation on how to add your own support for additional service endpoints.

All endpoints inherit from either :doc:`autodiscover` or :doc:`operation` classes.  In order to define a new endpoint you will need to import one of these classes.

```python
from pyews.service import Operation
```

Once you have imported the appropriate class (typically this will be Operation) you will then create a new class and inherit from it.  In this example I will demonstrate how to build a endpoint for the [`GetAppManifests`](https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/getappmanifests-operation) operation:

```python
from pyews.service import Operation

class GetAppManifests(Operation):

    def soap(self):
        pass
```

In order to inherit from `Operation` you must define the class name (which should be the name of the EWS operation) and a single method called `soap`.

The `soap` method will return the `Body` of a SOAP request using the provided elements.

* M_NAMESPACE
* T_NAMESPACE
* A_NAMESPACE
* WSA_NAMESPACE

By far the most common namespaces you will use wil be the `M_NAMESPACE` and `T_NAMESPACE` properties.

If we look at the example SOAP requst on this [page](https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/getappmanifests-operation) you will see this:

```
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:t="https://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:m="https://schemas.microsoft.com/exchange/services/2006/messages">
   <soap:Header>
      <t:RequestServerVersion Version="Exchange2013_SP1" />
      <t:MailboxCulture>en-US</t:MailboxCulture>
      <t:TimeZoneContext>
         <t:TimeZoneDefinition Id="GMT Standard Time"/>
      </t:TimeZoneContext>
   </soap:Header>
   <soap:Body >
      <m:GetAppManifests>
        <m:ApiVersionSupported>1.1</m:ApiVersionSupported>
        <m:SchemaVersionSupported>1.1</m:SchemaVersionSupported>
      </m:GetAppManifests>
   </soap:Body>
</soap:Envelope>
```

We will only worry about this portion of the XML SOAP request.  All other data is managed by the inherited classes:

```
<m:GetAppManifests>
    <m:ApiVersionSupported>1.1</m:ApiVersionSupported>
    <m:SchemaVersionSupported>1.1</m:SchemaVersionSupported>
</m:GetAppManifests>
```

To define this using the provided namespaces will use the provided namespace attributes (e.g. `m:` or `t:`) and build our return object.

This means that our `GetAppManifests` class and `soap` method will look like this:

```python
from pyews.service import Operation

class GetAppManifests(Operation):

    def soap(self):
        return self.M_NAMESPACE.GetAppManifests(
            self.M_NAMESPACE.ApiVersionSupported('1.1'),
            self.M_NAMESPACE.SchemaVersionSupported('1.1')
        )
```

That's it!  Seriously, pretty easy huh?

## Additional details

If you see a SOAP request element on Microsoft's site that looks like this:

```
<t:AlternateId Format="EwsId" Id="AAMkAGZhN2IxYTA0LWNiNzItN=" Mailbox="user1@example.com"/>
```

Then using our namespaces you would write this as:

```python
self.T_NAMESPACE.AlternateId(Format="EwsId", Id="AAMkAGZhN2IxYTA0LWNiNzItN=", Mailbox="user1@example.com")
```

## Running your class

Now that we have our newly defined endpoint we can instantiate it and then just call the `run` method.

```python
from getappmanifests import GetAppManifests

print(GetAppManifests().run())
```

And we're done!  I hope this helps and if you have any feedback or questions please open a pull requst or an issue.
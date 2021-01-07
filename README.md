# Welcome to py-ews's documentation!


```

    .______   ____    ____       ___________    __    ____   _______.
    |   _  \  \   \  /   /      |   ____\   \  /  \  /   /  /       |
    |  |_)  |  \   \/   / ______|  |__   \   \/    \/   /  |   (----`
    |   ___/    \_    _/ |______|   __|   \            /    \   \    
    |  |          |  |          |  |____   \    /\    / .----)   |   
    | _|          |__|          |_______|   \__/  \__/  |_______/    
                                                                 


    A Python package to interact with Exchange Web Services
```


**py-ews** is a cross platform python package to interact with both Exchange 2010 to 2019 on-premises and Exchange Online (Office 365). 

> This package will wrap all Exchange Web Service endpoints, but currently is focused on providing eDiscovery endpoints. 


## Features

**py-ews** has the following notable features in it's current release:

* Autodiscover support
* Delegation support
* Impersonation support
* Retrieve all mailboxes that can be searched based on credentials provided
* Search a list of (or single) mailboxes in your Exchange environment using all supported search attributes
* Delete email items from mailboxes in your Exchange environment
* Retrieve mailbox inbox rules for a specific account
* Find additional hidden inbox rules for a specified account

Currently this package supports the following endpoint's:

* [DeleteItem](docs/services/deleteitem.md)
* [GetInboxRules](docs/services/getinboxrules.md)
* [FindHiddenInboxRules](docs/services/findhiddeninboxrules.md)
* [GetSearchableMailboxes](docs/services/getsearchablemailboxes.md)
* [ResolveNames](docs/services/resolvenames.md)
* [SearchMailboxes](docs/services/searchmailboxes.md)


## Installation

### OS X & Linux:

```python
pip install py-ews
```

### Windows:

```python
pip install py-ews
```

## Usage example

The first step in using **py-ews** is that you need to create a [UserConfiguration](docs/configuration/userconfiguration.md) object.  Think of this as all the connection information for Exchange Web Services.  An example of creating a [UserConfiguration](docs/configuration/userconfiguration.md) using Office 365 Autodiscover is:

```python
from pyews import UserConfiguration

userconfig = UserConfiguration(
      'myaccount@company.com',
      'Password1234'
)
```


If you would like to use an alternative [Autodiscover](docs/configuration/autodiscover.md) endpoint (or any alternative endpoint) then please provide one using the `endpoint` named parameter:

```python
from pyews import UserConfiguration

userconfig = UserConfiguration(
      'myaccount@company.com',
      'Password1234',
      endpoint='https://outlook.office365.com/autodiscover/autodiscover.svc'
)
```

For more information about creating a [UserConfiguration](docs/configuration/userconfiguration.md) object, please see the full documentation.

Now that you have a [UserConfiguration](docs/configuration/userconfiguration.md) object, we can now use any of the available service endpoints.  This example will demonstrate how you can identify which mailboxes you have access to by using the [GetSearchableMailboxes](docs/services/getsearchablemailboxes.md) EWS endpoint.

Once you have identified a list of mailbox reference ids, then you can begin searching all of those mailboxes by using the [SearchMailboxes](docs/services/searchmailboxes.md) EWS endpoint.

The returned results will then be deleted (moved to Deleted Items folder) from Exchange using the [DeleteItem](docs/services/deleteitem.md) EWS endpoint.

```python
from pyews import UserConfiguration
from pyews import GetSearchableMailboxes
from pyews import SearchMailboxes
from pyews import DeleteItem

userconfig = UserConfiguration(
      'myaccount@company.com',
      'Password1234'
)

# get searchable mailboxes based on your accounts permissions
referenceid_list = []
for mailbox in GetSearchableMailboxes(userconfig).run():
      referenceid_list.append(mailbox['reference_id'])

# let's search all the referenceid_list items
messages_found = []
for search in SearchMailboxes(userconfig).run('subject:account', referenceid_list):
      messages_found.append(search['id'])
      # we can print the results first if we want
      print(search['subject'])
      print(search['id'])
      print(search['sender'])
      print(search['to_recipients'])
      print(search['created_time'])
      print(search['received_time'])
      #etc.

# if we wanted to now delete a specific message then we would call the DeleteItem 
# class like this but we can also pass in the entire messages_found list
deleted_message_response = DeleteItem(userconfig).run(messages_found[2])

print(deleted_message_response)
```

The following is an example of the output returned when calling the above code:

```text
YOUR ACCOUNT IS ABOUT TO EXPIRE! UPGRADE NOW!!!
AAMkAGZjOTlkOWExLTM2MDEtNGI3MS0..............
Josh Rickard
Research
2019-02-28T18:28:36Z
2019-02-28T18:28:36Z
Upgrade Your Account!
AAMkADAyNTZhNmMyLWNmZTctNDIyZC0..............
Josh Rickard
Josh Rickard 
2019-01-24T18:41:11Z
2019-01-24T18:41:11Z
New or modified user account information
AAMkAGZjOTlkOWExLTM2MDEtNGI3MS04.............. 
Microsoft Online Services Team
Research
2019-01-24T18:38:06Z
2019-01-24T18:38:06Z
[{'MessageText': 'Succesfull'}]
```


**For more examples and usage, please refer to the individual class documentation**

* [Services](docs/services/root.md)
* [Configuration](docs/configuration/root.md)

## Development setup

I have provided a [Dockerfile](https://github.com/swimlane/pyews/blob/master/Dockerfile) with all the dependencies and it is currently calling [test.py](https://github.com/swimlane/pyews/blob/master/Dockerfilebin\pyews_test.py).  If you want to test new features, I recommend that you use this [Dockerfile](https://github.com/swimlane/pyews/blob/master/Dockerfile).  You can call the following to build a new container, but keep the dependencies unless they have changed in your requirements.txt or any other changes to the [Dockerfile](https://github.com/swimlane/pyews/blob/master/Dockerfile).

```
docker build --force-rm -t pyews .
```

To run the container, use the following:

``` 
docker run pyews
```

I am new to Unit Testing, but I am working on that as time permits.  If you would like to help, I wouldn't be sad about it. :)


## Release History
 
* 1.0.0
    * Initial release of py-ews and it is still considered a work in progress
* 2.0.0
   * Revamped logic and overhauled all endpoints and classes


## Meta

Josh Rickard – [@MSAdministrator](https://twitter.com/MSAdministrator)

Distributed under the MIT license. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://github.com/swimlane/pyews/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

```eval_rst
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   services/root
   configuration/root
   utils/root
```

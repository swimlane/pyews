# py-ews

[![Documentation Status](https://readthedocs.org/projects/py-ews/badge/?version=latest)](https://py-ews.readthedocs.io/en/latest/?badge=latest)


```
.______   ____    ____       ___________    __    ____   _______.
|   _  \  \   \  /   /      |   ____\   \  /  \  /   /  /       |
|  |_)  |  \   \/   / ______|  |__   \   \/    \/   /  |   (----`
|   ___/    \_    _/ |______|   __|   \            /    \   \    
|  |          |  |          |  |____   \    /\    / .----)   |   
| _|          |__|          |_______|   \__/  \__/  |_______/    
```                                                       
A Python package to interact with Exchange Web Services

**py-ews** is a cross platform python package to interact with both Exchange 2010 to 2019 on-premises and Exchange Online (Office 365).  This package will wrap all Exchange Web Service endpoints, but currently is focused on providing eDiscovery endpoints. 



**py-ews** has the following notable features in it's current release:

* Autodiscover support
* Delegation support
* Impersonation support
* Retrieve all mailboxes that can be searched based on credentials provided
* Search a list of (or single) mailboxes in your Exchange environment using all supported search attributes
* Delete email items from mailboxes in your Exchange environment
* Retrieve mailbox inbox rules for a specific account
* Find additional hidden inbox rules for a specified account

Currently this package supports the following ServiceEndpoints:

* Autodiscover
* DeleteItem
* GetInboxRules
* FindItems (Retrieving hidden inbox rules)
* GetSearchableMailboxes
* ResolveNames
* SearchMailboxes


## Installation

OS X & Linux:

```sh
pip install py-ews
```

Windows:

```sh
pip install py-ews
```

## Usage example

The first step in using **py-ews** is that you need to create a `UserConfiguration` object.  Think of this as all the connection information for Exchange Web Services.  An example of creating a `UserConfiguration object` using Office 365 `Autodiscover` is:

```python
from pyews import UserConfiguration

userconfig = UserConfiguration(
      'myaccount@company.com',
      'Password1234'
)
```


If you would like to use an alternative `Autodiscover` endpoint (or any alternative endpoint) then please provide one using the `endpoint` named parameter:

```python
from pyews import UserConfiguration

userconfig = UserConfiguration(
   'myaccount@company.com',
   'Password1234',
   endpoint='https://outlook.office365.com/autodiscover/autodiscover.svc'
)
```

For more information about creating a `UserConfiguration` object, please see the full documentation on our ReadTheDocs page.

Now that you have a `UserConfiguration` object, we can now use a `ServiceEndpoint`.  This example will demonstrate how you can identify which mailboxes you have access to by using the `GetSearchableMailboxes` EWS endpoint.

Once you have identified a list of mailbox reference ids, then you can begin searching all of those mailboxes by using the `SearchMailboxes` EWS endpoint.

The returned results will then be deleted (moved to Deleted Items folder) from Exchange using the `DeleteItem` EWS endpoint.

```python

from pyews import UserConfiguration

userconfig = UserConfiguration(
      'myaccount@company.com',
      'Password1234'
)

# get searchable mailboxes based on your accounts permissions
referenceid_list = []
for mailbox in GetSearchableMailboxes(userconfig).response:
      referenceid_list.append(mailbox['ReferenceId'])

# let's search all the referenceid_list items
messages_found = []
for search in SearchMailboxes('subject:account', userconfig, referenceid_list).response:
      messages_found.append(search['MessageId'])
      # we can print the results first if we want
      print(search['Subject'])
      print(search['MessageId'])
      print(search['Sender'])
      print(search['ToRecipients'])
      print(search['CreatedTime'])
      print(search['ReceivedTime'])
      #etc.

# if we wanted to now delete a specific message then we would call the DeleteItem 
# class like this but we can also pass in the entire messages_found list
deleted_message_response = DeleteItem(messages_found[2], userconfig).response

print(deleted_message_response)
```

The following is an example of the output returned when calling the above code:

```output
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

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

I have provided a [Dockerfile](Dockerfile) with all the dependencies and it is currently calling `bin\pyews_test.py`.  If you want to test new features, I recommend that you use this Dockerfile instead of a virtualenv.  You can call the following to build a new container, but keep the dependencies unless they have changed in your requirements.txt or any other changes to the Dockerfile.

```sh
docker build --force-rm -t pyews .
```

To run the container, use the following:

```sh
docker run pyews
```

## Release History

* 1.1.0
   * Fixed bug with inbox rules
   * Added feature to find hidden inbox rules
* 1.0.1
   * Updating Documentation with new reference links
* 1.0.0
   * Initial release of py-ews to PyPi

## Meta

Josh Rickard – [@MSAdministrator](https://twitter.com/MSAdministrator) – rickardja@live.com

Distributed under the MIT license. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://github.com/swimlane/pyews/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
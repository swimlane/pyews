Welcome to pyews's documentation!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    A Python package to interact with Exchange Web Services


`pyews` is a python package to interact with both Exchange 2010 to 2016 on-premises and Exchange Online (Office 365).  This package will wrap all Exchange Web Service endpoints, but currently is focused on providing eDiscovery endpoints. 

Currently this package supports the following endpoints:

* Autodiscover
* GetSearchableMailboxes
* SearchMailboxes
* DeleteItem
* GetInboxRules
* ResolveNames

^^^^^^^^^^^^^^
Installation
^^^^^^^^^^^^^^

"""""""""""""""""
OS X & Linux:
"""""""""""""""""

.. code-block:: guess

   pip install pyews


"""""""""""""""""
Windows:
"""""""""""""""""

.. code-block:: guess

   pip install pyews


"""""""""""""""""
Usage example
"""""""""""""""""

The first step in using pyews is that you need to create a userconfiguration object.  Think of this as all the connection information for Exchange Web Services.  An example of creating a userconfiguration using Office 365 Autodiscover is:

.. code-block:: python
   :linenos:

   from pyews import UserConfiguration

   userconfig = UserConfiguration(
       'myaccount@company.com',
       'Password1234'
   )


If you would like to use an alternative autodiscover endpoint (or any alternative endpoint) then please provide one using the `endpoint` named paramter:

.. code-block:: python
   :linenos:

   from pyews import UserConfiguration

   userconfig = UserConfiguration(
       'myaccount@company.com',
       'Password1234',
       endpoint='https://outlook.office365.com/autodiscover/autodiscover.svc'
   )


For more information about creating a `UserConfiguration` object, please see the full documentation here:

Now that you have a `UserConfiguration` object, we can now use a Service Endpoint.  This example will demonstrate how you can identify which mailboxes you have access to by using the `GetSearchableMailboxes` EWS endpoint.

Once you havec identified a list of mailbox reference ids, then you can begin searching all of those mailboxes by using the `SearchMailboxes` EWS endpoint.

The returned results will then be deleted (moved to Deleted Items folder) from Exchange using the `DeleteItem` EWS endpoint.

.. code-block:: python
   :linenos:

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


The following is an example of the output returned when calling the above code:

.. code-block:: guess

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


*For more examples and usage, please refer to the [Wiki][wiki].*

""""""""""""""""""
Development setup
""""""""""""""""""

I have provided a [Dockerfile](Dockerfile) with all the dependencies and it is currently calling `bin\pyews_test.py`.  If you want to test new features, I recommend that you use this Dockerfile instead of a virtualenv.  You can call the following to build a new container, but keep the dependencies unless they have changed in your requirements.txt or any other changes to the Dockerfile.

.. code-block:: guess
   :linenos:

   docker build --force-rm -t pyews .


To run the container, use the following:

.. code-block:: python
   :linenos:
   
   docker run pyews


I am new to Unit Testing, but I am working on that as time permits.  If you would like to help, I wouldn't be sad about it. :)

"""""""""""""""""
Release History
"""""""""""""""""

* 0.0.1
    * Initial release of pyews and it is still considered a work in progress

"""""""""""""""""
Meta
"""""""""""""""""

Josh Rickard – [@MSAdministrator](https://twitter.com/MSAdministrator) – rickardja@live.com

Distributed under the MIT license. See ``LICENSE`` for more information.

"""""""""""""""""
Contributing
"""""""""""""""""

1. Fork it (<https://github.com/msadministrator/pyews/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's 
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
-->
[wiki]: https://github.com/yourname/yourproject/wiki


.. toctree::
   :maxdepth: 2

   services
   userconfiguration

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
Welcome to py-ews's documentation!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    .______   ____    ____       ___________    __    ____   _______.
    |   _  \  \   \  /   /      |   ____\   \  /  \  /   /  /       |
    |  |_)  |  \   \/   / ______|  |__   \   \/    \/   /  |   (----`
    |   ___/    \_    _/ |______|   __|   \            /    \   \    
    |  |          |  |          |  |____   \    /\    / .----)   |   
    | _|          |__|          |_______|   \__/  \__/  |_______/    
                                                                 


    A Python package to interact with Exchange Web Services



**py-ews** is a cross platform python package to interact with both Exchange 2010 to 2019 on-premises and Exchange Online (Office 365).  This package will wrap all Exchange Web Service endpoints, but currently is focused on providing eDiscovery endpoints. 

************
Features
************

**py-ews** has the following notable features in it's current release:

* Autodiscover support
* Delegation support
* Impersonation support
* Retrieve all mailboxes that can be searched based on credentials provided
* Search a list of (or single) mailboxes in your Exchange environment using all supported search attributes
* Delete email items from mailboxes in your Exchange environment
* Retrieve mailbox inbox rules for a specific account
* Find additional hidden inbox rules for a specified account

Currently this package supports the following :doc:`services/serviceendpoint`:'s:

* :doc:`services/deleteitem`
* :doc:`services/getinboxrules`
* :doc:`services/findhiddeninboxrules` (Retrieving hidden inbox rules)
* :doc:`services/getsearchablemailboxes`
* :doc:`services/resolvenames`
* :doc:`services/searchmailboxes`

^^^^^^^^^^^^^^
Installation
^^^^^^^^^^^^^^

"""""""""""""""""
OS X & Linux:
"""""""""""""""""

.. code-block:: guess

   pip install py-ews


"""""""""""""""""
Windows:
"""""""""""""""""

.. code-block:: guess

   pip install py-ews


"""""""""""""""""
Usage example
"""""""""""""""""

The first step in using **py-ews** is that you need to create a :doc:`configuration/userconfiguration` object.  Think of this as all the connection information for Exchange Web Services.  An example of creating a :doc:`configuration/userconfiguration` using Office 365 Autodiscover is:

.. code-block:: python
   :linenos:

   from pyews import UserConfiguration

   userconfig = UserConfiguration(
       'myaccount@company.com',
       'Password1234'
   )


If you would like to use an alternative :doc:`configuration/autodiscover` endpoint (or any alternative endpoint) then please provide one using the `endpoint` named parameter:

.. code-block:: python
   :linenos:

   from pyews import UserConfiguration

   userconfig = UserConfiguration(
       'myaccount@company.com',
       'Password1234',
       endpoint='https://outlook.office365.com/autodiscover/autodiscover.svc'
   )


For more information about creating a :doc:`configuration/userconfiguration` object, please see the full documentation.

Now that you have a :doc:`configuration/userconfiguration` object, we can now use a :doc:`services/serviceendpoint`.  This example will demonstrate how you can identify which mailboxes you have access to by using the :doc:`services/getsearchablemailboxes` EWS endpoint.

Once you have identified a list of mailbox reference ids, then you can begin searching all of those mailboxes by using the :doc:`services/searchmailboxes` EWS endpoint.

The returned results will then be deleted (moved to Deleted Items folder) from Exchange using the :doc:`services/deleteitem` EWS endpoint.

.. code-block:: python
   :linenos:

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


**For more examples and usage, please refer to the individual class documentation**

* :doc:`services/root`
* :doc:`configuration/root`

""""""""""""""""""
Development setup
""""""""""""""""""

I have provided a `Dockerfile <https://github.com/swimlane/pyews/blob/master/Dockerfile>`_ with all the dependencies and it is currently calling `bin\pyews_test.py`.  If you want to test new features, I recommend that you use this `Dockerfile <https://github.com/swimlane/pyews/blob/master/Dockerfile>`_.  You can call the following to build a new container, but keep the dependencies unless they have changed in your requirements.txt or any other changes to the `Dockerfile <https://github.com/swimlane/pyews/blob/master/Dockerfile>`_.

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

* 1.0.0
    * Initial release of py-ews and it is still considered a work in progress

"""""""""""""""""
Meta
"""""""""""""""""

Josh Rickard – `@MSAdministrator <https://twitter.com/MSAdministrator>`_

Distributed under the MIT license. See ``LICENSE`` for more information.

"""""""""""""""""
Contributing
"""""""""""""""""

1. Fork it (<https://github.com/swimlane/pyews/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


.. toctree::
   :maxdepth: 2

   services/root
   configuration/root
   utils/root

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
Netorca SDK
===========

The NetOrca SDK is a powerful tool that allows developers to seamlessly
integrate and interact with the NetOrca API, simplifying the management
of various aspects of the NetOrca platform. This documentation provides
comprehensive guidance on using the SDK to access NetOrca’s features and
data.

Overview
--------

The NetOrca SDK offers a set of Python classes and methods that
facilitate communication with the NetOrca API. It provides an
abstraction layer for authentication, making API calls, and handling
responses, enabling developers to focus on building applications and
services that leverage NetOrca’s capabilities.

Prerequisites
-------------

Before using this code, ensure you have the following:

-  NetOrca API Key: You’ll need an API key to authenticate with the
   NetOrca API.
-  URL: The URL for the NetOrca API.
-  Python Environment: Make sure you have Python installed on your
   system.

Installation
------------

First, you need to install the NetOrca SDK if you haven’t already. You
can install it using pip:

.. code:: bash

   pip install netorca-sdk

Sample Code
-----------

Create an Instance of Netorca
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The NetOrca SDK works with either the use of an API key or a username
and password. After creating the Netorca instance, you can utilize the
supported methods as shown in the examples below. Each method supports
various parameters and filters to customize the requests and responses.
You can refer to the `NetOrca API
documentation <https://docs.netorca.io/api_guide/api/>`__ for more
details on the available endpoints and parameters.

.. code:: python

   # Import necessary modules
   import os
   from netorca_sdk.auth import NetorcaAuth
   from netorca_sdk.netorca import Netorca

   # Initialize the authentication object with your API key and API URL
   netorca_auth = NetorcaAuth(api_key=os.environ["api_key"], fqdn=os.environ["url"])

   # Create an instance of the Netorca class with the authentication object
   netorca = Netorca(auth=netorca_auth)

   # Define filters to narrow down the search
   filters = {"service_name": "name_of_the_service"}

   # Retrieve information about services using the defined filters
   services_info = netorca.get_services(filters=filters)

   # Print the result
   print(services_info)

Using NetOrca with username and password
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Import necessary modules
   import os
   from netorca_sdk.auth import NetorcaAuth
   from netorca_sdk.netorca import Netorca

   # Initialize the authentication object with your API key and API URL
   netorca_auth = NetorcaAuth(username="VALID_USERNAME", password="VALID_PASSWORD", fqdn=os.environ["url"])

   # Create an instance of the Netorca class with the authentication object
   netorca = Netorca(auth=netorca_auth)

   # Define filters to narrow down the search
   filters = {"service_name": "name_of_the_service"}

   # Retrieve information about services using the defined filters
   services_info = netorca.get_services(filters=filters)

   # Print the result
   print(services_info)

Get Services
~~~~~~~~~~~~

.. code:: python

   # Retrieve a list of services with optional filters
   filters = {"service_name": "some_name"} 
   result = netorca.get_services(filters)
   print("Services:", result)

Get Service Items
~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve a list of service items with optional filters
   filters = {"service_name": "some_service_name"}  
   result = netorca.get_service_items(filters)
   print("Service Items:", result)

Get Service Item by ID
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve information about a specific service item by its ID
   service_item_id = 789  # Replace with the actual service item ID
   result = netorca.get_service_item(service_item_id)
   print("Service Item Information:", result)

Get Change Instances
~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve a list of change instances with optional filters
   filters = {"service_name": "some_service_name"}  # Replace with desired filters, or set to None to get all change instances
   result = netorca.get_change_instances(filters)
   print("Change Instances:", result)

Get Change Instance by ID
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve information about a specific change instance by its ID
   change_instance_id = 1234  # Replace with the actual change instance ID
   result = netorca.get_change_instance(change_instance_id)
   print("Change Instance:", result)

Get Service Configs
~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve a list of service configs with optional filters
   filters = {"service_name": "some_service_name"}  # Replace with desired filters, or set to None to get all service configs
   result = netorca.get_service_configs(filters)
   print("Service Configs:", result)

Get Service Config by ID
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve information about a specific service config by its ID
   service_config_id = 9012  # Replace with the actual service config ID
   result = netorca.get_service_config(service_config_id)
   print("Service Config Information:", result)

Get Deployed Items
~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve a list of deployed items with optional filters
   filters = {"service_id": 555}  # Replace with desired filters, or set to None to get all deployed items
   result = netorca.get_deployed_items(filters)
   print("Deployed Items:", result)

Get Deployed Item by ID
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve information about a specific deployed item by its ID
   deployed_item_id = 456  # Replace with the actual deployed item ID
   result = netorca.get_deployed_item(deployed_item_id)
   print("Deployed Item Information:", result)

Create Deployed Item
~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Create a new deployed item associated with a change instance
   change_instance_id = 123  # Replace with the actual change instance ID
   description = {
     "data": "some_data"
   }
   result = netorca.create_deployed_item(change_instance_id, description)
   print("Created Deployed Item:", result)

Update Change Instance
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Update information of a specific change instance by its ID
   change_instance_id = 5678  # Replace with the actual change instance ID
   update_data = {"state": "APPROVED"} 
   result = netorca.update_change_instance(change_instance_id, update_data)
   print("Updated Change Instance:", result)

Create Service Config
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Create a new service config with the provided data
   config_data = {
       "config": {
           "config1":"test1", 
           "config2":"test2"
       }, 
       "service":1
   } 
   result = netorca.create_service_config(config_data)
   print("Created Service Config:", result)

Get Service Items Dependant
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve a list of service item dependants with optional filters
   filters = {"service_name": "some_service"}  
   result = netorca.get_service_items_dependant(filters)
   print("Service Items Dependant:", result)

Get Charges
~~~~~~~~~~~

.. code:: python

   # Retrieve a list of charges with optional filters
   filters = {"charge_type": "monthly_cost"} 
   result = netorca.get_charges(filters)
   print("Charges:", result)

Update Charges
~~~~~~~~~~~~~~

.. code:: python

   # Update information of a specific charge by its ID
   data = { "processed": True }
   result = netorca.caller("charges", "patch", id="123", data=data)
   print("Updated Charges:", result)

Replace the placeholder values in each example with the actual data or
IDs you want to use in your interactions with the Netorca API. These
examples demonstrate how to use the various functions provided by the
``Netorca`` class to perform different operations.

Submission Examples
-------------------

NetOrca Support two types of submission, Consumer and ServiceOwner. We
use these on the CI/CD pipeline to submit changes to the NetOrca API.

Consumer submission
~~~~~~~~~~~~~~~~~~~

In this example ConsumerSubmission will look for configuration in the
``config.yaml`` file. The ``config.yaml`` file should be in the same
directory as the script. Example of ``config.yaml`` file:

.. code:: yaml

   ---

   netorca_global:
     base_url: https://api.example-netorca-url.com/v1
     metadata:
       budget_code: 12345
       team_name: name_of_the_team
       team_email: user@mail.com

.. code:: python

   # Import necessary modules
   from netorca_sdk.netorca import ConsumerSubmission

   # Create an instance of ConsumerSubmission with the authentication object and use_config parameter
   consumer = ConsumerSubmission(api_key="API_KEY")
   # Set the NetOrca API URL
   consumer.load_from_repository(REPOSITORY_URL)
   result = consumer.submit()
   # Show the result
   print("Task Submission Result:", result)

Consumer submission with use_config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We should pass config parameter to the load_from_repository as a
dictionary instead of ``config.yaml`` file.

.. code:: python

   # Import necessary modules
   from netorca_sdk.netorca import ConsumerSubmission

   # Create an instance of ConsumerSubmission with the authentication object and use_config parameter
   consumer = ConsumerSubmission(api_key="API_KEY", use_config=True)
   config = {
     "netorca_global": {
       "base_url": "https://api.example-netorca-url.com/v1",
       "metadata": {
         "budget_code": 12345,
         "team_name": "name_of_the_team",
         "team_email": "user@email.com"
       }
     }
   }
   # We can use netorca_validate_only to validate the changes without submitting them
   consumer.load_from_repository(REPOSITORY_URL, netorca_validate_only=True, repository_config=config)
   result = consumer.submit()
   # Show the result
   print("Task Submission Result:", result)

ServiceOwner submission
~~~~~~~~~~~~~~~~~~~~~~~

In this example ServiceOwnerSubmission will look for configuration in
the ``config.yaml`` file. The ``config.yaml`` file should be under
``.netorca`` directory in the same directory of script.

.. code:: python

   # Import necessary modules
   from netorca_sdk.netorca import ServiceOwnerSubmission

   # Create an instance of ConsumerSubmission
   service_owner = ServiceOwnerSubmission(api_key="API_KEY")
   # Set the repository base directory
   REPOSITORY_URL = os.environ.get("REPOSITORY_URL", "./")
   service_owner.load_from_repository(REPOSITORY_URL)
   result = service_owner.submit()
   # Show the result
   print("Task Submission Result:", result)

ServiceOwner submission with extra configs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can also pass extra configuration such as the NetOrca directory or
pass configuration instead of using the ``config.json`` file.

.. code:: python

   # Import necessary modules
   from netorca_sdk.netorca import ServiceOwnerSubmission

   # Create an instance of ConsumerSubmission with the authentication object and use_config parameter
   service_owner = ServiceOwnerSubmission(api_key="API_KEY")
   # Set the repository base directory
   REPOSITORY_URL = os.environ.get("REPOSITORY_URL", "./")
   config = {
     "netorca_global": {
       "base_url": "https://api.example-netorca-url.com/v1"
     }
   }
   service_owner.load_from_repository(REPOSITORY_URL, netorca_directory="netorca", repository_config=config)
   result = service_owner.submit()
   # Show the result
   print("Task Submission Result:", result)

\```python

Usage
-----

1. Replace ``"api_key_here"`` and ``"api_url_here"`` in the code with
   your actual API key and API URL.

2. Run the Python script to execute the code. It will make a request to
   the Netorca API and retrieve information about services that match
   the specified filters.

3. The result will be printed to the console.

Additional Information
----------------------

-  You can customize the ``filters`` dictionary to filter services based
   on your requirements.

-  For more advanced usage, consider setting the ``use_config``
   parameter to ``True`` when creating an instance of
   ``ConsumerSubmission``. When ``use_config`` is set to ``True``, the
   SDK will search for the ``team_name`` in the ``config.yaml`` file. If
   ``use_config`` is set to ``False`` (the default), the SDK will call
   the API with your token to dynamically retrieve the ``team_name``.

-  For more details on available API endpoints and methods, refer to the
   NetOrca API documentation.

-  Ensure you have the necessary environment variables set for the API
   key and URL before running the code.

Updates
-------

This SDK will aim to always be released in line with the latest NetOrca
version but does not provide any guarantees.

License
-------

This code is provided under the `MIT License <LICENSE>`__.

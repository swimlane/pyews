# OAuth2 Connector

`py-ews` now allows the user to authenticate using OAuth2. You can authenticate with OAuth2 using multiple different grant flow types. Below are the list of authentication methods which can be used within the py-ews OAuth2 authentication:

* legacy_app_flow
* auth_code_grant
* client_credentials_grant
* backend_app_flow
* web_application_flow
* implicit_grant_flow

The `OAuth2Connector` class also supports both version 1 and 2 of Microsoft's OAuth2 authentication schema. By default, `py-ews` will attempt to use both versions before failing.

You can set the details around OAuth2 authentication using the `Authentication` class. At a minimum you must provide values for the following properties on the `Authentication` object:

* oauth2_authorization_type (one of the values above)
* client_id
* client_secret
* tenant_id

Additional properties include:

* access_token
* redirect_uri
* oauth2_scope
* username
* password
* resource

## Auth Code Grant (Interactive)

The `auth_code_grant` authorization type is the most common and will suffice for most situations. This method requires the following property values:

* client_id
* client_secret
* tenant_id
* redirect_uri
* oauth2_scope

Once you choose this method you will be prompted to visit a provided URL and then copy the response URL back into the console to generate your required `access_token`.

## Client Credentials Grant (Non-Interactive)

The `client_credentials_grant` authorization type is the second most common and will also suffice for most situations. This method requires the following property values:

* client_id
* client_secret
* tenant_id

Once you choose this method you will NOT be prompted. This method is considered a Dameon or non-interactive authentication.

## Implict Grant Flow (Interactive)

The `implicit_grant_flow` authorization requires the following property values:

* client_id
* tenant_id
* redirect_uri

Once you choose this method you will be prompted to visit a provided URL and then copy the response URL back into the console to generate your required `access_token`.

## Web Application Flow (Non-Interactive)

The `web_application_flow` authorization requires the following property values:

* client_id
* client_secret
* tenant_id
* redirect_uri

## Legacy App Flow (Non-Interactive)

The `legacy_app_flow` authorization requires the following property values:

* client_id
* client_secret
* tenant_id
* redirect_uri
* username
* password
* scope

## Backend App Flow (Non-Interactive)

The `backend_app_flow` authorization requires the following property values:

* client_id
* client_secret
* tenant_id
* scope or resource


```eval_rst
.. autoclass:: pyews.core.oauth2connector.OAuth2Connector
   :members:
   :undoc-members:
```
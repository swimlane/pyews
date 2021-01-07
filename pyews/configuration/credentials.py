import re


class Credentials:
    '''Creates a credential object for communicating with EWS

    Example:

    Here is a basic example of createing a new Credentials object
    
    ```python
        creds = Credentials(
            'first.last@company.com',
            'mypassword123'
        )
    ```

    You can access your credential properties, including a domain property like this:

    ```python
    print(creds.email_address)
    print(creds.password)
    print(creds.domain)
    ```

    Args:
        email_address (str): The email address used in the EWS SOAP request
        password (str): The password used in the EWS SOAP request
    '''

    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password
        self.domain = self.email_address

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        '''Splits the domain from an email address
        
        Returns:
            str: Returns the split domain from an email address
        '''
        local, _, domain = value.partition('@')
        self._domain = domain
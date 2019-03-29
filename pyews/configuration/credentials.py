import re

class Credentials(object):
    
    def __init__(self, email_address, password):
        '''Creates a credential object for communicating with EWS
        
        Args:
            email_address (str): The email address used in the EWS SOAP request
            password (str): The password used in the EWS SOAP request
        '''

        self.email_address = email_address
        self.password = password
        self.domain = self.get_domain_from_email_address()


    def get_domain_from_email_address(self):
        '''Splits the domain from an email address
        
        Returns:
            str: Returns the split domain from an email address
        '''

        local, _, domain = self.email_address.partition('@')
        return domain
   
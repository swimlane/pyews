import re

class Credentials(object):
    
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password
        self.domain = self.get_domain_from_email_address()


    def get_domain_from_email_address(self):
        local, _, domain = self.email_address.partition('@')
        return domain
   
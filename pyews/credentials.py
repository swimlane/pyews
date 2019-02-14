import re

class Credentials(object):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.domain = self.get_domain_from_username()

    def get_domain_from_username(self):
        local, _, domain = self.username.partition('@')
        match_object = re.match(r'(.+)\.', domain)
        return match_object.group(1)
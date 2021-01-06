

class Endpoint:

    def __init__(self, domain=None):
        self.domain = domain

    def get(self):
        endpoint_list = ['https://outlook.office365.com/autodiscover/autodiscover.svc']
        if self.domain:
            endpoint_list.append("https://{}/autodiscover/autodiscover.svc".format(self.domain))
            endpoint_list.append("https://autodiscover.{}/autodiscover/autodiscover.svc".format(self.domain))
        return endpoint_list

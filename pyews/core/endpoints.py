class Endpoints:
    """Endpoints provides and generates endpoints to attempt
    EWS requests against.
    """

    def __init__(self, domain=None):
        self.domain = domain

    def get(self):
        endpoint_list = ['https://outlook.office365.com/autodiscover/autodiscover.svc', 'https://outlook.office365.com/EWS/Exchange.asmx', 'https://autodiscover-s.outlook.com/autodiscover/autodiscover.svc']
        if self.domain:
            endpoint_list.append("https://{}/autodiscover/autodiscover.svc".format(self.domain))
            endpoint_list.append("https://autodiscover.{}/autodiscover/autodiscover.svc".format(self.domain))
        return endpoint_list

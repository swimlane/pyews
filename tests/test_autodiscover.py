from re import A
from bs4 import BeautifulSoup
from pyews import Autodiscover, Authentication


class TestAutodiscover(Autodiscover):

    def soap(self):
        return self.A_NAMESPACE.TestAutodiscoverElement('Some Autodiscover Test Value')


def test_autodiscover_soap_body():
    test_operation = TestAutodiscover()
    assert test_operation.run() == None
    soap_body = test_operation.get('Exchange2016')
    soap = BeautifulSoup(soap_body, 'xml')

    envelope = soap.Envelope
    assert envelope['xmlns:wsa'] == Autodiscover.AUTODISCOVER_MAP['wsa']
    assert envelope['xmlns:xsi'] == Autodiscover.AUTODISCOVER_MAP['xsi']
    assert envelope['xmlns:soap'] == Autodiscover.AUTODISCOVER_MAP['soap']
    assert envelope['xmlns:a'] == Autodiscover.AUTODISCOVER_MAP['a']

    assert soap.Header.RequestedServerVersion.string == 'Exchange2016'
    assert soap.select('a|RequestedServerVersion')[0].string == 'Exchange2016'
    assert soap.Header.Action.string == 'http://schemas.microsoft.com/exchange/2010/Autodiscover/Autodiscover/TestAutodiscover'
    assert soap.select('wsa|Action')[0].string == 'http://schemas.microsoft.com/exchange/2010/Autodiscover/Autodiscover/TestAutodiscover'
    assert soap.Header.To.string == Authentication.credentials[0]
    assert soap.select('wsa|To')[0].string == Authentication.credentials[0]
    assert soap.find_all('TestAutodiscoverElement')[0].string == 'Some Autodiscover Test Value'
    assert soap.select('a|TestAutodiscoverElement')[0].string == 'Some Autodiscover Test Value'

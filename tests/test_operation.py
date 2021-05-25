from bs4 import BeautifulSoup
from pyews import Operation


class TestOperation(Operation):

    def soap(self):
        return Operation.M_NAMESPACE.TestElement('Some Test Value')


def test_operation_soap_body():
    test_operation = TestOperation()
    assert test_operation.run() == None
    soap_body = test_operation.get('Exchange2016')
    soap = BeautifulSoup(soap_body, 'xml')

    envelope = soap.Envelope
    assert envelope['xmlns:m'] == Operation.NAMESPACE_MAP['m']
    assert envelope['xmlns:soap'] == Operation.NAMESPACE_MAP['soap']
    assert envelope['xmlns:t'] == Operation.NAMESPACE_MAP['t']
    assert envelope['xmlns:xs'] == "http://www.w3.org/2001/XMLSchema"
    assert envelope['xmlns:xsi'] == "http://www.w3.org/2001/XMLSchema-instance"

    assert soap.Header.RequestedServerVersion['Version'] == 'Exchange2016'
    assert soap.select('t|RequestedServerVersion')[0]['Version'] == 'Exchange2016'
    assert soap.find_all('TestElement')[0].string == 'Some Test Value'
    assert soap.select('m|TestElement')[0].string == 'Some Test Value'

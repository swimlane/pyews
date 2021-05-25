def test_authentication_init():
    from pyews import Authentication, ExchangeVersion, Endpoints
    Authentication.credentials = ('user@company.com','mypassword')
    assert isinstance(Authentication.credentials, tuple)
    assert isinstance(Authentication.exchange_versions, list)
    assert Authentication.exchange_versions == ExchangeVersion.EXCHANGE_VERSIONS
    assert Authentication.endpoints == Endpoints('company.com').get()
    assert Authentication.domain == 'company.com'
    assert Authentication.impersonate_as == ''

def test_setting_authentication_details_directly():
    from pyews import Authentication
    Authentication.credentials = ('user@company.com','mypassword')
    assert Authentication.credentials == ('user@company.com','mypassword')
    Authentication.exchange_versions = 'Exchange2015'
    assert Authentication.exchange_versions == ['Exchange2015']
    Authentication.endpoints = 'https://outlook.office365.com/EWS/Exchange.asmx'
    assert Authentication.endpoints == ['https://outlook.office365.com/EWS/Exchange.asmx']
    Authentication.endpoints = ['https://outlook.office365.com/EWS/Exchange.asmx','https://outlook.office365.com/autodiscover/autodiscover.svc']
    assert Authentication.endpoints == ['https://outlook.office365.com/EWS/Exchange.asmx', 'https://outlook.office365.com/autodiscover/autodiscover.svc']
    Authentication.domain = 'testcompany.com'
    assert Authentication.domain == 'testcompany.com'
    Authentication.domain = 'first.last@testcompany.com'
    assert Authentication.domain == 'testcompany.com'

def test_instantiation_of_ews_interface(pyews_ews_interface):
    ews = pyews_ews_interface(
        'username@company.com',
        'mypassword1'
    )
    assert ews.multi_threading == False
    from pyews import Authentication
    assert Authentication.credentials == ('username@company.com','mypassword1')
    assert Authentication.domain == 'company.com'
    assert isinstance(Authentication.endpoints, list)
    assert isinstance(Authentication.exchange_versions, list)
    assert Authentication.impersonate_as is ''

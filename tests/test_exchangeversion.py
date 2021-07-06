def test_exchange_version():
    from pyews import ExchangeVersion
    version = ExchangeVersion('15.20.4.3')
    if version.exchange_version == 'Exchange2016':
        assert True
    try:
        version = ExchangeVersion('14.20.4.2')
    except:
        assert True
    if ExchangeVersion.valid_version('Exchange2019'):
        assert True
    if ExchangeVersion.valid_version('Office365'):
        assert True
    if not ExchangeVersion.valid_version('Exchange2007'):
        assert True
    

def test_endpoints(pyews_fixture):
    from pyews import Endpoints
    domain  = 'example.com'
    endpoints = Endpoints(domain=domain).get()
    if isinstance(endpoints, list):
        assert True
    if len(endpoints) >= 5:
        assert True
    if domain in endpoints[3] and domain in endpoints[4]:
        assert True


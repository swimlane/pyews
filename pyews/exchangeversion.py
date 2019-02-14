
class ExchangeVersion(object):
    
    # List of build numbers here: https://technet.microsoft.com/en-gb/library/hh135098(v=exchg.150).aspx
    API_VERSION_MAP = {
        8: {
            0: 'Exchange2007',
            1: 'Exchange2007_SP1',
            2: 'Exchange2007_SP1',
            3: 'Exchange2007_SP1',
        },
        14: {
            0: 'Exchange2010',
            1: 'Exchange2010_SP1',
            2: 'Exchange2010_SP2',
            3: 'Exchange2010_SP2',
        },
        15: {
            0: 'Exchange2013',  # Minor builds starting from 847 are Exchange2013_SP1, see api_version()
            1: 'Exchange2016',
            20: 'Exchange2016',  # This is Office365. See issue #221
        }
    }

    def __init__(self, version):
        self.exchangeVersion = self._get_api_version(version)

    def _get_api_version(self, version):
        ver = version.split('.')
        return self.API_VERSION_MAP[int(ver[0])][int(ver[1])]
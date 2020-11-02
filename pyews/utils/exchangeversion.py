
class ExchangeVersion(object):
    '''Used to validate compatible Exchange Versions across multiple service endpoints
        
        Examples:
            To determine if a version number is a valid ExchangeVersion then would pass in the value when instantiating this object:

            .. code-block:: python
                   
               version = ExchangeVersion('15.20.5').exchangeVersion
               print(version)

               # output
               Exchange2016

            To verify an ExchangeVersion is supported, you can view the supported version by access the EXCHANGE_VERSIONS attribute

            .. code-block:: python
                   
               versions = ExchangeVersion('15.20.5').EXCHANGE_VERSIONS
               print(versions)

               # output
               ['Exchange2019', 'Exchange2016', 'Exchange2013_SP1', 'Exchange2013', 'Exchange2010_SP2', 'Exchange2010_SP1', 'Exchange2010']
                
        Args:
            version (str): An Exchange Version number.  Example: 15.20.5 = Exchange2016
        '''
        
    # Borrowed from exchangelib: https://github.com/ecederstrand/exchangelib/blob/master/exchangelib/version.py#L54
    # List of build numbers here: https://docs.microsoft.com/en-us/Exchange/new-features/build-numbers-and-release-dates?view=exchserver-2019 
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
            2: 'Exchange2019',
            20: 'Exchange2016',  # This is Office365. See issue #221
        }
    }

    EXCHANGE_VERSIONS = ['Exchange2019', 'Exchange2016', 'Exchange2013_SP1', 'Exchange2013', 'Exchange2010_SP2', 'Exchange2010_SP1', 'Exchange2010']

    def __init__(self, version):
        self.exchangeVersion = self._get_api_version(version)

    def _get_api_version(self, version):
        '''Gets a string representation of an Exchange Version number
        
        Args:
            version (str): An Exchange Version number.  Example: 15.20.5
        
        Returns:
            str: A string representation of a Exchange Version number. Example: Exchange2016
        '''

        if version == '15.0.847.32':
            return 'Exchange2013_SP1'
        else:
            ver = version.split('.')
            return self.API_VERSION_MAP[int(ver[0])][int(ver[1])]

    @staticmethod
    def valid_version(version):
        '''Determines if a string version name is in list of accepted Exchange Versions
        
        Args:
            version (str): String used to determine if it is an acceptable Exchange Version
        
        Returns:
            bool: Returns either True or False if the passed in version is an acceptable Exchange Version
        '''

        if version == 'Office365':
            return True
        elif version in ExchangeVersion.EXCHANGE_VERSIONS:
            return True
            
        return False

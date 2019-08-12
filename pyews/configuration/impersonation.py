

class Impersonation(object):
    '''The Impersonation class is used when you want to impersonate a user.  You must access rights to impersonate a specific user within your Exchange environment.
    
    Example:
        Below are examples of the data inputs expected for all parameters.
        
        .. code-block:: python

           Impersonation(principalname='first.last@company.com')
           Impersonation(primarysmtpaddress='first.last@company.com')
           Impersonation(smtpaddress='first.last@company.com')

    Args:
        principalname (str, optional): The PrincipalName of the account you want to impersonate
        sid (str, optional): The SID of the account you want to impersonate
        primarysmtpaddress (str, optional): The PrimarySmtpAddress of the account you want to impersonate
        smtpaddress (bool, optional): The SmtpAddress of the account you want to impersonate
    
    Raises:
        AttributeError: This will raise when you call this class but do not provide at least 1 parameter
    '''

    def __init__(self, principalname=None, sid=None, primarysmtpaddress=None, smtpaddress=None):

        if principalname:
            self.impersonation_type = 'PrincipalName'
            self.impersonation_value = principalname
        elif sid:
            self.impersonation_type = 'SID'
            self.impersonation_value = sid
        elif primarysmtpaddress:
            self.impersonation_type = 'PrimarySmtpAddress'
            self.impersonation_value = primarysmtpaddress
        elif smtpaddress:
            self.impersonation_type = 'SmtpAddress'
            self.impersonation_value = smtpaddress
        else:
            raise AttributeError('By setting impersonation to true you must provide either a PrincipalName, SID, PrimarySmtpAddress, or SmtpAddress')

        self.header = self._create_impersonation_header()

    def _create_impersonation_header(self):
        return '''<soap:Header>
  <t:ExchangeImpersonation>
    <t:ConnectingSID>
      <t:{start_type}>{value}</t:{end_type}>
    </t:ConnectingSID>
  </t:ExchangeImpersonation>
</soap:Header>'''.format(start_type=self.impersonation_type, value=self.impersonation_value, end_type=self.impersonation_type)
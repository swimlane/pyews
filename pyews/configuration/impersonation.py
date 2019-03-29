

class Impersonation(object):

    def __init__(self, principalname=None, sid=None, primarysmtpaddress=None, smtpaddress=None):

        if principalname is not None:
            self.impersonation_type = 'PrincipalName'
            self.impersonation_value = principalname
        elif sid is not None:
            self.impersonation_type = 'SID'
            self.impersonation_value = sid
        elif primarysmtpaddress is not None:
            self.impersonation_type = 'PrimarySmtpAddress'
            self.impersonation_value = primarysmtpaddress
        elif smtpaddress is not None:
            self.impersonation_type = 'SmtpAddress'
            self.impersonation_value = smtpaddress
        else:
            raise AttributeError('By setting impersonation to true you must provide either a PrincipalName, SID, PrimarySmtpAddress, or SmtpAddress')

        self.header = self._create_impersonation_header()

    def _create_impersonation_header(self):
        return '''<soap:Header>
  <t:ExchangeImpersonation>
    <t:ConnectingSID>
      <t:%s>%s</t:%s>
    </t:ConnectingSID>
  </t:ExchangeImpersonation>
</soap:Header>''' % (self.impersonation_type, self.impersonation_value, self.impersonation_type)
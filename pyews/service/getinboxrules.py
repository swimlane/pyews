from ..core import Core


class GetInboxRules(Core):
    '''Retrieves inbox (mailbox) rules for a specified email address.
    
    Examples:
        
    To use any service class you must provide a UserConfiguration object first.
    Like all service classes, you can access formatted properties from the EWS endpoint using the `response` property.
    
    If you want to retrieve the inbox rules for a specific email address you must provide it when creating a GetInboxRules object.
        
    ```python
    from pyews import UserConfiguration
    from pyews import GetInboxRules
    
    userconfig = UserConfiguration(
        'first.last@company.com',
        'mypassword123'
    )

    inboxRules = GetInboxRules(userconfig).run('first.last@company.com')
    ```

    Args:
        smtp_address (str): The email address you want to get inbox rules for
        userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
    '''
    
    def __init__(self, userconfiguration):
        super(GetInboxRules, self).__init__(userconfiguration)

    def __process_rule_properties(self, item):
        if item:
            return_dict = {}
            for prop in item:
                if prop.name != 'Conditions' and prop.name != 'Actions':
                    if prop.name not in return_dict:
                        return_dict[prop.name] = prop.string
            if item.find('Conditions'):
                for condition in item.find('Conditions'):
                    if 'conditions' not in return_dict:
                        return_dict['conditions'] = []
                    return_dict['conditions'].append({
                        condition.name: condition.string
                    })
            if item.find('Actions'):
                for action in item.find('Actions'):
                    if 'actions' not in return_dict:
                        return_dict['actions'] = []
                    return_dict['actions'].append({
                        action.name: action.string
                    })
            return return_dict

    def __parse_response(self, value):
        '''Creates and sets a response object
        
        Args:
            value (str): The raw response from a SOAP request
        '''
        return_list = []
        if value.find('ResponseCode').string == 'NoError':
            for item in value.find('InboxRules'):
                if item.name == 'Rule' and item:
                    return_list.append(self.__process_rule_properties(item))
        if self.hidden_rules:
            from .findhiddeninboxrules import FindHiddenInboxRules
            return_list.append(FindHiddenInboxRules(self.userconfiguration).run())
        return return_list

    def run(self, smtp_address, hidden_rules=False):
        self.hidden_rules = hidden_rules
        self.email_address = smtp_address
        self.raw_xml = self.invoke(self.soap())
        return self.__parse_response(self.raw_xml)

    def soap(self):
        '''Creates the SOAP XML message body

        Args:
            email_address (str): A single email addresses you want to GetInboxRules for

        Returns:
            str: Returns the SOAP XML request body
        '''
        if self.userconfiguration.impersonation:
            impersonation_header = self.userconfiguration.impersonation.header
        else:
            impersonation_header = ''

        return '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
        xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
        xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <t:RequestServerVersion Version="{version}" />
    {header}
  </soap:Header>
  <soap:Body>
    <m:GetInboxRules>
      <m:MailboxSmtpAddress>{email}</m:MailboxSmtpAddress>
    </m:GetInboxRules>
  </soap:Body>
</soap:Envelope>
        '''.format(
            version=self.userconfiguration.exchangeVersion, 
            header=impersonation_header, 
            email=self.email_address
        )

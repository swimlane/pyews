from ..service import Operation
from ..utils.exceptions import UknownValueError
from ..utils.attributes import FOLDER_LIST, MESSAGE_ELEMENTS


class GetServiceConfiguration(Operation):
    """GetServiceConfiguration EWS Operation retrieves
    service configuration details
    """

    RESULTS_KEY = 'ServiceConfigurationResponseMessageType'
    CONFIGURATION_NAMES = [
        'MailTips',
        'UnifiedMessagingConfiguration',
        'ProtectionRules'
    ]

    def __init__(self, configuration_name=None, acting_as=None):
        """Retrieves service configuration details.
        Default will attempt to retrieve them all.

        Args:
            configuration_name (list, optional): The name of one or more configuration items. Defaults to 'MailTips','UnifiedMessagingConfiguration','ProtectionRules'.
            acting_as (str, optional): If provided, will attempt to make call using provided user. Defaults to None.

        Raises:
            UknownValueError: Unknown value was provided
        """
        if configuration_name and configuration_name not in self.CONFIGURATION_NAMES:
            UknownValueError(provided_value=configuration_name, known_values=self.CONFIGURATION_NAMES)
        if configuration_name:
            self.configuration_name = configuration_name if isinstance(configuration_name, list) else [configuration_name]
        else:
            self.configuration_name = self.CONFIGURATION_NAMES
        self.acting_as = acting_as

    def __get_configuration_name(self):
        return_list = []
        for item in self.configuration_name:
            return_list.append(self.M_NAMESPACE.ConfigurationName(item))
        return return_list

    def soap(self):
        if self.acting_as:
            return self.M_NAMESPACE.GetServiceConfiguration(
                self.M_NAMESPACE.ActingAs(
                    self.T_NAMESPACE.EmailAddress(self.acting_as),
                    self.T_NAMESPACE.RoutingType('SMTP')
                ),
                self.M_NAMESPACE.RequestedConfiguration(
                    *self.__get_configuration_name()
                )
            )
        else:
            return self.M_NAMESPACE.GetServiceConfiguration(
                self.M_NAMESPACE.RequestedConfiguration(
                    *self.__get_configuration_name()
                )
            )

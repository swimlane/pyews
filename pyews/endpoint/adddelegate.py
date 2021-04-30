from ..service import Operation
from ..utils.exceptions import UknownValueError
from ..utils.attributes import FOLDER_LIST, MESSAGE_ELEMENTS


class AddDelegate(Operation):
    """AddDelegate EWS Operation adds one or more delegates
    to a principal's mailbox and sets access permissions.
    """

    RESULTS_KEY = 'Items'

    __PERMISSIONS = [
        'None',
        'Reviewer',
        'Author',
        'Editor'
    ]

    def __init__(self, target_mailbox, delegate_to, inbox_permissions=None, calender_permissions=None, contacts_permissions=None):
        """Adds the delegate_to to the provided target_mailbox with specific permission sets.

        Args:
            target_mailbox (str): The mailbox in which permissions are added
            delegate_to (str): The account that the permissions are assocaited with
            inbox_permissions (str, optional): Mailbox permission set value. Defaults to None.
            calender_permissions (str, optional): Calendar permission set value. Defaults to None.
            contacts_permissions (str, optional): Contacts permission set value. Defaults to None.
        """
        self.target_mailbox = target_mailbox
        self.delegate_to = delegate_to
        if inbox_permissions and inbox_permissions not in self.__PERMISSIONS:
            UknownValueError(provided_value=inbox_permissions, known_values=self.__PERMISSIONS)
        self.inbox_permissions = inbox_permissions if isinstance(inbox_permissions, list) else [inbox_permissions]

        if calender_permissions and calender_permissions not in self.__PERMISSIONS:
            UknownValueError(provided_value=calender_permissions, known_values=self.__PERMISSIONS)
        self.calender_permissions = calender_permissions if isinstance(calender_permissions, list) else [calender_permissions]

        if contacts_permissions and contacts_permissions not in self.__PERMISSIONS:
            UknownValueError(provided_value=contacts_permissions, known_values=self.__PERMISSIONS)
        self.contacts_permissions = contacts_permissions if isinstance(contacts_permissions, list) else [contacts_permissions]

    def __get_delegate_users(self):
        return_list = []
        if self.inbox_permissions:
            for item in self.inbox_permissions:
                return_list.append(
                    self.T_NAMESPACE.InboxFolderPermissionLevel(item)
                )
        if self.contacts_permissions:
            for item in self.contacts_permissions:
                return_list.append(
                    self.T_NAMESPACE.ContactsFolderPermissionLevel(item)
                )
        if self.calender_permissions:
            for item in self.calender_permissions:
                return_list.append(
                    self.T_NAMESPACE.CalendarFolderPermissionLevel(item)
                )
        return self.T_NAMESPACE.DelegateUser(
            self.T_NAMESPACE.UserId(
                self.T_NAMESPACE.PrimarySmtpAddress(self.delegate_to)
            ),
            self.T_NAMESPACE.DelegatePermissions(
                *return_list
            ),
            self.T_NAMESPACE.ReceiveCopiesOfMeetingMessages('false'),
            self.T_NAMESPACE.ViewPrivateItems('false')
        )

    def soap(self):
        return self.M_NAMESPACE.AddDelegate(
            self.M_NAMESPACE.Mailbox(
                self.T_NAMESPACE.EmailAddress(self.target_mailbox)
            ),
            self.M_NAMESPACE.DelegateUsers(
                self.__get_delegate_users()
            ),
            self.M_NAMESPACE.ReceiveCopiesOfMeetingMessages('DelegatesAndMe')
        )

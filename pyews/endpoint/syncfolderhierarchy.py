from ..service import Operation


class SyncFolderHierarchy(Operation):
    """SyncFolderHierarchy EWS Operation will retrieve 
    a mailboxes folder hierarchy
    """

    RESULTS_KEY = 'Changes'
    FOLDER_LIST = [
        'msgfolderroot',
        'calendar',
        'contacts',
        'deleteditems',
        'drafts',
        'inbox',
        'journal',
        'notes',
        'outbox',
        'sentitems',
        'tasks',
        'junkemail',
        'searchfolders',
        'voicemail',
        'recoverableitemsdeletions',
        'recoverableitemsversions',
        'recoverableitemspurges',
        'recipientcache',
        'quickcontacts',
        'conversationhistory',
        'todosearch',
        'mycontacts',
        'imcontactlist',
        'peopleconnect',
        'favorites'
    ]

    def __init__(self, well_known_folder_name=None):
        """Retrieve the authenticated users mailbox folder hierarchy.

        Args:
            well_known_folder_name (str, optional): The well known folder name. Defaults to all known folder names.
        """
        self.attachment_id = well_known_folder_name

    def soap(self):
        folder_id_list = []
        for folder in self.FOLDER_LIST:
            folder_id_list.append(self.T_NAMESPACE.DistinguishedFolderId(Id=folder))
        return self.M_NAMESPACE.SyncFolderHierarchy(
            self.M_NAMESPACE.FolderShape(
                self.T_NAMESPACE.BaseShape('AllProperties')
            ),
            self.M_NAMESPACE.SyncFolderId(
                *folder_id_list
            )
        )

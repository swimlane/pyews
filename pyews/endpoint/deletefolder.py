from ..service import Operation


class DeleteFolder(Operation):
    """DeleteFolder EWS Operation attempts to delete a folder.
    Specifically this class is focused on deleting search folders.
    """

    RESULTS_KEY = 'Folders'

    def __init__(self, folder_id):
        """
        """
        self.folder_id = folder_id

    def soap(self):
        return self.M_NAMESPACE.DeleteFolder(
            self.M_NAMESPACE.FolderIds(
                self.T_NAMESPACE.FolderId(
                    Id=self.folder_id
                )
            ),
            DeleteType="MoveToDeletedItems"
        )

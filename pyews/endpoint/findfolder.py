from ..service import Operation
from ..utils.exceptions import UknownValueError
from ..utils.attributes import FOLDER_LIST, TRAVERSAL_LIST


class FindFolder(Operation):
    """FindFolder EWS Operation attempts to find a folder.
    Specifically this class is focused on finding search folders.
    """

    RESULTS_KEY = 'Folders'
    BASE_SHAPES = [
        'IdOnly',
        'Default',
        'AllProperties'
    ]
    BODY_TYPES = [
        'Best',
        'HTML',
        'Text'
    ]
    SEARCH_FILTERS = [
        'Contains',
        'Excludes',
        'Exists',
        'IsEqualTo',
        'IsNotEqualTo',
        'IsGreaterThan',
        'IsGreaterThanOrEqualTo',
        'IsLessThan',
        'IsLessThanOrEqualTo'
    ]

    def __init__(self, folder_id='searchfolders', traversal='Shallow'):
        """
        """
        self.folder_id = folder_id
        if traversal not in TRAVERSAL_LIST:
            raise UknownValueError(provided_value=traversal, known_values=TRAVERSAL_LIST)
        self.traversal = traversal

    def soap(self):
        return self.M_NAMESPACE.FindFolder(
            self.M_NAMESPACE.FolderShape(
                self.T_NAMESPACE.BaseShape('AllProperties'),
                self.T_NAMESPACE.AdditionalProperties(
                    self.T_NAMESPACE.FieldURI(FieldURI='folder:DisplayName')
                )
            ),
            self.M_NAMESPACE.IndexedPageFolderView(
                MaxEntriesReturned="10", Offset="0", BasePoint="Beginning"
            ),
            self.M_NAMESPACE.ParentFolderIds(
                self.T_NAMESPACE.DistinguishedFolderId(Id="searchfolders")
            )
        )

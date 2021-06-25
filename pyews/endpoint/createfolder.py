from ..service import Operation
from lxml import etree
from ..utils.exceptions import UknownValueError
from ..utils.attributes import FOLDER_LIST, FIELD_URI_MAP, TRAVERSAL_LIST
from ..utils.searchfilter import SearchFilter


class CreateFolder(Operation):
    """FindItem EWS Operation retrieves details about an item.
    """

    RESULTS_KEY = 'CreateFolderResponseMessage'
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

    def __init__(self, search_string, search_folder=True, display_name='Search Folder', search_all_folders=True, base_folder='inbox', traversal='Deep'):
        """Creates a Folder. Default behavior is to create a Search Folder (eDiscovery Search Folder)

            search_string:
                Detailed Information:
                Each search filter is made of several elements. These are:
                    Field Name - Retrieve all available Field Names by using SearchFilter.FIELD_NAMES
                    Expression - Retrieve all expressions by using SearchFilter.EXPRESSIONS
                    Value - Values are typically strings which make sens for field names
                A logic operator within the SearchFilter class is one of:
                    and - This will perform a boolean AND search operation between two or more search expressions
                    or - This will perform a logical OR search operation between two or more search expressions
                    not - This will perform a search expression that negates a search expression
                Examples:
                    SearchFilter('Body contains Hello World')
                    SearchFilter('Subject contains phishing and IsRead IsEqualTo true')
                    SearchFilter('Subject contains phishing and IsRead IsEqualTo true or Subject contains microsoft', to_string=True)

        Args:
            search_string (str): A search string which is converted to a Search Filter
            search_folder (bool, optional): Creates a Search Folder. Defaults to True.
            display_name (str, optional): The display name of the search folder. Defaults to 'Search Folder'.
            base_folder (str, optional): The base folder the search folder should look at. Defaults to 'inbox'.
            traversal (str, optional): The traversal type. Options are Deep and Shallow. Defaults to 'Deep'.
        """
        self.search_string = SearchFilter(search_string)
        self.display_name = display_name
        if search_folder:
            self.folder_id = [self.T_NAMESPACE.DistinguishedFolderId(Id='searchfolders')]
        else:
            self.folder_id = self.__get_distinguished_folder_ids()
        #if search_all_folders:
        #    self.base_folder_ids = self.__get_distinguished_folder_ids()
        #else:
        self.base_folder_ids = [self.T_NAMESPACE.DistinguishedFolderId(Id=base_folder)]
        if traversal not in TRAVERSAL_LIST:
            raise UknownValueError(provided_value=traversal, known_values=TRAVERSAL_LIST)
        self.traversal = traversal

    def __get_distinguished_folder_ids(self):
        return_list = []
        for item in FOLDER_LIST:
            return_list.append(self.T_NAMESPACE.DistinguishedFolderId(Id=item))
        return return_list

    def soap(self):
        return self.M_NAMESPACE.CreateFolder(
            self.M_NAMESPACE.ParentFolderId(
                *self.folder_id
            ),
            self.M_NAMESPACE.Folders(
                self.T_NAMESPACE.SearchFolder(
                    self.T_NAMESPACE.DisplayName(self.display_name),
                    self.T_NAMESPACE.SearchParameters(
                        self.search_string,
                        self.T_NAMESPACE.BaseFolderIds(
                            *self.base_folder_ids
                        ),
                        Traversal=self.traversal
                    )
                )
            )
        )

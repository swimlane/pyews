from ..service import Operation
from ..utils.exceptions import UknownValueError
from ..utils.attributes import FOLDER_LIST, TRAVERSAL_LIST


class FindItem(Operation):
    """FindItem EWS Operation retrieves details about an item.
    """

    RESULTS_KEY = 'Message'
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

    def __init__(self, query_string, distinguished_folder_name='inbox', base_shape='AllProperties', include_mime_content=True, body_type='Best', traversal='Shallow', reset_cache=False, return_deleted_items=True, return_highlight_terms=True):
        """Retrieves results from a query string

        Args:
            item_id (str): The item id you want to get information about.
            change_key (str, optional): The change key of the item. Defaults to None.
            base_shape (str, optional): The base shape of the returned item. Defaults to 'AllProperties'.
            include_mime_content (bool, optional): Whether or not to include MIME content. Defaults to True.
            body_type (str, optional): The item body type. Defaults to 'Best'.
        """
        if distinguished_folder_name:
            self.folder_name = [self.T_NAMESPACE.DistinguishedFolderId(Id=distinguished_folder_name)]
        else:
            self.folder_name = self.__get_distinguished_folder_ids()
        self.query_string = query_string
        self.include_mime_content = include_mime_content
        if base_shape not in self.BASE_SHAPES:
            raise UknownValueError(provided_value=base_shape, known_values=self.BASE_SHAPES)
        self.base_shape = base_shape
        if body_type not in self.BODY_TYPES:
            raise UknownValueError(provided_value=body_type, known_values=self.BODY_TYPES)
        self.body_type = body_type
        if traversal not in TRAVERSAL_LIST:
            raise UknownValueError(provided_value=traversal, known_values=TRAVERSAL_LIST)
        self.traversal = traversal

        self.query_properties = {}
        if reset_cache:
            self.query_properties.update({
                'ResetCache': 'true'
            })
        if return_deleted_items:
            self.query_properties.update({
                'ReturnDeletedItems': 'true'
            })
        if return_highlight_terms:
            self.query_properties.update({
                'ReturnHighlightTerms': 'true'
            })

    def __get_distinguished_folder_ids(self):
        return_list = []
        for item in FOLDER_LIST:
            return_list.append(self.T_NAMESPACE.DistinguishedFolderId(Id=item))
        return return_list

    def soap(self):
        return self.M_NAMESPACE.FindItem(
            self.M_NAMESPACE.ItemShape(
                self.M_NAMESPACE.BaseShape(self.base_shape),
                self.M_NAMESPACE.IncludeMimeContent(str(self.include_mime_content).lower()),
                self.M_NAMESPACE.BodyType(self.body_type),
                self.M_NAMESPACE.FilterHtmlContent('false')
            ),
            self.M_NAMESPACE.ParentFolderIds(
                *self.folder_name
            ),
            self.M_NAMESPACE.QueryString(self.query_string, **self.query_properties),
            Traversal=self.traversal
        )

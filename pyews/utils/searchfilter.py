from ..service.base import Base, etree
from ..utils.exceptions import UknownValueError
from ..utils.attributes import FIELD_URI_MAP, SEARCH_FILTERS


class SearchFilter:
    """SearchFilter is used to generate a search filter XML body for
    the FindItem EWS Operation
    """

    FIELD_NAMES = FIELD_URI_MAP
    EXPRESSIONS = list(SEARCH_FILTERS.keys())

    def __init__(self, value, to_string=False):
        """Pass in a string value and in return this class returns a
        XML object

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
            value ([str]): A query string
        """
        self.to_string = to_string
        self.__parent = Base.T_NAMESPACE.Restriction()
        self.__build_return_object(value)
        if to_string:
            self._value = str(etree.tostring(self.__parent).decode("utf-8"))
        else:
            self._value = self.__parent

    def __new__(cls, value, to_string=False):
        instance = super(SearchFilter, cls).__new__(cls)
        if hasattr(cls, '__init__'):
            instance.__init__(value, to_string=to_string)
        return instance._value

    @property
    def search_string(self):
        if self.to_string:
            return str(etree.tostring(self.__parent).decode("utf-8"))
        return self.__parent

    def __build_return_object(self, value):
        if 'and' in value:
            object_list = []
            for item in value.split('and'):
                obj = self.__evaluate(item)
                if obj is not None:
                    object_list.append(obj)
            self.__parent.append(Base.T_NAMESPACE.And(*object_list))
        if 'or' in value:
            object_list = []
            for item in value.split('or'):
                obj = self.__evaluate(item)
                if obj is not None:
                    object_list.append(obj)
            self.__parent.append(Base.T_NAMESPACE.Or(*object_list))
        else:
            self.__parent.append(self.__evaluate(value))
        self.__parent

    def __build_search_filter(self, search_filter, field, field_value):
        if search_filter == 'Contains':
            return Base.T_NAMESPACE.Contains(
                Base.T_NAMESPACE.FieldURI(FieldURI=field),
                Base.T_NAMESPACE.FieldURIOrConstant(
                    Base.T_NAMESPACE.Constant(Value=field_value)
                ),
              #  Base.T_NAMESPACE.Constant(Value=field_value),
                ContainmentMode='Substring',
                ContainmentComparison='IgnoreCase'
            )
        elif search_filter == 'Excludes':
            return Base.T_NAMESPACE.Excludes(
                Base.T_NAMESPACE.ExtendedFieldURI(
                    PropertySetId="aa3df801-4fc7-401f-bbc1-7c93d6498c2e",
                    PropertyName="ItemIndex",
                    PropertyType="Integer"
                ),
                Base.T_NAMESPACE.Bitmask(Value=field_value)
            )
        elif search_filter == 'Exists':
            return Base.T_NAMESPACE.Exists(
                Base.T_NAMESPACE.ExtendedFieldURI(
                    PropertySetId="aa3df801-4fc7-401f-bbc1-7c93d6498c2e",
                    PropertyName="ItemIndex",
                    PropertyType="Integer"
                ),
            )
        elif search_filter == 'IsEqualTo':
            return Base.T_NAMESPACE.IsEqualTo(
                Base.T_NAMESPACE.FieldURI(FieldURI=field),
                Base.T_NAMESPACE.FieldURIOrConstant(
                    Base.T_NAMESPACE.Constant(Value=field_value)
                )
            )
        elif search_filter == 'IsNotEqualTo':
            return Base.T_NAMESPACE.IsNotEqualTo(
                Base.T_NAMESPACE.ExtendedFieldURI(
                    PropertySetId="aa3df801-4fc7-401f-bbc1-7c93d6498c2e",
                    PropertyName="ItemIndex",
                    PropertyType="Integer"
                ),
                Base.T_NAMESPACE.FieldURIOrConstant(
                    Base.T_NAMESPACE.FieldURI(FieldURI=field)
                )
            )

    def __to_title_case(self, value):
        return ''.join([x for x in value.title() if not x.isspace()])

    def __evaluate(self, value):
        search_filter = None
        field = None
        field_value = None
        temp_value = value
        for key,val in SEARCH_FILTERS.items():
            if key in value:
                search_filter = key
                temp_value = value.split(key)
                field = temp_value[0].strip()
                field_value = temp_value[1].strip()
            elif key.lower() in value:
                search_filter = key
                temp_value = value.split(key.lower())
                field = temp_value[0].strip()
                field_value = temp_value[1].strip()
        if field:
            for key,val in FIELD_URI_MAP.items():
                if field in val:
                    field = f"{key}:{field}"
                elif self.__to_title_case(field) in val:
                    field = f"{key}:{self.__to_title_case(field)}"
        if ' or ' in field_value:
            field_value = field_value.split(' or ')[0]
        elif ' and ' in field_value:
            field_value = field_value.split(' and ')[0]
        return self.__build_search_filter(search_filter, field, field_value)

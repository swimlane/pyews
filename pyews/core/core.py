import xmltodict
import json

from ..utils.logger import LoggingBase


class Core(metaclass=LoggingBase):
    """The Core class inherits logging and defines
    required authentication details as well as parsing of results
    """

    def camel_to_snake(self, s):
        if s != 'UserDN':
            return ''.join(['_'+c.lower() if c.isupper() else c for c in s]).lstrip('_')
        else:
            return 'user_dn'

    def __process_keys(self, key):
        return_value = key.replace('t:','')
        if return_value.startswith('@'):
            return_value = return_value.lstrip('@')
        return self.camel_to_snake(return_value)

    def _process_dict(self, obj):
        if isinstance(obj, dict):
            obj = {
                self.__process_keys(key): self._process_dict(value) for key, value in obj.items()
                }
        return obj

    def _get_recursively(self, search_dict, field):
        """
        Takes a dict with nested lists and dicts,
        and searches all dicts for a key of the field
        provided.
        """
        fields_found = []
        if search_dict:
            for key, value in search_dict.items():
                if key == field:
                    fields_found.append(value)
                elif isinstance(value, dict):
                    results = self._get_recursively(value, field)
                    for result in results:
                        fields_found.append(result)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            more_results = self._get_recursively(item, field)
                            for another_result in more_results:
                                fields_found.append(another_result)
        return fields_found

    def parse_response(self, soap_response, namespace_dict=None):
        """parse_response is standardized to parse all soap_responses from
        EWS requests

        Args:
            soap_response (BeautifulSoup): EWS SOAP response returned from the Base class
            namespace_dict (dict, optional): A dictionary of namespaces to process. Defaults to None.

        Returns:
            list: Returns a list of dictionaries containing parsed responses from EWS requests.
        """
        ordered_dict = xmltodict.parse(str(soap_response), process_namespaces=True, namespaces=namespace_dict)
        item_dict = json.loads(json.dumps(ordered_dict))
        if hasattr(self, 'RESULTS_KEY'):
            search_response = self._get_recursively(item_dict, self.RESULTS_KEY)
            if search_response:
                return_list = []
                for item in search_response:
                    if isinstance(item,list):
                        for i in item:
                            return_list.append(self._process_dict(i))
                    else:
                        return_list.append(self._process_dict(item))
                return return_list
        return self._process_dict(item_dict)

from .core import Authentication
from .endpoint import GetSearchableMailboxes, GetUserSettings, ResolveNames, SearchMailboxes, ExecuteSearch, GetInboxRules, GetItem, ConvertId, GetHiddenInboxRules, CreateItem, GetServiceConfiguration, SyncFolderHierarchy, SyncFolderItems, GetAttachment


class EWS:

    def __init__(self, username, password, ews_url=None, exchange_version=None, impersonate_as=None):
        Authentication(username, password, ews_url=ews_url, exchange_version=exchange_version, impersonate_as=impersonate_as)

    def get_service_configuration(self, configuration_name=None, acting_as=None):
        return GetServiceConfiguration(configuration_name=configuration_name, acting_as=acting_as).run()

    def get_searchable_mailboxes(self, search_filter=None, expand_group_memberhip=True):
        return GetSearchableMailboxes(search_filter=search_filter, expand_group_memberhip=expand_group_memberhip).run()

    def get_user_settings(self, user=None):
        return GetUserSettings(user=user).run()

    def resolve_names(self, user=None):
        return ResolveNames(user=user).run()

    def execute_ews_search(self, query, reference_id, search_scope='All'):
        response = SearchMailboxes(query, reference_id=reference_id, search_scope=search_scope).run()
        return_list = []
        for item in response:
            return_dict = item
            get_item_response = self.get_item(return_dict['id'].get('id'))
            if get_item_response:
                for response in get_item_response:
                    if response.get('message').get('attachments').get('file_attachment').get('attachment_id').get('id'):
                        attachment_details_list = []
                        attachment = self.get_attachment(response.get('message').get('attachments').get('file_attachment').get('attachment_id').get('id'))
                        for attach in attachment:
                            attachment_dict = {}
                            for key,val in attach.items():
                                for k,v in val.items():
                                    attachment_dict[k] = v
                            if attachment_dict:
                                attachment_details_list.append(attachment_dict)
                    return_dict.update(response.pop('message'))
                    if attachment_details_list:
                        return_dict.update({'attachment_details': attachment_details_list})
            return_list.append(return_dict)
        return return_list

    def execute_outlook_search(self, query, result_row_count='25', max_results_count='-1'):
        return ExecuteSearch(
                query=query, 
                result_row_count=result_row_count, 
                max_results_count=max_results_count
            ).run()

    def get_inbox_rules(self, user=None):
        return GetInboxRules(user=user).run()

    def get_hidden_inbox_rules(self):
        return GetHiddenInboxRules().run()

    def get_item(self, item_id, change_key=None):
        response = GetItem(item_id, change_key=change_key).run()
        if isinstance(response, list):
            if any(item in response for item in ConvertId.ID_FORMATS):
                convert_id_response = ConvertId(Core.credentials[0], item_id, id_type=response[0], convert_to=response[1]).run()
                get_item_response = GetItem(convert_id_response[0]).run()
                return get_item_response if get_item_response else None
        return GetItem(item_id, change_key=change_key).run()

    def get_attachment(self, attachment_id):
        return GetAttachment(attachment_id=attachment_id).run()

    def sync_folder_hierarchy(self, well_known_folder_name=None):
        return SyncFolderHierarchy(well_known_folder_name=well_known_folder_name).run()

    def sync_folder_items(self, folder_id, change_key=None):
        return SyncFolderItems(folder_id, change_key=change_key).run()

    def create_item(self, subject, sender, to_recipients, body_type='HTML'):
        return CreateItem(**{'Subject': subject, 'BodyType': body_type, 'Sender': sender, 'ToRecipients': to_recipients}).run()

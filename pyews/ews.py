import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from .core import Authentication
from .endpoint import GetSearchableMailboxes, GetUserSettings, ResolveNames, SearchMailboxes, ExecuteSearch, GetInboxRules, GetItem, ConvertId, GetHiddenInboxRules, CreateItem, GetServiceConfiguration, SyncFolderHierarchy, SyncFolderItems, GetAttachment, DeleteItem, GetDomainSettings, FindItem, CreateFolder, FindFolder, DeleteFolder


class EWS:

    def __init__(self, 
        username, password, ews_url=None, exchange_version=None, impersonate_as=None, multi_threading=False, 
        tenant_id=None, client_id=None, client_secret=None, oauth2_authorization_type='auth_code_grant', redirect_uri=None, oauth2_scope=None):
        Authentication.credentials = (username, password)
        Authentication.ews_url = ews_url
        Authentication.exchange_versions = exchange_version
        Authentication.impersonate_as = impersonate_as
        Authentication.tenant_id = tenant_id
        Authentication.client_id = client_id
        Authentication.client_secret = client_secret
        Authentication.oauth2_authorization_type = oauth2_authorization_type
        Authentication.redirect_uri = redirect_uri
        Authentication.oauth2_scope = oauth2_scope
        self.multi_threading = multi_threading

    def chunk(self, items, n):
        n = max(1, n)
        return (items[i:i+n] for i in range(0, len(items), n))

    def get_service_configuration(self, configuration_name=None, acting_as=None):
        return GetServiceConfiguration(configuration_name=configuration_name, acting_as=acting_as).run()

    def get_searchable_mailboxes(self, search_filter=None, expand_group_memberhip=True):
        return GetSearchableMailboxes(search_filter=search_filter, expand_group_memberhip=expand_group_memberhip).run()

    def get_user_settings(self, user=None):
        return GetUserSettings(user=user).run()

    def resolve_names(self, user=None):
        return ResolveNames(user=user).run()

    def __execute_multithreaded_search(self, query, reference_id, scope):
        return SearchMailboxes(query=query, reference_id=reference_id, search_scope=scope).run()

    def __execute_multithreaded_find(
            self, 
            query_string, 
            user_list,
            distinguished_folder_name='inbox', 
            base_shape='AllProperties', 
            include_mime_content=True, 
            body_type='Best', 
            traversal='Shallow', 
            reset_cache=False, 
            return_deleted_items=True, 
            return_highlight_terms=True
        ):
        return_list = []
        for user in user_list:
            if user:
                Authentication.impersonate_as = user
                return_list.extend(FindItem(query_string=query_string, distinguished_folder_name=distinguished_folder_name, base_shape=base_shape, include_mime_content=include_mime_content, body_type=body_type, traversal=traversal, reset_cache=reset_cache, return_deleted_items=return_deleted_items, return_highlight_terms=return_highlight_terms).run())
        return return_list

    def execute_ews_search(self, query, reference_id, search_scope='All', thread_count=os.cpu_count()*5):
        response = []
        return_list = []
        if self.multi_threading:
            threads = []
            chunks = self.chunk(reference_id, int(len(reference_id) / thread_count))
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                for chunk in chunks:
                    threads.append(executor.submit(self.__execute_multithreaded_search, query, chunk, search_scope))
                for task in as_completed(threads):
                    result = task.result()
                    if isinstance(result, list):
                        for item in result:
                            response.append(item)
        else:
            response = SearchMailboxes(query, reference_id=reference_id, search_scope=search_scope).run()
        for item in response:
            if item:
                return_dict = item
                get_item_response = self.get_item(return_dict['id'].get('id'))
                if get_item_response:
                    for item_response in get_item_response:
                        if item_response and item_response.get('message').get('attachments') and item_response.get('message').get('attachments').get('file_attachment').get('attachment_id').get('id'):
                            attachment_details_list = []
                            attachment = self.get_attachment(item_response.get('message').get('attachments').get('file_attachment').get('attachment_id').get('id'))
                            for attach in attachment:
                                attachment_dict = {}
                                if attach:
                                    for key,val in attach.items():
                                        for k,v in val.items():
                                            attachment_dict[k] = v
                                if attachment_dict:
                                    attachment_details_list.append(attachment_dict)
                            if attachment_details_list:
                                return_dict.update({'attachment_details': attachment_details_list})
                        return_dict.update(item_response.pop('message'))
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
        if isinstance(response, list) and response:
            if any(item in response for item in ConvertId.ID_FORMATS):
                convert_id_response = ConvertId(Authentication.credentials[0], item_id, id_type=response[0], convert_to=response[1]).run()
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

    def delete_item(self, item_id, delete_type='MoveToDeletedItems'):
        if not isinstance(item_id, list):
            item_id = [item_id]
        return_list = []
        for item in item_id:
            if item:
                return_list.append(DeleteItem(item, delete_type=delete_type).run())
        return return_list

    def search_and_delete_message(self, query, thread_count=os.cpu_count()*5, what_if=False):
        return_list = []
        reference_id_list = []
        for mailbox in self.get_searchable_mailboxes():
            if mailbox:
                reference_id_list.append(mailbox.get('reference_id'))
        if not reference_id_list:
            print('No searchable mailboxes found')
            return None
        else:
            for item in self.execute_ews_search(query, reference_id_list, thread_count=thread_count):
                if item:
                    if what_if:
                        print('WHAT IF: About to delete message ID: {}'.format(item.get('id').get('id')))
                    else:
                        return_list.extend(self.delete_item(item.get('id').get('id')))
        return return_list

    def get_domain_settings(self, domain=None):
        return GetDomainSettings(domain=domain).run()

    def find_items(self, 
                    query_string, 
                    distinguished_folder_name='inbox', 
                    base_shape='AllProperties', 
                    include_mime_content=True, 
                    body_type='Best', 
                    traversal='Shallow', 
                    reset_cache=False, 
                    return_deleted_items=True, 
                    return_highlight_terms=True
        ):
        return_list = []
        for message in FindItem(query_string=query_string, distinguished_folder_name=distinguished_folder_name, base_shape=base_shape, include_mime_content=include_mime_content, body_type=body_type, traversal=traversal, reset_cache=reset_cache, return_deleted_items=return_deleted_items, return_highlight_terms=return_highlight_terms).run():
            if message:
                items = self.get_item(item_id=message.get('item_id').get('id'))
                if items:
                    for item in items:
                        return_list.append(item)
        return return_list

    def search_mailboxes_using_find_item(self, 
                    query_string, 
                    impersonation_list,
                    multi_threading=True,
                    thread_count=os.cpu_count()*5,
                    distinguished_folder_name='inbox', 
                    base_shape='AllProperties', 
                    include_mime_content=True, 
                    body_type='Best', 
                    traversal='Shallow', 
                    reset_cache=False, 
                    return_deleted_items=True, 
                    return_highlight_terms=True):
        if multi_threading:
            threads = []
            response = []
            chunks = self.chunk(impersonation_list, int(len(impersonation_list) / thread_count))
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                for chunk in chunks:
                    threads.append(executor.submit(self.__execute_multithreaded_find, query_string, distinguished_folder_name, base_shape, include_mime_content, body_type, traversal, reset_cache, return_deleted_items, return_highlight_terms, chunk))
                for task in as_completed(threads):
                    result = task.result()
                    if isinstance(result, list):
                        for item in result:
                            response.append(item)
            return response

    def create_search_folder(self, search_string, display_name='Search Folder', base_folder='inbox', traversal='Deep'):
        return CreateFolder(search_string=search_string, search_folder=True, display_name=display_name, base_folder=base_folder, traversal=traversal).run()

    def find_search_folder(self):
        return FindFolder().run()

    def delete_search_folder(self, folder_id):
        return DeleteFolder(folder_id=folder_id)

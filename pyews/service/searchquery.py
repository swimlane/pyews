
pass


import re
import datetime

SEARCH_QUERY_MAP = {
    'attachment': { 'type': str },
    'subject': { 'type': str },
    'body': { 'type': str },
    'to': { 'type': str },
    'from':{ 'type': str },
    'cc': { 'type': str },
    'bcc': { 'type': str },
    'participants': { 'type': str },
    'category': { 'type': str },
    'importance': { 'type': str },
    'kind': ['contacts','docs','email','externaldata','faxes','im','journals','meetings','microsoftteams','notes','posts','rssfeeds','tasks','voicemail'],
    'sent': { 'type': datetime.datetime },
    'received': { 'type': datetime.datetime },
    'hasattachment': { 'type': bool },
    'isflagged': { 'type': bool },
    'isread': { 'type': bool },
    'size': { 'type': int },
}

RELATIONAL_OPERATORS = ['<', '>', '=', '..']

OPERATORS = ['AND', 'OR', 'NOT']



class SearchQuery(object):
        
    def __init__(self, query):
        SEARCH_QUERY_MAP.values()
        
        split_query = re.split('[:]', query)
        for key, value in SEARCH_QUERY_MAP.items():
            if (key == split_query[0]):
                if (split_query[0] == 'kind'):
                    if (split_query[1] in value):
                        print(split_query[1])
               # elif (split_query[0] == 'sent'):

             #   elif (split_query[0] == 'received'):

              #  elif (split_query[0] == 'hasattachment'):

               # elif (split_query[0] == 'isflagged'):

                #elif (split_query[0] == 'isread'):

                else:
                    if (isinstance(split_query[1], value['type'])):
                        print(split_query)
            #if ()
'''
        valid_hashattachment = ['true', 'false']
        if hasattachment:
            if hasattachment not in valid_hashattachment:
                raise ValueError("results: hasattachment must be one of %r." % valid_hashattachment)

        valid_isread = ['true', 'false']
        if isread:
            if isread not in valid_isread:
                raise ValueError("results: isread must be one of %r." % valid_isread)

        valid_category = ['Blue Category', 'Green Category', 'Orange Category', 'Purple Category', 'Red Category', 'Yellow Category']
        if category:
            if category not in valid_category:
                raise ValueError("results: category must be one of %r." % valid_category)

        valid_kind = ['contacts','docs','email','externaldata','faxes','im','journals','meetings','microsoftteams','notes','posts','rssfeeds','tasks','voicemail']
        if kind:
            if kind not in valid_kind:
                raise ValueError("results: kind must be one of %r." % valid_kind)
'''    
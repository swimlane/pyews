
__SEARCHABLE_EMAIL_PROPERTIES__ = ['attachmentnames:', 'bcc:', 'category:', 'cc:', 'from:', 'hasattachment:', 'isread:', 'kind:', 'participants:', 'received', 'recipients:', 'sent', 'size:', 'subject:' 'to:']

class SearchQuery(object):
        
    def __init__(
        self,
        attachmentnames=None,
        bcc=None,
        cc=None,
        category=None,
        from_address=None,
        hasattachment=None,
        isread=None,
        kind=None,
        participants=None,
        received=None,
        recipients=None,
        sent=None,
        size=None,
        subject=None,
        to=None,
        **kwargs
        ):

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

        
    
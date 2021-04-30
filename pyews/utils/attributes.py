FOLDER_LIST = [
        'msgfolderroot',
        'calendar',
        'contacts',
        'deleteditems',
        'drafts',
        'inbox',
        'journal',
        'notes',
        'outbox',
        'sentitems',
        'tasks',
        'junkemail',
        'searchfolders',
        'voicemail',
        'recoverableitemsdeletions',
        'recoverableitemsversions',
        'recoverableitemspurges',
        'recipientcache',
        'quickcontacts',
        'conversationhistory',
        'todosearch',
        'mycontacts',
        'imcontactlist',
        'peopleconnect',
        'favorites'
    ]

MESSAGE_ELEMENTS = {
   "MimeContent": None,
   "ItemClass": [
       'AcceptItem',
       'CalendarItem',
       'Contact',
       'Conversation',
       'DeclineItem',
       'DistributionList',
       'GlobalItemClass',
       'Item',
       'MeetingCancellation',
       'MeetingMessage',
       'MettingRequest',
       'MeetingResponse',
       'Message',
       'RemoveItem',
       'Task',
       'TentativelyAcceptItem'
   ],
   "Subject": None,
   "Sensitivity": [
       'Normal',
       'Personal',
       'Private',
       'Confidential'
   ],
   "Body": {
       'BodyType': [
           'HTML',
           'Text'
       ],
       'IsTruncated': [
           'true',
           'false'
       ]
   },
   "Attachments": {
       'FileAttachment':{
           'Name': None,
           'IsInline': ['true', 'false'],
           'Content': None
       }
   },
   "Importance": [
       'Low',
       'Normal',
       'High'
   ],
   "IsSubmitted": [
       'true',
       'false'
   ],
   "IsDraft": [
       'true',
       'false'
   ],
   "DisplayCc": None,
   "DisplayTo": None,
   "Sender": {
       'Mailbox': {
           'Name': None,
           'EmailAddress': None,
           'MailboxType': [
               'Mailbox',
               'PublicDL',
               'PrivateDl',
               'Contact',
               'PublicFolder',
               'Unknown',
               'OneOff',
               'GroupMailbox'
           ]
       }
   },
   "ToRecipients": {
       'Mailbox': {
           'Name': None,
           'EmailAddress': None,
           'MailboxType': [
               'Mailbox',
               'PublicDL',
               'PrivateDl',
               'Contact',
               'PublicFolder',
               'Unknown',
               'OneOff',
               'GroupMailbox'
           ]
       }
   },
   "CcRecipients": {
       'Mailbox': {
           'Name': None,
           'EmailAddress': None,
           'MailboxType': [
               'Mailbox',
               'PublicDL',
               'PrivateDl',
               'Contact',
               'PublicFolder',
               'Unknown',
               'OneOff',
               'GroupMailbox'
           ]
       }
   },
   "BccRecipients": {
       'Mailbox': {
           'Name': None,
           'EmailAddress': None,
           'MailboxType': [
               'Mailbox',
               'PublicDL',
               'PrivateDl',
               'Contact',
               'PublicFolder',
               'Unknown',
               'OneOff',
               'GroupMailbox'
           ]
       }
   },
   "IsReadReceiptRequested": [
       'true',
       'false'
   ],
   "IsDeliveryReceiptRequested": [
       'true',
       'false'
   ],
   "From": {
       'Mailbox': {
           'Name': None,
           'EmailAddress': None,
           'MailboxType': [
               'Mailbox',
               'PublicDL',
               'PrivateDl',
               'Contact',
               'PublicFolder',
               'Unknown',
               'OneOff',
               'GroupMailbox'
           ]
       }
   },
   "IsRead": [
       'true',
       'false'
   ],
   "IsResponseRequested": [
       'true'
   ]
}
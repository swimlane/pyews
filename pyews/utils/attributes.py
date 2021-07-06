TRAVERSAL_LIST = [
    'Deep',
    'Shallow',
    'SoftDeleted',
    'Associated'
]

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

SEARCH_FILTERS = {
    'Contains': {
        'ContainmentMode': [
            'FullString',
            'Prefixed',
            'Substring',
            'PrefixOnWords',
            'ExactPhrase'
        ],
        'ContainmentComparison': [
            'Exact',
            'IgnoreCase',
            'IgnoreNonSpacingCharacters',
            'Loose',
            'IgnoreCaseAndNonSpacingCharacters',
            'LooseAndIgnoreCase',
            'LooseAndIgnoreNonSpace',
            'LooseAndIgnoreCaseAndIgnoreNonSpace'
        ]
    },
    'Excludes': {
        'Bitmask': []
    },
    'Exists': {},
    'IsEqualTo': {
        'FieldURIOrConstant': []
    },
    'IsNotEqualTo': {},
    'IsGreaterThan': {},
    'IsGreaterThanOrEqualTo': {},
    'IsLessThan': {},
    'IsLessThanOrEqualTo': {}
}

FIELD_URI_MAP = {
    'folder': [
        "FolderId",
        "ParentFolderId",
        "DisplayName",
        "UnreadCount",
        "TotalCount",
        "ChildFolderCount",
        "FolderClass",
        "SearchParameters",
        "ManagedFolderInformation",
        "PermissionSet",
        "EffectiveRights",
        "SharingEffectiveRights"
    ],
    'item': [
        "ItemId",
        "ParentFolderId",
        "ItemClass",
        "MimeContent",
        "Attachments",
        "Subject",
        "DateTimeReceived",
        "Size",
        "Categories",
        "HasAttachments",
        "Importance",
        "InReplyTo",
        "InternetMessageHeaders",
        "IsAssociated",
        "IsDraft",
        "IsFromMe",
        "IsResend",
        "IsSubmitted",
        "IsUnmodified",
        "DateTimeSent",
        "DateTimeCreated",
        "Body",
        "ResponseObjects",
        "Sensitivity",
        "ReminderDueBy",
        "ReminderIsSet",
        "ReminderNextTime",
        "ReminderMinutesBeforeStart",
        "DisplayTo",
        "DisplayCc",
        "Culture",
        "EffectiveRights",
        "LastModifiedName",
        "LastModifiedTime",
        "ConversationId",
        "UniqueBody",
        "Flag",
        "StoreEntryId",
        "InstanceKey",
        "NormalizedBody",
        "EntityExtractionResult",
        "ArchiveTag",
        "RetentionDate",
        "Preview",
        "NextPredictedAction",
        "GroupingAction",
        "PredictedActionReasons",
        "IsClutter",
        "RightsManagementLicenseData",
        "BlockStatus",
        "HasBlockedImages",
        "WebClientReadFormQueryString",
        "WebClientEditFormQueryString",
        "TextBody",
        "IconIndex",
        "MimeContentUTF8"
    ],
    'message': [
        "ConversationIndex",
        "ConversationTopic",
        "InternetMessageId",
        "IsRead",
        "IsResponseRequested",
        "IsReadReceiptRequested",
        "IsDeliveryReceiptRequested",
        "ReceivedBy",
        "ReceivedRepresenting",
        "References",
        "ReplyTo",
        "From",
        "Sender",
        "ToRecipients",
        "CcRecipients",
        "BccRecipients",
        "ApprovalRequestData",
        "VotingInformation",
        "ReminderMessageData",
    ],
    'meeting': [
        "AssociatedCalendarItemId",
        "IsDelegated",
        "IsOutOfDate",
        "HasBeenProcessed",
        "ResponseType",
        "ProposedStart",
        "PropsedEnd",
    ],
    'meetingRequest': [
        "MeetingRequestType",
        "IntendedFreeBusyStatus",
        "ChangeHighlights",
    ],
    'calendar': [
        "Start",
        "End",
        "OriginalStart",
        "StartWallClock",
        "EndWallClock",
        "StartTimeZoneId",
        "EndTimeZoneId",
        "IsAllDayEvent",
        "LegacyFreeBusyStatus",
        "Location",
        "When",
        "IsMeeting",
        "IsCancelled",
        "IsRecurring",
        "MeetingRequestWasSent",
        "IsResponseRequested",
        "CalendarItemType",
        "MyResponseType",
        "Organizer",
        "RequiredAttendees",
        "OptionalAttendees",
        "Resources",
        "ConflictingMeetingCount",
        "AdjacentMeetingCount",
        "ConflictingMeetings",
        "AdjacentMeetings",
        "Duration",
        "TimeZone",
        "AppointmentReplyTime",
        "AppointmentSequenceNumber",
        "AppointmentState",
        "Recurrence",
        "FirstOccurrence",
        "LastOccurrence",
        "ModifiedOccurrences",
        "DeletedOccurrences",
        "MeetingTimeZone",
        "ConferenceType",
        "AllowNewTimeProposal",
        "IsOnlineMeeting",
        "MeetingWorkspaceUrl",
        "NetShowUrl",
        "UID",
        "RecurrenceId",
        "DateTimeStamp",
        "StartTimeZone",
        "EndTimeZone",
        "JoinOnlineMeetingUrl",
        "OnlineMeetingSettings",
        "IsOrganizer",
    ],
    'task': [
        "ActualWork",
        "AssignedTime",
        "BillingInformation",
        "ChangeCount",
        "Companies",
        "CompleteDate",
        "Contacts",
        "DelegationState",
        "Delegator",
        "DueDate",
        "IsAssignmentEditable",
        "IsComplete",
        "IsRecurring",
        "IsTeamTask",
        "Mileage",
        "Owner",
        "PercentComplete",
        "Recurrence",
        "StartDate",
        "Status",
        "StatusDescription",
        "TotalWork",
    ],
    'contacts': [
        "Alias",
        "AssistantName",
        "Birthday",
        "BusinessHomePage",
        "Children",
        "Companies",
        "CompanyName",
        "CompleteName",
        "ContactSource",
        "Culture",
        "Department",
        "DisplayName",
        "DirectoryId",
        "DirectReports",
        "EmailAddresses",
        "FileAs",
        "FileAsMapping",
        "Generation",
        "GivenName",
        "ImAddresses",
        "Initials",
        "JobTitle",
        "Manager",
        "ManagerMailbox",
        "MiddleName",
        "Mileage",
        "MSExchangeCertificate",
        "Nickname",
        "Notes",
        "OfficeLocation",
        "PhoneNumbers",
        "PhoneticFullName",
        "PhoneticFirstName",
        "PhoneticLastName",
        "Photo",
        "PhysicalAddresses",
        "PostalAddressIndex",
        "Profession",
        "SpouseName",
        "Surname",
        "WeddingAnniversary",
        "UserSMIMECertificate",
        "HasPicture",
    ],
    'conversation': [
        "ConversationId",
        "ConversationTopic",
        "UniqueRecipients",
        "GlobalUniqueRecipients",
        "UniqueUnreadSenders",
        "GlobalUniqueUnreadSenders",
        "UniqueSenders",
        "GlobalUniqueSenders",
        "LastDeliveryTime",
        "GlobalLastDeliveryTime",
        "Categories",
        "GlobalCategories",
        "FlagStatus",
        "GlobalFlagStatus",
        "HasAttachments",
        "GlobalHasAttachments",
        "HasIrm",
        "GlobalHasIrm",
        "MessageCount",
        "GlobalMessageCount",
        "UnreadCount",
        "GlobalUnreadCount",
        "Size",
        "GlobalSize",
        "ItemClasses",
        "GlobalItemClasses",
        "Importance",
        "GlobalImportance",
        "ItemIds",
        "GlobalItemIds",
        "LastModifiedTime",
        "InstanceKey",
        "Preview",
        "GlobalParentFolderId",
        "NextPredictedAction",
        "GroupingAction",
        "IconIndex",
        "GlobalIconIndex",
        "DraftItemIds",
        "HasClutter",
    ],
    'persona': [
        "PersonaId",
        "PersonaType",
        "GivenName",
        "CompanyName",
        "Surname",
        "DisplayName",
        "EmailAddress",
        "FileAs",
        "HomeCity",
        "CreationTime",
        "RelevanceScore",
        "WorkCity",
        "PersonaObjectStatus",
        "FileAsId",
        "DisplayNamePrefix",
        "YomiCompanyName",
        "YomiFirstName",
        "YomiLastName",
        "Title",
        "EmailAddresses",
        "PhoneNumber",
        "ImAddress",
        "ImAddresses",
        "ImAddresses2",
        "ImAddresses3",
        "FolderIds",
        "Attributions",
        "DisplayNames",
        "Initials",
        "FileAses",
        "FileAsIds",
        "DisplayNamePrefixes",
        "GivenNames",
        "MiddleNames",
        "Surnames",
        "Generations",
        "Nicknames",
        "YomiCompanyNames",
        "YomiFirstNames",
        "YomiLastNames",
        "BusinessPhoneNumbers",
        "BusinessPhoneNumbers2",
        "HomePhones",
        "HomePhones2",
        "MobilePhones",
        "MobilePhones2",
        "AssistantPhoneNumbers",
        "CallbackPhones",
        "CarPhones",
        "HomeFaxes",
        "OrganizationMainPhones",
        "OtherFaxes",
        "OtherTelephones",
        "OtherPhones2",
        "Pagers",
        "RadioPhones",
        "TelexNumbers",
        "WorkFaxes",
        "Emails1",
        "Emails2",
        "Emails3",
        "BusinessHomePages",
        "School",
        "PersonalHomePages",
        "OfficeLocations",
        "BusinessAddresses",
        "HomeAddresses",
        "OtherAddresses",
        "Titles",
        "Departments",
        "CompanyNames",
        "Managers",
        "AssistantNames",
        "Professions",
        "SpouseNames",
        "Hobbies",
        "WeddingAnniversaries",
        "Birthdays",
        "Children",
        "Locations",
        "ExtendedProperties",
        "PostalAddress",
        "Bodies",
    ]
}

RESPONSE_CODES = [
    "NoError",
    "ErrorAccessDenied",
    "ErrorAccessModeSpecified",
    "ErrorAccountDisabled",
    "ErrorAddDelegatesFailed",
    "ErrorAddressSpaceNotFound",
    "ErrorADOperation",
    "ErrorADSessionFilter",
    "ErrorADUnavailable",
    "ErrorServiceUnavailable",
    "ErrorAutoDiscoverFailed",
    "ErrorAffectedTaskOccurrencesRequired",
    "ErrorAttachmentNestLevelLimitExceeded" ,
    "ErrorAttachmentSizeLimitExceeded",
    "ErrorArchiveFolderPathCreation",
    "ErrorArchiveMailboxNotEnabled",
    "ErrorArchiveMailboxServiceDiscoveryFailed",
    "ErrorAvailabilityConfigNotFound",
    "ErrorBatchProcessingStopped",
    "ErrorCalendarCannotMoveOrCopyOccurrence",
    "ErrorCalendarCannotUpdateDeletedItem",
    "ErrorCalendarCannotUseIdForOccurrenceId",
    "ErrorCalendarCannotUseIdForRecurringMasterId",
    "ErrorCalendarDurationIsTooLong",
    "ErrorCalendarEndDateIsEarlierThanStartDate",
    "ErrorCalendarFolderIsInvalidForCalendarView",
    "ErrorCalendarInvalidAttributeValue",
    "ErrorCalendarInvalidDayForTimeChangePattern",
    "ErrorCalendarInvalidDayForWeeklyRecurrence",
    "ErrorCalendarInvalidPropertyState",
    "ErrorCalendarInvalidPropertyValue",
    "ErrorCalendarInvalidRecurrence",
    "ErrorCalendarInvalidTimeZone",
    "ErrorCalendarIsCancelledForAccept",
    "ErrorCalendarIsCancelledForDecline",
    "ErrorCalendarIsCancelledForRemove",
    "ErrorCalendarIsCancelledForTentative",
    "ErrorCalendarIsDelegatedForAccept",
    "ErrorCalendarIsDelegatedForDecline",
    "ErrorCalendarIsDelegatedForRemove",
    "ErrorCalendarIsDelegatedForTentative",
    "ErrorCalendarIsNotOrganizer",
    "ErrorCalendarIsOrganizerForAccept",
    "ErrorCalendarIsOrganizerForDecline",
    "ErrorCalendarIsOrganizerForRemove",
    "ErrorCalendarIsOrganizerForTentative",
    "ErrorCalendarOccurrenceIndexIsOutOfRecurrenceRange",
    "ErrorCalendarOccurrenceIsDeletedFromRecurrence",
    "ErrorCalendarOutOfRange",
    "ErrorCalendarMeetingRequestIsOutOfDate",
    "ErrorCalendarViewRangeTooBig",
    "ErrorCallerIsInvalidADAccount",
    "ErrorCannotAccessDeletedPublicFolder",
    "ErrorCannotArchiveCalendarContactTaskFolderException",
    "ErrorCannotArchiveItemsInPublicFolders",
    "ErrorCannotArchiveItemsInArchiveMailbox",
    "ErrorCannotCreateCalendarItemInNonCalendarFolder",
    "ErrorCannotCreateContactInNonContactFolder",
    "ErrorCannotCreatePostItemInNonMailFolder",
    "ErrorCannotCreateTaskInNonTaskFolder",
    "ErrorCannotDeleteObject",
    "ErrorCannotDisableMandatoryExtension",
    "ErrorCannotFindUser",
    "ErrorCannotGetSourceFolderPath",
    "ErrorCannotGetExternalEcpUrl",
    "ErrorCannotOpenFileAttachment",
    "ErrorCannotDeleteTaskOccurrence",
    "ErrorCannotEmptyFolder",
    "ErrorCannotSetCalendarPermissionOnNonCalendarFolder",
    "ErrorCannotSetNonCalendarPermissionOnCalendarFolder",
    "ErrorCannotSetPermissionUnknownEntries",
    "ErrorCannotSpecifySearchFolderAsSourceFolder",
    "ErrorCannotUseFolderIdForItemId",
    "ErrorCannotUseItemIdForFolderId",
    "ErrorChangeKeyRequired",
    "ErrorChangeKeyRequiredForWriteOperations",
    "ErrorClientDisconnected",
    "ErrorClientIntentInvalidStateDefinition",
    "ErrorClientIntentNotFound",
    "ErrorConnectionFailed",
    "ErrorContainsFilterWrongType",
    "ErrorContentConversionFailed",
    "ErrorContentIndexingNotEnabled",
    "ErrorCorruptData",
    "ErrorCreateItemAccessDenied",
    "ErrorCreateManagedFolderPartialCompletion",
    "ErrorCreateSubfolderAccessDenied",
    "ErrorCrossMailboxMoveCopy",
    "ErrorCrossSiteRequest",
    "ErrorDataSizeLimitExceeded",
    "ErrorDataSourceOperation",
    "ErrorDelegateAlreadyExists",
    "ErrorDelegateCannotAddOwner",
    "ErrorDelegateMissingConfiguration",
    "ErrorDelegateNoUser",
    "ErrorDelegateValidationFailed",
    "ErrorDeleteDistinguishedFolder",
    "ErrorDeleteItemsFailed",
    "ErrorDeleteUnifiedMessagingPromptFailed",
    "ErrorDistinguishedUserNotSupported",
    "ErrorDistributionListMemberNotExist",
    "ErrorDuplicateInputFolderNames",
    "ErrorDuplicateUserIdsSpecified",
    "ErrorDuplicateTransactionId",
    "ErrorEmailAddressMismatch",
    "ErrorEventNotFound",
    "ErrorExceededConnectionCount",
    "ErrorExceededSubscriptionCount",
    "ErrorExceededFindCountLimit",
    "ErrorExpiredSubscription",
    "ErrorExtensionNotFound",
    "ErrorExtensionsNotAuthorized",
    "ErrorFolderCorrupt",
    "ErrorFolderNotFound",
    "ErrorFolderPropertRequestFailed",
    "ErrorFolderSave",
    "ErrorFolderSaveFailed",
    "ErrorFolderSavePropertyError",
    "ErrorFolderExists",
    "ErrorFreeBusyGenerationFailed",
    "ErrorGetServerSecurityDescriptorFailed",
    "ErrorImContactLimitReached",
    "ErrorImGroupDisplayNameAlreadyExists",
    "ErrorImGroupLimitReached",
    "ErrorImpersonateUserDenied",
    "ErrorImpersonationDenied",
    "ErrorImpersonationFailed",
    "ErrorIncorrectSchemaVersion",
    "ErrorIncorrectUpdatePropertyCount",
    "ErrorIndividualMailboxLimitReached",
    "ErrorInsufficientResources",
    "ErrorInternalServerError",
    "ErrorInternalServerTransientError",
    "ErrorInvalidAccessLevel",
    "ErrorInvalidArgument",
    "ErrorInvalidAttachmentId",
    "ErrorInvalidAttachmentSubfilter",
    "ErrorInvalidAttachmentSubfilterTextFilter",
    "ErrorInvalidAuthorizationContext",
    "ErrorInvalidChangeKey",
    "ErrorInvalidClientSecurityContext",
    "ErrorInvalidCompleteDate",
    "ErrorInvalidContactEmailAddress",
    "ErrorInvalidContactEmailIndex",
    "ErrorInvalidCrossForestCredentials",
    "ErrorInvalidDelegatePermission",
    "ErrorInvalidDelegateUserId",
    "ErrorInvalidExcludesRestriction",
    "ErrorInvalidExpressionTypeForSubFilter",
    "ErrorInvalidExtendedProperty",
    "ErrorInvalidExtendedPropertyValue",
    "ErrorInvalidFolderId",
    "ErrorInvalidFolderTypeForOperation",
    "ErrorInvalidFractionalPagingParameters",
    "ErrorInvalidFreeBusyViewType",
    "ErrorInvalidId",
    "ErrorInvalidIdEmpty",
    "ErrorInvalidIdMalformed",
    "ErrorInvalidIdMalformedEwsLegacyIdFormat",
    "ErrorInvalidIdMonikerTooLong",
    "ErrorInvalidIdNotAnItemAttachmentId",
    "ErrorInvalidIdReturnedByResolveNames",
    "ErrorInvalidIdStoreObjectIdTooLong",
    "ErrorInvalidIdTooManyAttachmentLevels",
    "ErrorInvalidIdXml",
    "ErrorInvalidImContactId",
    "ErrorInvalidImDistributionGroupSmtpAddress",
    "ErrorInvalidImGroupId",
    "ErrorInvalidIndexedPagingParameters",
    "ErrorInvalidInternetHeaderChildNodes",
    "ErrorInvalidItemForOperationArchiveItem",
    "ErrorInvalidItemForOperationCreateItemAttachment",
    "ErrorInvalidItemForOperationCreateItem",
    "ErrorInvalidItemForOperationAcceptItem",
    "ErrorInvalidItemForOperationDeclineItem",
    "ErrorInvalidItemForOperationCancelItem",
    "ErrorInvalidItemForOperationExpandDL",
    "ErrorInvalidItemForOperationRemoveItem",
    "ErrorInvalidItemForOperationSendItem",
    "ErrorInvalidItemForOperationTentative",
    "ErrorInvalidLogonType",
    "ErrorInvalidLikeRequest",
    "ErrorInvalidMailbox",
    "ErrorInvalidManagedFolderProperty",
    "ErrorInvalidManagedFolderQuota",
    "ErrorInvalidManagedFolderSize",
    "ErrorInvalidMergedFreeBusyInterval",
    "ErrorInvalidNameForNameResolution",
    "ErrorInvalidOperation",
    "ErrorInvalidNetworkServiceContext",
    "ErrorInvalidOofParameter",
    "ErrorInvalidPagingMaxRows",
    "ErrorInvalidParentFolder",
    "ErrorInvalidPercentCompleteValue",
    "ErrorInvalidPermissionSettings",
    "ErrorInvalidPhoneCallId",
    "ErrorInvalidPhoneNumber",
    "ErrorInvalidUserInfo",
    "ErrorInvalidPropertyAppend",
    "ErrorInvalidPropertyDelete",
    "ErrorInvalidPropertyForExists",
    "ErrorInvalidPropertyForOperation",
    "ErrorInvalidPropertyRequest",
    "ErrorInvalidPropertySet",
    "ErrorInvalidPropertyUpdateSentMessage",
    "ErrorInvalidProxySecurityContext",
    "ErrorInvalidPullSubscriptionId",
    "ErrorInvalidPushSubscriptionUrl",
    "ErrorInvalidRecipients",
    "ErrorInvalidRecipientSubfilter",
    "ErrorInvalidRecipientSubfilterComparison",
    "ErrorInvalidRecipientSubfilterOrder",
    "ErrorInvalidRecipientSubfilterTextFilter",
    "ErrorInvalidReferenceItem",
    "ErrorInvalidRequest",
    "ErrorInvalidRestriction",
    "ErrorInvalidRetentionTagTypeMismatch",
    "ErrorInvalidRetentionTagInvisible",
    "ErrorInvalidRetentionTagInheritance",
    "ErrorInvalidRetentionTagIdGuid",
    "ErrorInvalidRoutingType",
    "ErrorInvalidScheduledOofDuration",
    "ErrorInvalidSchemaVersionForMailboxVersion",
    "ErrorInvalidSecurityDescriptor",
    "ErrorInvalidSendItemSaveSettings",
    "ErrorInvalidSerializedAccessToken",
    "ErrorInvalidServerVersion",
    "ErrorInvalidSid",
    "ErrorInvalidSIPUri",
    "ErrorInvalidSmtpAddress",
    "ErrorInvalidSubfilterType",
    "ErrorInvalidSubfilterTypeNotAttendeeType",
    "ErrorInvalidSubfilterTypeNotRecipientType",
    "ErrorInvalidSubscription",
    "ErrorInvalidSubscriptionRequest",
    "ErrorInvalidSyncStateData",
    "ErrorInvalidTimeInterval",
    "ErrorInvalidUserOofSettings",
    "ErrorInvalidUserPrincipalName",
    "ErrorInvalidUserSid",
    "ErrorInvalidUserSidMissingUPN",
    "ErrorInvalidValueForProperty",
    "ErrorInvalidWatermark",
    "ErrorIPGatewayNotFound",
    "ErrorIrresolvableConflict",
    "ErrorItemCorrupt",
    "ErrorItemNotFound",
    "ErrorItemPropertyRequestFailed",
    "ErrorItemSave",
    "ErrorItemSavePropertyError",
    "ErrorLegacyMailboxFreeBusyViewTypeNotMerged",
    "ErrorLocalServerObjectNotFound",
    "ErrorLogonAsNetworkServiceFailed",
    "ErrorMailboxConfiguration",
    "ErrorMailboxDataArrayEmpty",
    "ErrorMailboxDataArrayTooBig",
    "ErrorMailboxHoldNotFound",
    "ErrorMailboxLogonFailed",
    "ErrorMailboxMoveInProgress",
    "ErrorMailboxStoreUnavailable",
    "ErrorMailRecipientNotFound",
    "ErrorMailTipsDisabled",
    "ErrorManagedFolderAlreadyExists",
    "ErrorManagedFolderNotFound",
    "ErrorManagedFoldersRootFailure",
    "ErrorMeetingSuggestionGenerationFailed",
    "ErrorMessageDispositionRequired",
    "ErrorMessageSizeExceeded",
    "ErrorMimeContentConversionFailed",
    "ErrorMimeContentInvalid",
    "ErrorMimeContentInvalidBase64String",
    "ErrorMissingArgument",
    "ErrorMissingEmailAddress",
    "ErrorMissingEmailAddressForManagedFolder",
    "ErrorMissingInformationEmailAddress",
    "ErrorMissingInformationReferenceItemId",
    "ErrorMissingItemForCreateItemAttachment",
    "ErrorMissingManagedFolderId",
    "ErrorMissingRecipients",
    "ErrorMissingUserIdInformation",
    "ErrorMoreThanOneAccessModeSpecified",
    "ErrorMoveCopyFailed",
    "ErrorMoveDistinguishedFolder",
    "ErrorMoveUnifiedGroupPropertyFailed",
    "ErrorMultiLegacyMailboxAccess",
    "ErrorNameResolutionMultipleResults",
    "ErrorNameResolutionNoMailbox",
    "ErrorNameResolutionNoResults",
    "ErrorNoApplicableProxyCASServersAvailable",
    "ErrorNoCalendar",
    "ErrorNoDestinationCASDueToKerberosRequirements",
    "ErrorNoDestinationCASDueToSSLRequirements",
    "ErrorNoDestinationCASDueToVersionMismatch",
    "ErrorNoFolderClassOverride",
    "ErrorNoFreeBusyAccess",
    "ErrorNonExistentMailbox",
    "ErrorNonPrimarySmtpAddress",
    "ErrorNoPropertyTagForCustomProperties",
    "ErrorNoPublicFolderReplicaAvailable",
    "ErrorNoPublicFolderServerAvailable",
    "ErrorNoRespondingCASInDestinationSite",
    "ErrorNotDelegate",
    "ErrorNotEnoughMemory",
    "ErrorObjectTypeChanged",
    "ErrorOccurrenceCrossingBoundary",
    "ErrorOccurrenceTimeSpanTooBig" ,
    "ErrorOperationNotAllowedWithPublicFolderRoot" ,
    "ErrorParentFolderIdRequired",
    "ErrorParentFolderNotFound",
    "ErrorPasswordChangeRequired",
    "ErrorPasswordExpired",
    "ErrorPhoneNumberNotDialable",
    "ErrorPropertyUpdate",
    "ErrorPromptPublishingOperationFailed",
    "ErrorPropertyValidationFailure",
    "ErrorProxiedSubscriptionCallFailure",
    "ErrorProxyCallFailed",
    "ErrorProxyGroupSidLimitExceeded",
    "ErrorProxyRequestNotAllowed",
    "ErrorProxyRequestProcessingFailed",
    "ErrorProxyServiceDiscoveryFailed",
    "ErrorProxyTokenExpired",
    "ErrorPublicFolderMailboxDiscoveryFailed",
    "ErrorPublicFolderOperationFailed",
    "ErrorPublicFolderRequestProcessingFailed",
    "ErrorPublicFolderServerNotFound",
    "ErrorPublicFolderSyncException",
    "ErrorQueryFilterTooLong",
    "ErrorQuotaExceeded",
    "ErrorReadEventsFailed",
    "ErrorReadReceiptNotPending",
    "ErrorRecurrenceEndDateTooBig",
    "ErrorRecurrenceHasNoOccurrence",
    "ErrorRemoveDelegatesFailed",
    "ErrorRequestAborted",
    "ErrorRequestStreamTooBig",
    "ErrorRequiredPropertyMissing",
    "ErrorResolveNamesInvalidFolderType",
    "ErrorResolveNamesOnlyOneContactsFolderAllowed",
    "ErrorResponseSchemaValidation",
    "ErrorRestrictionTooLong",
    "ErrorRestrictionTooComplex",
    "ErrorResultSetTooBig",
    "ErrorInvalidExchangeImpersonationHeaderData",
    "ErrorSavedItemFolderNotFound",
    "ErrorSchemaValidation",
    "ErrorSearchFolderNotInitialized",
    "ErrorSendAsDenied",
    "ErrorSendMeetingCancellationsRequired",
    "ErrorSendMeetingInvitationsOrCancellationsRequired",
    "ErrorSendMeetingInvitationsRequired",
    "ErrorSentMeetingRequestUpdate",
    "ErrorSentTaskRequestUpdate",
    "ErrorServerBusy",
    "ErrorServiceDiscoveryFailed",
    "ErrorStaleObject",
    "ErrorSubmissionQuotaExceeded",
    "ErrorSubscriptionAccessDenied",
    "ErrorSubscriptionDelegateAccessNotSupported",
    "ErrorSubscriptionNotFound",
    "ErrorSubscriptionUnsubscribed",
    "ErrorSyncFolderNotFound",
    "ErrorTeamMailboxNotFound",
    "ErrorTeamMailboxNotLinkedToSharePoint",
    "ErrorTeamMailboxUrlValidationFailed",
    "ErrorTeamMailboxNotAuthorizedOwner",
    "ErrorTeamMailboxActiveToPendingDelete",
    "ErrorTeamMailboxFailedSendingNotifications",
    "ErrorTeamMailboxErrorUnknown",
    "ErrorTimeIntervalTooBig",
    "ErrorTimeoutExpired",
    "ErrorTimeZone",
    "ErrorToFolderNotFound",
    "ErrorTokenSerializationDenied",
    "ErrorTooManyObjectsOpened",
    "ErrorUpdatePropertyMismatch",
    "ErrorAccessingPartialCreatedUnifiedGroup",
    "ErrorUnifiedGroupMailboxAADCreationFailed",
    "ErrorUnifiedGroupMailboxAADDeleteFailed",
    "ErrorUnifiedGroupMailboxNamingPolicy",
    "ErrorUnifiedGroupMailboxDeleteFailed",
    "ErrorUnifiedGroupMailboxNotFound",
    "ErrorUnifiedGroupMailboxUpdateDelayed",
    "ErrorUnifiedGroupMailboxUpdatedPartialProperties",
    "ErrorUnifiedGroupMailboxUpdateFailed",
    "ErrorUnifiedGroupMailboxProvisionFailed",
    "ErrorUnifiedMessagingDialPlanNotFound",
    "ErrorUnifiedMessagingReportDataNotFound",
    "ErrorUnifiedMessagingPromptNotFound",
    "ErrorUnifiedMessagingRequestFailed",
    "ErrorUnifiedMessagingServerNotFound",
    "ErrorUnableToGetUserOofSettings",
    "ErrorUnableToRemoveImContactFromGroup",
    "ErrorUnsupportedSubFilter",
    "ErrorUnsupportedCulture",
    "ErrorUnsupportedMapiPropertyType",
    "ErrorUnsupportedMimeConversion",
    "ErrorUnsupportedPathForQuery",
    "ErrorUnsupportedPathForSortGroup",
    "ErrorUnsupportedPropertyDefinition",
    "ErrorUnsupportedQueryFilter",
    "ErrorUnsupportedRecurrence",
    "ErrorUnsupportedTypeForConversion",
    "ErrorUpdateDelegatesFailed",
    "ErrorUserNotUnifiedMessagingEnabled",
    "ErrorVoiceMailNotImplemented",
    "ErrorValueOutOfRange",
    "ErrorVirusDetected",
    "ErrorVirusMessageDeleted",
    "ErrorWebRequestInInvalidState",
    "ErrorWin32InteropError",
    "ErrorWorkingHoursSaveFailed",
    "ErrorWorkingHoursXmlMalformed",
    "ErrorWrongServerVersion",
    "ErrorWrongServerVersionDelegate",
    "ErrorMissingInformationSharingFolderId",
    "ErrorDuplicateSOAPHeader" ,
    "ErrorSharingSynchronizationFailed" ,
    "ErrorSharingNoExternalEwsAvailable" ,
    "ErrorFreeBusyDLLimitReached",
    "ErrorInvalidGetSharingFolderRequest" ,
    "ErrorNotAllowedExternalSharingByPolicy" ,
    "ErrorUserNotAllowedByPolicy" ,
    "ErrorPermissionNotAllowedByPolicy" ,
    "ErrorOrganizationNotFederated" ,
    "ErrorMailboxFailover" ,
    "ErrorInvalidExternalSharingInitiator" ,
    "ErrorMessageTrackingPermanentError" ,
    "ErrorMessageTrackingTransientError" ,
    "ErrorMessageTrackingNoSuchDomain" ,
    "ErrorUserWithoutFederatedProxyAddress" ,
    "ErrorInvalidOrganizationRelationshipForFreeBusy" ,
    "ErrorInvalidFederatedOrganizationId" ,
    "ErrorInvalidExternalSharingSubscriber" ,
    "ErrorInvalidSharingData" ,
    "ErrorInvalidSharingMessage" ,
    "ErrorNotSupportedSharingMessage" ,
    "ErrorApplyConversationActionFailed" ,
    "ErrorInboxRulesValidationError" ,
    "ErrorOutlookRuleBlobExists" ,
    "ErrorRulesOverQuota" ,
    "ErrorNewEventStreamConnectionOpened" ,
    "ErrorMissedNotificationEvents" ,
    "ErrorDuplicateLegacyDistinguishedName" ,
    "ErrorInvalidClientAccessTokenRequest" ,
    "ErrorUnauthorizedClientAccessTokenRequest" ,
    "ErrorNoSpeechDetected" ,
    "ErrorUMServerUnavailable" ,
    "ErrorRecipientNotFound" ,
    "ErrorRecognizerNotInstalled" ,
    "ErrorSpeechGrammarError" ,
    "ErrorInvalidManagementRoleHeader" ,
    "ErrorLocationServicesDisabled",
    "ErrorLocationServicesRequestTimedOut",
    "ErrorLocationServicesRequestFailed",
    "ErrorLocationServicesInvalidRequest",
    "ErrorWeatherServiceDisabled",
    "ErrorMailboxScopeNotAllowedWithoutQueryString" ,
    "ErrorArchiveMailboxSearchFailed" ,
    "ErrorGetRemoteArchiveFolderFailed" ,
    "ErrorFindRemoteArchiveFolderFailed" ,
    "ErrorGetRemoteArchiveItemFailed" ,
    "ErrorExportRemoteArchiveItemsFailed" ,
    "ErrorInvalidPhotoSize" ,
    "ErrorSearchQueryHasTooManyKeywords",
    "ErrorSearchTooManyMailboxes",
    "ErrorInvalidRetentionTagNone",
    "ErrorDiscoverySearchesDisabled",
    "ErrorCalendarSeekToConditionNotSupported",
    "ErrorCalendarIsGroupMailboxForAccept",
    "ErrorCalendarIsGroupMailboxForDecline",
    "ErrorCalendarIsGroupMailboxForTentative",
    "ErrorCalendarIsGroupMailboxForSuppressReadReceipt",
    "ErrorOrganizationAccessBlocked",
    "ErrorInvalidLicense",
    "ErrorMessagePerFolderCountReceiveQuotaExceeded",
    "ErrorInvalidBulkActionType",
    "ErrorInvalidKeepNCount",
    "ErrorInvalidKeepNType",
    "ErrorNoOAuthServerAvailableForRequest",  
    "ErrorInstantSearchSessionExpired",
    "ErrorInstantSearchTimeout",
    "ErrorInstantSearchFailed",
    "ErrorUnsupportedUserForExecuteSearch",
    "ErrorDuplicateExtendedKeywordDefinition",
    "ErrorMissingExchangePrincipal",
    "ErrorUnexpectedUnifiedGroupsCount",
    "ErrorParsingXMLResponse",
    "ErrorInvalidFederationOrganizationIdentifier",
    "ErrorInvalidSweepRule",
    "ErrorInvalidSweepRuleOperationType",
    "ErrorTargetDomainNotSupported",
    "ErrorInvalidInternetWebProxyOnLocalServer",
    "ErrorNoSenderRestrictionsSettingsFoundInRequest",
    "ErrorDuplicateSenderRestrictionsInputFound",
    "ErrorSenderRestrictionsUpdateFailed",
    "ErrorMessageSubmissionBlocked",
    "ErrorExceededMessageLimit",
    "ErrorExceededMaxRecipientLimitBlock",
    "ErrorAccountSuspend",
    "ErrorExceededMaxRecipientLimit",
    "ErrorMessageBlocked",
    "ErrorAccountSuspendShowTierUpgrade",
    "ErrorExceededMessageLimitShowTierUpgrade",
    "ErrorExceededMaxRecipientLimitShowTierUpgrade",
    "ErrorInvalidLongitude",
    "ErrorInvalidLatitude",
    "ErrorProxySoapException",
    "ErrorUnifiedGroupAlreadyExists",
    "ErrorUnifiedGroupAadAuthorizationRequestDenied",
    "ErrorUnifiedGroupCreationDisabled",
    "ErrorMarketPlaceExtensionAlreadyInstalledForOrg",
    "ErrorExtensionAlreadyInstalledForOrg",
    "ErrorNewerExtensionAlreadyInstalled",
    "ErrorNewerMarketPlaceExtensionAlreadyInstalled",
    "ErrorInvalidExtensionId",
    "ErrorCannotUninstallProvidedExtensions",
    "ErrorNoRbacPermissionToInstallMarketPlaceExtensions",
    "ErrorNoRbacPermissionToInstallReadWriteMailboxExtensions",
    "ErrorInvalidReportMessageActionType",
    "ErrorCannotDownloadExtensionManifest",
    "ErrorCalendarForwardActionNotAllowed",
    "ErrorUnifiedGroupAliasNamingPolicy",
    "ErrorSubscriptionsDisabledForGroup",
    "ErrorCannotFindFileAttachment",
    "ErrorInvalidValueForFilter",
    "ErrorQuotaExceededOnDelete",
    "ErrorAccessDeniedDueToCompliance",
    "ErrorRecoverableItemsAccessDenied"
]
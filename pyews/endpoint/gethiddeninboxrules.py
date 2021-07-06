from ..service import Operation


class GetHiddenInboxRules(Operation):
    """FindItem EWS Operation attempts to find
    hidden inbox rules based on ExtendedFieldURI properties.
    """

    RESULTS_KEY = 'Items'

    def soap(self):
        return self.M_NAMESPACE.FindItem(
            self.M_NAMESPACE.ItemShape(
                self.T_NAMESPACE.BaseShape('IdOnly'),
                self.T_NAMESPACE.AdditionalProperties(
                    self.T_NAMESPACE.ExtendedFieldURI(PropertyTag="0x65EC", PropertyType="String"),
                    self.T_NAMESPACE.ExtendedFieldURI(PropertyTag="0x0E99", PropertyType="Binary"),
                    self.T_NAMESPACE.ExtendedFieldURI(PropertyTag="0x0E9A", PropertyType="Binary"),
                    self.T_NAMESPACE.ExtendedFieldURI(PropertyTag="0x65E9", PropertyType="Integer"),
                    self.T_NAMESPACE.ExtendedFieldURI(PropertyTag="0x6800", PropertyType="String"),
                    self.T_NAMESPACE.ExtendedFieldURI(PropertyTag="0x65EB", PropertyType="String"),
                    self.T_NAMESPACE.ExtendedFieldURI(PropertyTag="0x3FEA", PropertyType="Boolean"),
                    self.T_NAMESPACE.ExtendedFieldURI(PropertyTag="0x6645", PropertyType="Binary"),
                )
            ),
            self.M_NAMESPACE.Restriction(
                self.T_NAMESPACE.IsEqualTo(
                    self.T_NAMESPACE.FieldURI(FieldURI="item:ItemClass"),
                    self.T_NAMESPACE.FieldURIOrConstant(
                        self.T_NAMESPACE.Constant(Value="IPM.Rule.Version2.Message")
                    )
                )
            ),
            self.M_NAMESPACE.ParentFolderIds(
                self.T_NAMESPACE.DistinguishedFolderId(Id="inbox")
            ),
            Traversal="Shallow")

from .base import Base, etree, abc


class Operation(Base):
    """Operation class inherits from the Base class
    and defines namespaces, headers, and body
    of EWS Operation SOAP request
    """

    def get(self, exchange_version):
        self.__logger.info('Building SOAP request for {current}'.format(current=self.__class__.__name__))
        ENVELOPE = self.SOAP_MESSAGE_ELEMENT.Envelope
        HEADER = self.SOAP_NAMESPACE.Header
        self.envelope = ENVELOPE(
            HEADER(
                self.T_NAMESPACE.RequestedServerVersion(Version=exchange_version),
                self._impersonation_header()
            ),
            self.BODY_ELEMENT(
                self.soap()
            )
        )
        return etree.tostring(self.envelope)

    @abc.abstractmethod
    def soap(self):
        raise NotImplementedError

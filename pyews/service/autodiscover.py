from .base import Base, ElementMaker, abc, etree, Authentication


class Autodiscover(Base):
    """Autodiscover class inherits from the Base class
    and defines namespaces, headers, and body
    of an Autodiscover SOAP request
    """

    AUTODISCOVER_MAP  = {
        'wsa': "http://www.w3.org/2005/08/addressing",
        'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'soap': "http://schemas.xmlsoap.org/soap/envelope/",
        'a': "http://schemas.microsoft.com/exchange/2010/Autodiscover"
    }
    AUTODISCOVER_NAMESPACE = ElementMaker(
        namespace=Base.NAMESPACE_MAP['soap'],
        nsmap=AUTODISCOVER_MAP
    )
    BODY_ELEMENT = ElementMaker(namespace=AUTODISCOVER_MAP['soap']).Body
    A_NAMESPACE = ElementMaker(namespace=AUTODISCOVER_MAP['a'], nsmap={'a': AUTODISCOVER_MAP['a']})
    WSA_NAMESPACE = ElementMaker(namespace=AUTODISCOVER_MAP['wsa'], nsmap={'wsa': AUTODISCOVER_MAP['wsa']})

    @property
    def to(self):
        return Authentication.credentials[0]

    def get(self, exchange_version):
        self.__logger.info('Building Autodiscover SOAP request for {current}'.format(current=self.__class__.__name__))
        ENVELOPE = self.AUTODISCOVER_NAMESPACE.Envelope
        HEADER = self.SOAP_NAMESPACE.Header   
        self.A_NAMESPACE = ElementMaker(namespace=self.AUTODISCOVER_MAP['a'], nsmap={'a': self.AUTODISCOVER_MAP['a']})
        self.envelope = ENVELOPE(
            HEADER(
                self.A_NAMESPACE.RequestedServerVersion(exchange_version),
                self.WSA_NAMESPACE.Action('http://schemas.microsoft.com/exchange/2010/Autodiscover/Autodiscover/{}'.format(self.__class__.__name__)),
                self.WSA_NAMESPACE.To(self.to)
            ),
            self.BODY_ELEMENT(
                self.soap()
            )
        )
        return etree.tostring(self.envelope)

    @abc.abstractmethod
    def soap(self):
        raise NotImplementedError

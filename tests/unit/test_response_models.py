from __future__ import absolute_import, division, print_function
from lxml import etree

from symantecssl import utils
from symantecssl.models import OrderContacts, ContactInfo
from symantecssl.response_models import (
    Certificate, CertificateInfo, IntermediateCertificate, ModificationEvent,
    ModificationEvents, OrganizationInfo, OrderDetail, OrderDetails,
    OrderResponseHeader, QuickOrderResponse, QuickOrderResult, Vulnerabilities
)


class TestOrganizationInfo(object):

    def test_deserialize(self):

        xml_node = etree.fromstring(
            b"""<?xml version="1.0" encoding="UTF-8"?>
<m:OrganizationInfo xmlns:m="http://api.geotrust.com/webtrust/query">
    <m:OrganizationName>MyOrg</m:OrganizationName>
    <m:OrganizationAddress>
        <m:City>San Antonio</m:City>
        <m:Region>Texas</m:Region>
        <m:Country>US</m:Country>
    </m:OrganizationAddress>
</m:OrganizationInfo>
            """)

        org_info = OrganizationInfo.deserialize(xml_node)

        assert org_info.name == "MyOrg"
        assert org_info.city == "San Antonio"
        assert org_info.region == "Texas"
        assert org_info.country == "US"


class TestOrderContacts(object):

    def test_deserialize(self):

        xml_node = etree.fromstring(
            b"""<?xml version="1.0" encoding="UTF-8"?>
<m:OrderContacts xmlns:m="http://api.geotrust.com/webtrust/query">
    <m:AdminContact>
        <m:FirstName>John</m:FirstName>
        <m:LastName>Doe</m:LastName>
        <m:Phone>2103122400</m:Phone>
        <m:Email>someone@email.com</m:Email>
        <m:Title>Caesar</m:Title>
    </m:AdminContact>
    <m:TechContact>
        <m:FirstName>John</m:FirstName>
        <m:LastName>Doe</m:LastName>
        <m:Phone>2103122400</m:Phone>
        <m:Email>someone@email.com</m:Email>
        <m:Title>Caesar</m:Title>
    </m:TechContact>
    <m:BillingContact>
        <m:FirstName>John</m:FirstName>
        <m:LastName>Doe</m:LastName>
        <m:Phone>2103122400</m:Phone>
        <m:Email>someone@email.com</m:Email>
        <m:Title>Caesar</m:Title>
    </m:BillingContact>
</m:OrderContacts>
            """)

        contacts = OrderContacts.deserialize(xml_node)

        assert contacts.admin, ContactInfo
        assert contacts.tech, ContactInfo
        assert contacts.billing, ContactInfo


class TestContactInfo(object):

    def test_deserialize(self):

        xml_node = etree.fromstring(
            b"""<?xml version="1.0" encoding="UTF-8"?>
    <m:AdminContact xmlns:m="http://api.geotrust.com/webtrust/query">
        <m:FirstName>John</m:FirstName>
        <m:LastName>Doe</m:LastName>
        <m:Phone>2103122400</m:Phone>
        <m:Email>someone@email.com</m:Email>
        <m:Title>Caesar</m:Title>
    </m:AdminContact>
            """)

        contact = ContactInfo.deserialize(xml_node)

        assert contact.first_name == "John"
        assert contact.last_name == "Doe"
        assert contact.phone == "2103122400"
        assert contact.email == "someone@email.com"
        assert contact.title == "Caesar"


class TestCertificateInfo(object):

    def test_deserialize(self):
        xml_node = etree.fromstring(
            b"""<?xml version="1.0" encoding="UTF-8"?>
<m:CertificateInfo xmlns:m="http://api.geotrust.com/webtrust/query">
<m:CertificateStatus>ACTIVE</m:CertificateStatus>
<m:StartDate>2014-11-20T12:48:39+00:00</m:StartDate>
<m:EndDate>2014-11-28T23:02:59+00:00</m:EndDate>
<m:CommonName>example.com</m:CommonName>
<m:SerialNumber>1234</m:SerialNumber>
<m:OrganizationalUnit>Org Unit 1</m:OrganizationalUnit>
<m:OrganizationalUnit2>Org Unit 2</m:OrganizationalUnit2>
<m:OrganizationalUnit3>Org Unit 3</m:OrganizationalUnit3>
<m:WebServerType>other</m:WebServerType>
<m:AlgorithmInfo>
<m:SignatureHashAlgorithm>SHA1</m:SignatureHashAlgorithm>
<m:SignatureEncryptionAlgorithm>RSA</m:SignatureEncryptionAlgorithm>
</m:AlgorithmInfo>
</m:CertificateInfo>
            """)

        certificate_info = CertificateInfo.deserialize(xml_node)
        assert certificate_info.common_name == "example.com"
        assert certificate_info.status == "ACTIVE"
        assert certificate_info.hash_algorithm == "SHA1"
        assert certificate_info.encryption_algorithm == "RSA"


class TestCertificate(object):

    def test_deserialize(self):
        xml_node = etree.fromstring(
            b"""<?xml version="1.0" encoding="UTF-8"?>
<m:Fulfillment xmlns:m="http://api.geotrust.com/webtrust/query">
<m:CACertificates>
<m:CACertificate>
<m:Type>INTERMEDIATE</m:Type>
<m:CACert>-----BEGIN CERTIFICATE-----
DEF
-----END CERTIFICATE-----</m:CACert>
</m:CACertificate>
<m:CACertificate>
<m:Type>INTERMEDIATE</m:Type>
<m:CACert>-----BEGIN CERTIFICATE-----
MNO
-----END CERTIFICATE-----</m:CACert>
</m:CACertificate>
<m:CACertificate>
<m:Type>ROOT</m:Type>
<m:CACert>-----BEGIN CERTIFICATE-----
XYZ
-----END CERTIFICATE-----</m:CACert>
</m:CACertificate>
</m:CACertificates>
<m:ServerCertificate>Boo
</m:ServerCertificate>
</m:Fulfillment>
            """)

        certificate = Certificate.deserialize(xml_node)
        assert certificate.intermediates[0], IntermediateCertificate
        assert certificate.intermediates[1], IntermediateCertificate
        assert certificate.intermediates[2], IntermediateCertificate


class TestIntermediateCertificate(object):

    def test_deserialize(self):
        xml_node = etree.fromstring(
            b"""<?xml version="1.0" encoding="UTF-8"?>
<m:CACertificate xmlns:m="http://api.geotrust.com/webtrust/query">
<m:Type>INTERMEDIATE</m:Type>
<m:CACert>-----BEGIN CERTIFICATE-----
DEF
-----END CERTIFICATE-----</m:CACert>
</m:CACertificate>
            """)

        intermediate = IntermediateCertificate.deserialize(xml_node)
        assert intermediate.type == "INTERMEDIATE"
        assert intermediate.cert == """-----BEGIN CERTIFICATE-----
DEF
-----END CERTIFICATE-----
""".rstrip()


class TestModificationEvents(object):

    def test_deserialize(self):
        xml_node = etree.fromstring(
            b"""<?xml version="1.0" encoding="UTF-8"?>
<m:ModificationEvents xmlns:m="http://api.geotrust.com/webtrust/query">
<m:ModificationEvent>
<m:ModificationEventID>21612526</m:ModificationEventID>
<m:ModificationEventName>Order Created</m:ModificationEventName>
<m:ModificationTimestamp>2014-08-05T15:05:33+00:00</m:ModificationTimestamp>
</m:ModificationEvent>
<m:ModificationEvent>
<m:ModificationEventID>21612556</m:ModificationEventID>
<m:ModificationEventName>Approver Rejected</m:ModificationEventName>
<m:ModificationTimestamp>2014-08-05T15:05:33+00:00</m:ModificationTimestamp>
</m:ModificationEvent>
</m:ModificationEvents>
        """)

        modifications = ModificationEvents.deserialize(xml_node)
        assert len(modifications) == 2


class TestModificationEvent(object):

    def test_deserialize(self):
        xml_node = etree.fromstring(
            b"""<?xml version="1.0" encoding="UTF-8"?>
<m:ModificationEvent xmlns:m="http://api.geotrust.com/webtrust/query">
<m:ModificationEventID>21612526</m:ModificationEventID>
<m:ModificationEventName>Order Created</m:ModificationEventName>
<m:ModificationTimestamp>2014-08-05T15:05:33+00:00</m:ModificationTimestamp>
</m:ModificationEvent>
        """)

        event = ModificationEvent.deserialize(xml_node)
        assert event.event_name == "Order Created"
        assert event.time_stamp == "2014-08-05T15:05:33+00:00"
        assert event.mod_id == "21612526"


class TestOrderDetail(object):

    def test_deserialize_with_modification_events(self):
        xml_node = etree.fromstring(
            b"""<?xml version="1.0" encoding="UTF-8"?>
<m:OrderDetail xmlns:m="http://api.geotrust.com/webtrust/query">
<m:ModificationEvents>
<m:ModificationEvent>
<m:ModificationEventID>21612199</m:ModificationEventID>
<m:ModificationEventName>Order Created</m:ModificationEventName>
<m:ModificationTimestamp>2014-08-05T14:44:15+00:00</m:ModificationTimestamp>
</m:ModificationEvent>
</m:ModificationEvents>
<m:OrderInfo>
<m:PartnerOrderID>eUogDVDrbdeRelyIzDyblFgWCOeeFc</m:PartnerOrderID>
<m:GeoTrustOrderID>1825833</m:GeoTrustOrderID>
<m:DomainName>testingsymantecssl.com</m:DomainName>
<m:OrderDate>2014-08-05T14:44:15+00:00</m:OrderDate>
<m:Price>35.0</m:Price>
<m:Method>RESELLER</m:Method>
<m:OrderStatusMajor>PENDING</m:OrderStatusMajor>
<m:ValidityPeriod>15</m:ValidityPeriod>
<m:ServerCount>1</m:ServerCount>
<m:RenewalInd>Y</m:RenewalInd>
<m:ProductCode>QUICKSSLPREMIUM</m:ProductCode>
<m:OrderState>WF_DOMAIN_APPROVAL</m:OrderState>
</m:OrderInfo>
<m:QuickOrderDetail>
<m:OrderStatusMinor>
<m:OrderStatusMinorCode>ORDER_WAITING_FOR_APPROVAL</m:OrderStatusMinorCode>
<m:OrderStatusMinorName>Order Waiting For Approval</m:OrderStatusMinorName>
</m:OrderStatusMinor>
<m:OrganizationInfo>
<m:OrganizationName>MyOrg</m:OrganizationName>
<m:OrganizationAddress>
<m:City>San Antonio</m:City>
<m:Region>Texas</m:Region>
<m:Country>US</m:Country>
</m:OrganizationAddress>
</m:OrganizationInfo>
<m:ApproverNotifiedDate>2014-08-05T14:44:15+00:00</m:ApproverNotifiedDate>
<m:ApproverEmailAddress>admin@example.com</m:ApproverEmailAddress>
</m:QuickOrderDetail>
<m:OrderContacts>
<m:AdminContact>
<m:FirstName>John</m:FirstName>
<m:LastName>Doe</m:LastName>
<m:Phone>2103122400</m:Phone>
<m:Email>someone@email.com</m:Email>
<m:Title>Caesar</m:Title>
</m:AdminContact>
<m:TechContact>
<m:FirstName>John</m:FirstName>
<m:LastName>Doe</m:LastName>
<m:Phone>2103122400</m:Phone>
<m:Email>someone@email.com</m:Email>
<m:Title>Caesar</m:Title>
</m:TechContact>
<m:BillingContact>
<m:FirstName>John</m:FirstName>
<m:LastName>Doe</m:LastName>
<m:Phone>2103122400</m:Phone>
<m:Email>someone@email.com</m:Email>
<m:Title>Caesar</m:Title>
</m:BillingContact>
</m:OrderContacts>
<m:Fulfillment>
<m:CACertificates>
<m:CACertificate>
<m:Type>INTERMEDIATE</m:Type>
<m:CACert>
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
</m:CACert>
</m:CACertificate>
<m:CACertificate>
<m:Type>ROOT</m:Type>
<m:CACert>
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
</m:CACert>
</m:CACertificate>
</m:CACertificates>
<m:IconScript>
</m:IconScript>
</m:Fulfillment>
<m:AuthenticationComments />
<m:AuthenticationStatuses />
</m:OrderDetail>
            """)

        order_detail = OrderDetail.deserialize(xml_node)
        assert order_detail.status_code == "ORDER_WAITING_FOR_APPROVAL"
        assert order_detail.status_name == "Order Waiting For Approval"
        assert order_detail.approver_email == "admin@example.com"
        assert order_detail.organization_contacts, OrderContacts
        assert order_detail.organization_info, OrganizationInfo
        assert order_detail.modified_events, ModificationEvents

    def test_deserialize_with_vulnerabilities(self):
        xml_node = etree.fromstring(
            b"""<?xml version="1.0" encoding="UTF-8"?>
<m:OrderDetail xmlns:m="http://api.geotrust.com/webtrust/query">
<m:ModificationEvents>
<m:ModificationEvent>
<m:ModificationEventID>21612199</m:ModificationEventID>
<m:ModificationEventName>Order Created</m:ModificationEventName>
<m:ModificationTimestamp>2014-08-05T14:44:15+00:00</m:ModificationTimestamp>
</m:ModificationEvent>
</m:ModificationEvents>
<m:OrderInfo>
<m:PartnerOrderID>eUogDVDrbdeRelyIzDyblFgWCOeeFc</m:PartnerOrderID>
<m:GeoTrustOrderID>1825833</m:GeoTrustOrderID>
<m:DomainName>testingsymantecssl.com</m:DomainName>
<m:OrderDate>2014-08-05T14:44:15+00:00</m:OrderDate>
<m:Price>35.0</m:Price>
<m:Method>RESELLER</m:Method>
<m:OrderStatusMajor>PENDING</m:OrderStatusMajor>
<m:ValidityPeriod>15</m:ValidityPeriod>
<m:ServerCount>1</m:ServerCount>
<m:RenewalInd>Y</m:RenewalInd>
<m:ProductCode>QUICKSSLPREMIUM</m:ProductCode>
<m:OrderState>WF_DOMAIN_APPROVAL</m:OrderState>
</m:OrderInfo>
<m:Vulnerabilities>
<m:Vulnerability>
<m:Severity>1</m:Severity>
<m:NumberFound>1</m:NumberFound>
</m:Vulnerability>
</m:Vulnerabilities>
<m:QuickOrderDetail>
<m:OrderStatusMinor>
<m:OrderStatusMinorCode>ORDER_WAITING_FOR_APPROVAL</m:OrderStatusMinorCode>
<m:OrderStatusMinorName>Order Waiting For Approval</m:OrderStatusMinorName>
</m:OrderStatusMinor>
<m:OrganizationInfo>
<m:OrganizationName>MyOrg</m:OrganizationName>
<m:OrganizationAddress>
<m:City>San Antonio</m:City>
<m:Region>Texas</m:Region>
<m:Country>US</m:Country>
</m:OrganizationAddress>
</m:OrganizationInfo>
<m:ApproverNotifiedDate>2014-08-05T14:44:15+00:00</m:ApproverNotifiedDate>
<m:ApproverEmailAddress>admin@example.com</m:ApproverEmailAddress>
</m:QuickOrderDetail>
<m:OrderContacts>
<m:AdminContact>
<m:FirstName>John</m:FirstName>
<m:LastName>Doe</m:LastName>
<m:Phone>2103122400</m:Phone>
<m:Email>someone@email.com</m:Email>
<m:Title>Caesar</m:Title>
</m:AdminContact>
<m:TechContact>
<m:FirstName>John</m:FirstName>
<m:LastName>Doe</m:LastName>
<m:Phone>2103122400</m:Phone>
<m:Email>someone@email.com</m:Email>
<m:Title>Caesar</m:Title>
</m:TechContact>
<m:BillingContact>
<m:FirstName>John</m:FirstName>
<m:LastName>Doe</m:LastName>
<m:Phone>2103122400</m:Phone>
<m:Email>someone@email.com</m:Email>
<m:Title>Caesar</m:Title>
</m:BillingContact>
</m:OrderContacts>
<m:Fulfillment>
<m:CACertificates>
<m:CACertificate>
<m:Type>INTERMEDIATE</m:Type>
<m:CACert>
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
</m:CACert>
</m:CACertificate>
<m:CACertificate>
<m:Type>ROOT</m:Type>
<m:CACert>
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
</m:CACert>
</m:CACertificate>
</m:CACertificates>
<m:IconScript>
</m:IconScript>
</m:Fulfillment>
<m:AuthenticationComments />
<m:AuthenticationStatuses />
</m:OrderDetail>
            """)

        order_detail = OrderDetail.deserialize(xml_node)

        assert order_detail.vulnerabilities, Vulnerabilities

    def test_deserialize_without_modification_events(self):
        xml_node = etree.fromstring(
            b"""<?xml version="1.0" encoding="UTF-8"?>
<m:OrderDetail xmlns:m="http://api.geotrust.com/webtrust/query">
<m:OrderInfo>
<m:PartnerOrderID>eUogDVDrbdeRelyIzDyblFgWCOeeFc</m:PartnerOrderID>
<m:GeoTrustOrderID>1825833</m:GeoTrustOrderID>
<m:DomainName>testingsymantecssl.com</m:DomainName>
<m:OrderDate>2014-08-05T14:44:15+00:00</m:OrderDate>
<m:Price>35.0</m:Price>
<m:Method>RESELLER</m:Method>
<m:OrderStatusMajor>PENDING</m:OrderStatusMajor>
<m:ValidityPeriod>15</m:ValidityPeriod>
<m:ServerCount>1</m:ServerCount>
<m:RenewalInd>Y</m:RenewalInd>
<m:ProductCode>QUICKSSLPREMIUM</m:ProductCode>
<m:OrderState>WF_DOMAIN_APPROVAL</m:OrderState>
</m:OrderInfo>
<m:QuickOrderDetail>
<m:OrderStatusMinor>
<m:OrderStatusMinorCode>ORDER_WAITING_FOR_APPROVAL</m:OrderStatusMinorCode>
<m:OrderStatusMinorName>Order Waiting For Approval</m:OrderStatusMinorName>
</m:OrderStatusMinor>
<m:OrganizationInfo>
<m:OrganizationName>MyOrg</m:OrganizationName>
<m:OrganizationAddress>
<m:City>San Antonio</m:City>
<m:Region>Texas</m:Region>
<m:Country>US</m:Country>
</m:OrganizationAddress>
</m:OrganizationInfo>
<m:ApproverNotifiedDate>2014-08-05T14:44:15+00:00</m:ApproverNotifiedDate>
<m:ApproverEmailAddress>admin@example.com</m:ApproverEmailAddress>
</m:QuickOrderDetail>
<m:OrderContacts>
<m:AdminContact>
<m:FirstName>John</m:FirstName>
<m:LastName>Doe</m:LastName>
<m:Phone>2103122400</m:Phone>
<m:Email>someone@email.com</m:Email>
<m:Title>Caesar</m:Title>
</m:AdminContact>
<m:TechContact>
<m:FirstName>John</m:FirstName>
<m:LastName>Doe</m:LastName>
<m:Phone>2103122400</m:Phone>
<m:Email>someone@email.com</m:Email>
<m:Title>Caesar</m:Title>
</m:TechContact>
<m:BillingContact>
<m:FirstName>John</m:FirstName>
<m:LastName>Doe</m:LastName>
<m:Phone>2103122400</m:Phone>
<m:Email>someone@email.com</m:Email>
<m:Title>Caesar</m:Title>
</m:BillingContact>
</m:OrderContacts>
<m:Fulfillment>
<m:CACertificates>
<m:CACertificate>
<m:Type>INTERMEDIATE</m:Type>
<m:CACert>
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
</m:CACert>
</m:CACertificate>
<m:CACertificate>
<m:Type>ROOT</m:Type>
<m:CACert>
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
</m:CACert>
</m:CACertificate>
</m:CACertificates>
<m:IconScript>
</m:IconScript>
</m:Fulfillment>
<m:AuthenticationComments />
<m:AuthenticationStatuses />
</m:OrderDetail>
            """)

        order_detail = OrderDetail.deserialize(xml_node)
        assert order_detail.status_code == "ORDER_WAITING_FOR_APPROVAL"
        assert order_detail.status_name == "Order Waiting For Approval"
        assert order_detail.approver_email == "admin@example.com"
        assert order_detail.organization_contacts, OrderContacts
        assert order_detail.organization_info, OrganizationInfo


class TestOrderDetails(object):

    def test_deserialize(self):
        xml_node = etree.fromstring(
            b"""<?xml version="1.0" encoding="UTF-8"?>
<m:OrderDetails xmlns:m="http://api.geotrust.com/webtrust/query">
<m:OrderDetail>
<m:ModificationEvents>
<m:ModificationEvent>
<m:ModificationEventID>21612199</m:ModificationEventID>
<m:ModificationEventName>Order Created</m:ModificationEventName>
<m:ModificationTimestamp>2014-08-05T14:44:15+00:00</m:ModificationTimestamp>
</m:ModificationEvent>
</m:ModificationEvents>
<m:OrderInfo>
<m:PartnerOrderID>eUogDVDrbdeRelyIzDyblFgWCOeeFc</m:PartnerOrderID>
<m:GeoTrustOrderID>1825833</m:GeoTrustOrderID>
<m:DomainName>testingsymantecssl.com</m:DomainName>
<m:OrderDate>2014-08-05T14:44:15+00:00</m:OrderDate>
<m:Price>35.0</m:Price>
<m:Method>RESELLER</m:Method>
<m:OrderStatusMajor>PENDING</m:OrderStatusMajor>
<m:ValidityPeriod>15</m:ValidityPeriod>
<m:ServerCount>1</m:ServerCount>
<m:RenewalInd>Y</m:RenewalInd>
<m:ProductCode>QUICKSSLPREMIUM</m:ProductCode>
<m:OrderState>WF_DOMAIN_APPROVAL</m:OrderState>
</m:OrderInfo>
<m:QuickOrderDetail>
<m:OrderStatusMinor>
<m:OrderStatusMinorCode>ORDER_WAITING_FOR_APPROVAL</m:OrderStatusMinorCode>
<m:OrderStatusMinorName>Order Waiting For Approval</m:OrderStatusMinorName>
</m:OrderStatusMinor>
<m:OrganizationInfo>
<m:OrganizationName>MyOrg</m:OrganizationName>
<m:OrganizationAddress>
<m:City>San Antonio</m:City>
<m:Region>Texas</m:Region>
<m:Country>US</m:Country>
</m:OrganizationAddress>
</m:OrganizationInfo>
<m:ApproverNotifiedDate>2014-08-05T14:44:15+00:00</m:ApproverNotifiedDate>
<m:ApproverEmailAddress>admin@example.com</m:ApproverEmailAddress>
</m:QuickOrderDetail>
<m:OrderContacts>
<m:AdminContact>
<m:FirstName>John</m:FirstName>
<m:LastName>Doe</m:LastName>
<m:Phone>2103122400</m:Phone>
<m:Email>someone@email.com</m:Email>
<m:Title>Caesar</m:Title>
</m:AdminContact>
<m:TechContact>
<m:FirstName>John</m:FirstName>
<m:LastName>Doe</m:LastName>
<m:Phone>2103122400</m:Phone>
<m:Email>someone@email.com</m:Email>
<m:Title>Caesar</m:Title>
</m:TechContact>
<m:BillingContact>
<m:FirstName>John</m:FirstName>
<m:LastName>Doe</m:LastName>
<m:Phone>2103122400</m:Phone>
<m:Email>someone@email.com</m:Email>
<m:Title>Caesar</m:Title>
</m:BillingContact>
</m:OrderContacts>
<m:Fulfillment>
<m:CACertificates>
<m:CACertificate>
<m:Type>INTERMEDIATE</m:Type>
<m:CACert>
-----BEGIN CERTIFICATE----- -----END CERTIFICATE-----
</m:CACert>
</m:CACertificate>
<m:CACertificate>
<m:Type>ROOT</m:Type>
<m:CACert>
-----BEGIN CERTIFICATE----- -----END CERTIFICATE-----
</m:CACert>
</m:CACertificate>
</m:CACertificates>
<m:IconScript>
</m:IconScript>
</m:Fulfillment>
<m:AuthenticationComments />
<m:AuthenticationStatuses />
</m:OrderDetail>
</m:OrderDetails>
            """)

        order_details = OrderDetails.deserialize(xml_node)
        assert len(order_details) == 1


class TestGetElementText(object):

    def test_get_element_text_with_none_type(self):
        element = None
        text = utils.get_element_text(element)

        assert text == "None"


class TestQuickOrderResponse(object):

    def test_deserialize(self):
        xml_node = etree.fromstring(b"""<?xml version="1.0" encoding="UTF-8"?>
<m:QuickOrderResponse xmlns:m="http://api.geotrust.com/webtrust/order">
<m:QuickOrderResult>
<m:OrderResponseHeader>
<m:PartnerOrderID>04201988</m:PartnerOrderID>
<m:SuccessCode>0</m:SuccessCode>
<m:Timestamp>2015-01-29T20:42:05.447+00:00</m:Timestamp>
</m:OrderResponseHeader>
<m:GeoTrustOrderID>1912794</m:GeoTrustOrderID>
</m:QuickOrderResult>
</m:QuickOrderResponse>
        """)

        order_response = QuickOrderResponse.deserialize(xml_node)
        assert type(order_response) == QuickOrderResponse


class TestQuickOrderResult(object):

    def test_deserialize(self):
        xml_node = etree.fromstring(b"""<?xml version="1.0" encoding="UTF-8"?>
<m:QuickOrderResult xmlns:m="http://api.geotrust.com/webtrust/order">
<m:OrderResponseHeader>
<m:PartnerOrderID>04201988</m:PartnerOrderID>
<m:SuccessCode>0</m:SuccessCode>
<m:Timestamp>2015-01-29T20:42:05.447+00:00</m:Timestamp>
</m:OrderResponseHeader>
<m:GeoTrustOrderID>1912794</m:GeoTrustOrderID>
</m:QuickOrderResult>
        """)

        order_result = QuickOrderResult.deserialize(xml_node)

        assert order_result.order_id == '1912794'


class TestOrderResponseHeader(object):

    def test_deserialize(self):
        xml_node = etree.fromstring(b"""<?xml version="1.0" encoding="UTF-8"?>
<m:OrderResponseHeader xmlns:m="http://api.geotrust.com/webtrust/order">
<m:PartnerOrderID>04201988</m:PartnerOrderID>
<m:SuccessCode>0</m:SuccessCode>
<m:Timestamp>2015-01-29T20:42:05.447+00:00</m:Timestamp>
</m:OrderResponseHeader>
        """)

        response = OrderResponseHeader.deserialize(xml_node)
        assert response.success_code == '0'
        assert response.partner_order_id == '04201988'

import datetime

from lxml import etree

from symantecssl.models import (
    ContactInfo, Certificate, CertificateInfo, GetModifiedOrderRequest,
    IntermediateCertificate, ModificationEvent, ModificationEvents,
    OrderContacts, OrganizationInfo, OrderDetail, OrderDetails,
    OrderQueryOptions, QueryRequestHeader, RequestEnvelope, get_element_text
)


class TestOrganizationInfo(object):

    def test_deserialize(self):

        xml_node = etree.fromstring(
            """<?xml version="1.0" encoding="UTF-8"?>
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
            """<?xml version="1.0" encoding="UTF-8"?>
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
            """<?xml version="1.0" encoding="UTF-8"?>
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
            """<?xml version="1.0" encoding="UTF-8"?>
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
            """<?xml version="1.0" encoding="UTF-8"?>
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
            """<?xml version="1.0" encoding="UTF-8"?>
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
            """<?xml version="1.0" encoding="UTF-8"?>
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
            """<?xml version="1.0" encoding="UTF-8"?>
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
            """<?xml version="1.0" encoding="UTF-8"?>
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

    def test_deserialize_without_modification_events(self):
        xml_node = etree.fromstring(
            """<?xml version="1.0" encoding="UTF-8"?>
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
            """<?xml version="1.0" encoding="UTF-8"?>
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


# Request Tests Start Here
class TestRequestEnvelope(object):

    def test_serialize_modified_orders(self):

        re = RequestEnvelope(GetModifiedOrderRequest())

        root = re.serialize()
        mod_requests = root.findall('.//GetModifiedOrders')
        len_mod_request = len(root.find('.//Request'))

        assert len(mod_requests) == 1
        assert len_mod_request > 0


class TestQueryRequestHeader(object):

    def test_serialize_query_request_header(self):

        qrh = QueryRequestHeader()
        qrh.username = "Axton"
        qrh.password = "IHateCL4P-TP!"
        qrh.partner_code = "BL2"

        root = qrh.serialize()

        assert root.find('.//PartnerCode').text == "BL2"
        assert root.find('.//UserName').text == "Axton"
        assert root.find('.//Password').text == "IHateCL4P-TP!"
        assert len(root.findall('.//AuthToken')) == 1


class TestOrderQueryOptions(object):

    def test_serialize_query_options_default(self):

        oqo = OrderQueryOptions()
        root = oqo.serialize()

        assert root.find('.//ReturnProductDetail').text == "true"
        assert root.find('.//ReturnContacts').text == "true"
        assert root.find('.//ReturnPaymentInfo').text == "true"
        assert root.find('.//ReturnFulfillment').text == "true"
        assert root.find('.//ReturnCACerts').text == "true"
        assert root.find('.//ReturnPKCS7Cert').text == "true"
        assert root.find('.//ReturnPartnerTags').text == "true"
        assert root.find('.//ReturnAuthenticationComments').text == "true"
        assert root.find('.//ReturnAuthenticationStatuses').text == "true"
        assert root.find('.//ReturnFileAuthDVSummary').text == "true"
        assert root.find('.//ReturnTrustServicesSummary').text == "true"
        assert root.find('.//ReturnTrustServicesDetails').text == "true"
        assert root.find('.//ReturnVulnerabilityScanSummary').text == "true"
        assert root.find('.//ReturnCertificateAlgorithmInfo').text == "true"

    def test_serialize_query_options_set_false(self):

        oqo = OrderQueryOptions(
            product_detail=False, contacts=False, payment_info=False,
            cert_info=False, fulfillment=False, ca_certs=False,
            pkcs7_cert=False, partner_tags=False, auth_comments=False,
            auth_statuses=False, file_auth_dv_summary=False,
            trust_services_summary=False, trust_services_details=False,
            vulnerability_scan_summary=False,
            vulnerability_scan_details=False, cert_algorithm_info=False

        )
        root = oqo.serialize()

        assert root.find('.//ReturnProductDetail').text == "false"
        assert root.find('.//ReturnContacts').text == "false"
        assert root.find('.//ReturnPaymentInfo').text == "false"
        assert root.find('.//ReturnFulfillment').text == "false"
        assert root.find('.//ReturnCACerts').text == "false"
        assert root.find('.//ReturnPKCS7Cert').text == "false"
        assert root.find('.//ReturnPartnerTags').text == "false"
        assert root.find('.//ReturnAuthenticationComments').text == "false"
        assert root.find('.//ReturnAuthenticationStatuses').text == "false"
        assert root.find('.//ReturnFileAuthDVSummary').text == "false"
        assert root.find('.//ReturnTrustServicesSummary').text == "false"
        assert root.find('.//ReturnTrustServicesDetails').text == "false"
        assert root.find('.//ReturnVulnerabilityScanSummary').text == "false"
        assert root.find('.//ReturnCertificateAlgorithmInfo').text == "false"


class TestGetModifiedOrderRequest(object):

    def test_serialize_get_modified_orders_request(self):

        gmor = GetModifiedOrderRequest()
        gmor.from_date = "2012-09-18"
        gmor.to_date = "2015-01-08"
        root = gmor.serialize()

        assert root.find('.//FromDate').text == "2012-09-18"
        assert root.find('.//ToDate').text == "2015-01-08"
        assert len(root.findall('.//OrderQueryOptions')) == 1
        assert len(root.findall('.//QueryRequestHeader')) == 1

    def test_set_credentials(self):
        username = "Maya"
        password = "SirenHarmony"
        partner_code = "BL2"

        gmor = GetModifiedOrderRequest()
        gmor.set_credentials(partner_code, username, password)

        assert gmor.query_request_header.username == username
        assert gmor.query_request_header.password == password
        assert gmor.query_request_header.partner_code == partner_code

    def test_set_time_frame(self):
        from_date = datetime.date(2012, 9, 18)
        to_date = datetime.date(2015, 1, 8)

        gmor = GetModifiedOrderRequest()
        gmor.set_time_frame(from_date, to_date)

        assert gmor.from_date == "2012-09-18"
        assert gmor.to_date == "2015-01-08"

    def test_set_query_options(self):

        gmor = GetModifiedOrderRequest()
        query_options = {
            'product_detail': False,
            'contacts': False,
            'payment_info': False,
            'cert_info': False,
            'fulfillment': False,
            'ca_certs': False,
            'pkcs7_cert': False,
            'partner_tags': False,
            'auth_comments': False,
            'auth_statuses': False,
            'file_auth_dv_summary': False,
            'trust_services_summary': False,
            'trust_services_details': False,
            'vulnerability_scan_summary': False,
            'vulnerability_scan_details': False,
            'cert_algorithm_info': False
        }

        gmor.set_query_options(**query_options)

        assert not gmor.query_options.product_detail
        assert not gmor.query_options.contacts
        assert not gmor.query_options.payment_info
        assert not gmor.query_options.certificate_info
        assert not gmor.query_options.fulfillment
        assert not gmor.query_options.ca_certs
        assert not gmor.query_options.pkcs7_cert
        assert not gmor.query_options.partner_tags
        assert not gmor.query_options.authentication_comments
        assert not gmor.query_options.authentication_statuses
        assert not gmor.query_options.file_auth_dv_summary
        assert not gmor.query_options.trust_services_summary
        assert not gmor.query_options.trust_services_details
        assert not gmor.query_options.vulnerability_scan_summary
        assert not gmor.query_options.vulnerability_scan_details
        assert not gmor.query_options.certificate_algorithm_info


class TestGetElementText(object):

    def test_get_element_text_with_none_type(self):
        element = None
        text = get_element_text(element)

        assert text == "None"

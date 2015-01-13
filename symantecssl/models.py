from __future__ import absolute_import, division, print_function
from lxml import etree

# Global Dict to be moved out, will carry namespaces for parsing
NS = {
    'm': 'http://api.geotrust.com/webtrust/query'
}

SOAP_NS = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/'
}


def get_element_text(element):
    """Checks if element is NoneType.

    :param element: element to check for NoneType
    :return: text of element or "None" text
    """
    if element is not None:
        return element.text
    else:
        return "None"


class RequestEnvelope(object):

    def __init__(self, request_model):
        self.request_model = request_model

    def serialize(self):
        """Serializes the entire request via request model.

        :return: root element for request
        """

        root = etree.Element(
            "{http://schemas.xmlsoap.org/soap/envelope/}Envelope",
            nsmap=SOAP_NS
        )

        body = etree.SubElement(
            root, "{http://schemas.xmlsoap.org/soap/envelope/}Body",
            nsmap=SOAP_NS
        )
        request_model = self.request_model.serialize()
        body.append(request_model)

        return root


class QueryRequestHeader(object):

    def __init__(self):
        self.partner_code = ''
        self.username = ''
        self.password = ''

    def serialize(self):
        """Serializes the query request header.

        Each request model should call this in order to process the request.
        The request model will initiate serialization here.

        :return: root element for the request header
        """

        root = etree.Element("QueryRequestHeader")

        partner_code = etree.SubElement(root, "PartnerCode")
        partner_code.text = self.partner_code
        auth_token = etree.SubElement(root, "AuthToken")
        username = etree.SubElement(auth_token, "UserName")
        username.text = self.username
        password = etree.SubElement(auth_token, "Password")
        password.text = self.password

        return root


class OrderQueryOptions(object):

    def __init__(
            self, product_detail=True, contacts=True, payment_info=True,
            cert_info=True, fulfillment=True, ca_certs=True, pkcs7_cert=True,
            partner_tags=True, auth_comments=True, auth_statuses=True,
            file_auth_dv_summary=True, trust_services_summary=True,
            trust_services_details=True, vulnerability_scan_summary=True,
            vulnerability_scan_details=True, cert_algorithm_info=True
    ):
        self.product_detail = product_detail
        self.contacts = contacts
        self.payment_info = payment_info
        self.certificate_info = cert_info
        self.fulfillment = fulfillment
        self.ca_certs = ca_certs
        self.pkcs7_cert = pkcs7_cert
        self.partner_tags = partner_tags
        self.authentication_comments = auth_comments
        self.authentication_statuses = auth_statuses
        self.file_auth_dv_summary = file_auth_dv_summary
        self.trust_services_summary = trust_services_summary
        self.trust_services_details = trust_services_details
        self.vulnerability_scan_summary = vulnerability_scan_summary
        self.vulnerability_scan_details = vulnerability_scan_details
        self.certificate_algorithm_info = cert_algorithm_info

    def serialize(self):
        """Serializes and sets the query options for the request.

        The query options are by default set to true. All data is passed
        through to the user. The user is able to change the values to false
        if they wish.


        :return: root element for the query options
        """
        root = etree.Element("OrderQueryOptions")

        element_map = {
            "ReturnProductDetail": self.product_detail,
            "ReturnContacts": self.contacts,
            "ReturnPaymentInfo": self.payment_info,
            "ReturnFulfillment": self.fulfillment,
            "ReturnCACerts": self.ca_certs,
            "ReturnPKCS7Cert": self.pkcs7_cert,
            "ReturnPartnerTags": self.partner_tags,
            "ReturnAuthenticationComments": self.authentication_comments,
            "ReturnAuthenticationStatuses": self.authentication_statuses,
            "ReturnFileAuthDVSummary": self.file_auth_dv_summary,
            "ReturnTrustServicesSummary": self.trust_services_summary,
            "ReturnTrustServicesDetails": self.trust_services_details,
            "ReturnVulnerabilityScanSummary": self.vulnerability_scan_details,
            "ReturnCertificateAlgorithmInfo": self.certificate_algorithm_info
        }

        for key, val in element_map.items():
            ele = etree.SubElement(root, key)
            ele.text = str(val).lower()

        return root


class GetModifiedOrderRequest(object):

    def __init__(self):
        self.query_options = OrderQueryOptions()
        self.query_request_header = QueryRequestHeader()
        self.from_date = ""
        self.to_date = ""

    def serialize(self):
        """Serializes the modified orders request.

        The request model for the GetModifiedOrders call in the Symantec
        SOAP XML API. Serializes all related sections to this request model.

        This will serialize the following:
            Query Request Header
            Query Options


        :return: root element for the get modified order request
        """
        root = etree.Element(
            "GetModifiedOrders",
            nsmap={None: 'http://api.geotrust.com/webtrust/query'}
        )

        query_request_header = self.query_request_header.serialize()
        query_options = self.query_options.serialize()

        request = etree.SubElement(root, "Request")

        from_date_ele = etree.Element("FromDate")
        to_date_ele = etree.Element("ToDate")
        from_date_ele.text = self.from_date
        to_date_ele.text = self.to_date

        request.append(query_request_header)
        request.append(query_options)
        request.append(from_date_ele)
        request.append(to_date_ele)

        return root

    def set_credentials(self, partner_code, username, password):
        """Sets credentials for serialization.

        Sets credentials to allow user to make requests with Symantec SOAPXML
        API. These credentials are set with Symantec proper. Contact Symantec
        to determine your partner code and username.

        :param partner_code: partner code for Symantec SOAPXML API
        :param username: username for Symantec SOAPXML API
        :param password: password associated with user in Symantec SOAPXML API
        """
        self.query_request_header.partner_code = partner_code
        self.query_request_header.username = username
        self.query_request_header.password = password

    def set_time_frame(self, from_date, to_date):
        """Sets time range of request to Symantec.

        It is recommended that this time range be kept short if you are
        interested in a quick response; however, it will parse a longer time
        range just fine. Be wary that it may be a little slow.

        :param from_date: ISO8601 Datetime object
        :param to_date: ISO8601 Datetime object
        """
        self.from_date = from_date.isoformat()
        self.to_date = to_date.isoformat()

    def set_query_options(
        self, product_detail, contacts, payment_info,
        cert_info, fulfillment, ca_certs, pkcs7_cert,
        partner_tags, auth_comments, auth_statuses,
        file_auth_dv_summary, trust_services_summary,
        trust_services_details, vulnerability_scan_summary,
        vulnerability_scan_details, cert_algorithm_info
    ):
        """Sets query options for serialization.

        Allows the user to change the query options. All query options are
        set default to True. There should really be no reason to change these
        to False unless you are concerned about performance of a large time
        ranged call. Check the Symantec API documentation for specifics on
        each of these components.

        All parameter explanations assume they are set to True.

        :param product_detail: details of the certificate product
        :param contacts: contacts for certificate order
        :param payment_info: payment information for certificate order
        :param cert_info: detailed certificate information
        :param fulfillment: section for the actual certificate itself
        :param ca_certs: section for the intermediate and root certificates
        :param pkcs7_cert: section for the pkcs7 certificate itself
        :param partner_tags:
        :param auth_comments: comments regarding authentication for the
        certificate
        :param auth_statuses: status for authentication comments
        :param file_auth_dv_summary:
        :param trust_services_summary:
        :param trust_services_details:
        :param vulnerability_scan_summary: results of vulnerability scan
        :param vulnerability_scan_details: details of vulnerability scan
        :param cert_algorithm_info: certificate algorithm hash (SHA2
        defaulted for Symantec as of January 2015)
        """
        self.query_options.product_detail = product_detail
        self.query_options.contacts = contacts
        self.query_options.payment_info = payment_info
        self.query_options.certificate_info = cert_info
        self.query_options.fulfillment = fulfillment
        self.query_options.ca_certs = ca_certs
        self.query_options.pkcs7_cert = pkcs7_cert
        self.query_options.partner_tags = partner_tags
        self.query_options.authentication_comments = auth_comments
        self.query_options.authentication_statuses = auth_statuses
        self.query_options.file_auth_dv_summary = file_auth_dv_summary
        self.query_options.trust_services_summary = trust_services_summary
        self.query_options.trust_services_details = trust_services_details
        self.query_options.vulnerability_scan_summary = (
            vulnerability_scan_summary)
        self.query_options.vulnerability_scan_details = (
            vulnerability_scan_details)
        self.query_options.certificate_algorithm_info = cert_algorithm_info


# Response Models
class OrderDetails(list):

    def __init__(self, details_to_add=[]):
        self.extend(details_to_add)

    @classmethod
    def deserialize(cls, xml_node):
        """ Deserializes order details section in response.

        :param xml_node: XML node to be parsed. Expected to explicitly be
        Order Details XML node.
        :return: details in order detail section.
        """
        details = [OrderDetail.deserialize(node) for node in
                   xml_node.findall('.//m:OrderDetail', NS)]
        return OrderDetails(details)


class OrderDetail(object):

    def __init__(self):
        self.status_code = ''
        self.status_message = ''
        self.organization_info = OrganizationInfo()
        self.organization_contacts = OrderContacts()
        self.modified_events = ModificationEvents()
        self.approver_email = ''

    @classmethod
    def deserialize(cls, xml_node):
        """Deserializes the order detail section in response.

        :param xml_node: XML node to be parsed. Expected to explicitly be
        Order Detail XML node.
        :return: parsed order detail response.
        """
        od = OrderDetail()

        od.status_code = get_element_text(
            xml_node.find('.//m:OrderStatusMinorCode', NS)
        )
        od.status_name = get_element_text(
            xml_node.find('.//m:OrderStatusMinorName', NS)
        )
        od.approver_email = get_element_text(
            xml_node.find('.//m:ApproverEmailAddress', NS)
        )

        # Deserialize Child nodes
        org_info_node = xml_node.find('.//m:OrganizationInfo', NS)
        org_contacts_node = xml_node.find('.//m:OrderContacts', NS)
        od.organization_info = OrganizationInfo.deserialize(org_info_node)
        od.organization_contacts = OrderContacts.deserialize(org_contacts_node)

        if xml_node.find('.//m:ModificationEvents', NS) is not None:
            mod_events_node = xml_node.find('.//m:ModificationEvents', NS)
            od.modified_events = (
                ModificationEvents.deserialize(mod_events_node)
            )
        else:
            pass

        return od


class OrganizationInfo(object):

    def __init__(self):
        self.name = ''
        self.city = ''
        # Region is also state
        self.region = ''
        self.country = ''

    @classmethod
    def deserialize(cls, xml_node):
        """Deserializes the organization information section in response.

        :param xml_node: XML node to be parsed. Expected to explicitly be
        Organization Information XML node.
        :return: parsed organization information response.
        """
        org_info = OrganizationInfo()
        org_info.name = get_element_text(
            xml_node.find('.//m:OrganizationName', NS)
        )
        org_info.city = get_element_text(
            xml_node.find('.//m:City', NS)
        )
        org_info.region = get_element_text(
            xml_node.find('.//m:Region', NS)
        )
        org_info.country = get_element_text(
            xml_node.find('.//m:Country', NS)
        )

        return org_info


class OrderContacts(object):

    def __init__(self):
        self.admin = None
        self.tech = None
        self.billing = None

    @classmethod
    def deserialize(cls, xml_node):
        """Deserializes the order contacts section in response.

        :param xml_node: XML node to be parsed. Expected to explicitly be
        Order Contacts XML node.
        :return: parsed order contacts information response.
        """
        contacts = OrderContacts()
        admin_node = xml_node.find('.//m:AdminContact', NS)
        tech_node = xml_node.find('.//m:TechContact', NS)
        billing_node = xml_node.find('.//m:BillingContact', NS)

        contacts.admin = ContactInfo.deserialize(admin_node)
        contacts.tech = ContactInfo.deserialize(tech_node)
        contacts.billing = ContactInfo.deserialize(billing_node)

        return contacts


class ContactInfo(object):

    def __init__(self):
        self.first_name = ''
        self.last_name = ''
        self.phone = ''
        self.email = ''
        self.title = ''
        self.org_name = ''
        self.address_line_one = ''
        self.address_line_two = ''
        self.city = ''
        self.region = ''
        self.postal_code = ''
        self.country = ''
        self.fax = ''

    @classmethod
    def deserialize(cls, xml_node):
        """Deserializes the contact information section in response.

        :param xml_node: XML node to be parsed. Expected to explicitly be
        Contact Information XML node.
        :return: parsed contact information response.
        """
        contact = ContactInfo()
        contact.first_name = get_element_text(
            xml_node.find('.//m:FirstName', NS)
        )
        contact.last_name = get_element_text(
            xml_node.find('.//m:LastName', NS)
        )
        contact.phone = get_element_text(
            xml_node.find('.//m:Phone', NS)
        )
        contact.email = get_element_text(
            xml_node.find('.//m:Email', NS)
        )
        contact.title = get_element_text(
            xml_node.find('.//m:Title', NS)
        )

        return contact


class CertificateInfo(object):

    def __init__(self):
        self.common_name = ''
        self.status = ''
        self.hash_algorithm = ''
        self.encryption_algorithm = ''

    @classmethod
    def deserialize(cls, xml_node):
        """Deserializes the certificate information section in the response.

        :param xml_node: XML node to be parsed. Expected to explicitly be
        Certificate Information XML node.
        :return: parsed certificate information response.
        """
        cert_info = CertificateInfo()
        cert_info.common_name = get_element_text(
            xml_node.find('.//m:CommonName', NS)
        )
        cert_info.status = get_element_text(
            xml_node.find('.//m:CertificateStatus', NS)
        )
        cert_info.hash_algorithm = get_element_text(
            xml_node.find('.//m:SignatureHashAlgorithm', NS)
        )
        cert_info.encryption_algorithm = get_element_text(
            xml_node.find('.//m:SignatureEncryptionAlgorithm', NS)
        )

        return cert_info


class Certificate(object):

    def __init__(self):
        self.server_cert = ''
        self.intermediates = []

    @classmethod
    def deserialize(cls, xml_node):
        """Deserializes the certificate section in the response.

        :param xml_node:XML node to be parsed. Expected to explicitly be
        Certificates XML node.
        :return: parsed certificate response.
        """
        cert = Certificate()
        cert.server_cert = get_element_text(
            xml_node.find('.//m:ServerCertificate', NS)
        )
        ca_certs = xml_node.find('.//m:CACertificates', NS)

        for x in ca_certs:
            cert.intermediates.append(IntermediateCertificate.deserialize(x))

        return cert


class IntermediateCertificate(object):

    def __init__(self):
        self.type = ''
        self.cert = ''

    @classmethod
    def deserialize(cls, xml_node):
        """Deserializes the intermediate certificates section in the response.

        :param xml_node: XML node to be parsed. Expected to explicitly be
        Intermediate Certificate XML node.
        :return: parsed intermediate certificate response.
        """

        inter_info = IntermediateCertificate()
        inter_info.type = get_element_text(xml_node.find('.//m:Type', NS))
        inter_info.cert = get_element_text(xml_node.find('.//m:CACert', NS))

        return inter_info


class ModificationEvents(list):

    def __init__(self, details_to_add=[]):
        self.extend(details_to_add)

    @classmethod
    def deserialize(cls, xml_node):
        """Deserializes the modification events section in the response.

        This is the section which holds multiple modification events. It will
        loop through each node found within it and initialize deserialization.

        :param xml_node: XML node to be parsed. Expected to explicitly be
        Modification Events XML node.
        :return: parsed modification events
        response.
        """
        details = [ModificationEvent.deserialize(node) for node in
                   xml_node.findall('.//m:ModificationEvent', NS)]
        return ModificationEvents(details)


class ModificationEvent(object):
    def __init__(self):
        self.event_name = ''
        self.time_stamp = ''
        self.mod_id = ''

    @classmethod
    def deserialize(cls, xml_node):
        """ Deserializes the modification event section in the response.

        :param xml_node: XML node to be parsed. Expected to explicitly be
        Modification Event XML node.
        :return: parsed modification event response.
        """
        me = ModificationEvent()

        me.mod_id = get_element_text(
            xml_node.find('.//m:ModificationEventID', NS)
        )
        me.event_name = get_element_text(
            xml_node.find('.//m:ModificationEventName', NS)
        )
        me.time_stamp = get_element_text(
            xml_node.find('.//m:ModificationTimestamp', NS)
        )

        return me

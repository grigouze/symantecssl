from __future__ import absolute_import, division, print_function
from lxml import etree

from symantecssl.response_models import (
    OrderDetails, OrderContacts, QuickOrderResponse
)

# Global Dict to be moved out, will carry namespaces for parsing
NS = {
    'm': 'http://api.geotrust.com/webtrust/query'
}

ONS = {
    'm': 'http://api.geotrust.com/webtrust/order'
}

SOAP_NS = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/'
}


class ApproverEmail(object):

    def __init__(self):
        self.approver_email = ''

    def serialize(self):

        approver_email = etree.Element('ApproverEmail')
        approver_email.text = self.approver_email

        return approver_email

    def set_approver_email(self, approver_email):
        self.approver_email = approver_email


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


class RequestHeader(object):

    def __init__(self):
        self.partner_code = ''
        self.username = ''
        self.password = ''

    def serialize(self, order_type):
        """Serializes the request header.

        Each request model should call this in order to process the request.
        The request model will initiate serialization here.

        :order_type: a True or False value to create the proper XML header for
        the request.

        :return: root element for the request header
        """
        if order_type:
            root = etree.Element("OrderRequestHeader")
        else:
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


class OrganizationInfo(object):

    def __init__(self):
        self.org_name = ''
        self.org_address = ''
        self.address_line_one = ''
        self.address_line_two = ''
        self.city = ''
        self.region = ''
        self.postal_code = ''
        self.country = ''
        self.phone = ''

    def serialize(self):
        """Serializes the Organization Info for the request.

        :return: root element for the organization info
        """
        root = etree.Element('OrganizationInfo')

        org_name = etree.SubElement(root, 'OrganizationName')
        org_name.text = self.org_name

        org_address = etree.SubElement(root, 'OrganizationAddress')

        address_line_one = etree.Element('AddressLine1')
        address_line_one.text = self.address_line_one
        org_address.append(address_line_one)

        address_line_two = etree.Element('AddressLine2')
        address_line_two.text = self.address_line_two
        org_address.append(address_line_two)

        city = etree.Element('City')
        city.text = self.city
        org_address.append(city)

        region = etree.Element('Region')
        region.text = self.region
        org_address.append(region)

        postal_code = etree.Element('PostalCode')
        postal_code.text = self.postal_code
        org_address.append(postal_code)

        country = etree.Element('Country')
        country.text = self.country
        org_address.append(country)

        phone = etree.Element('Phone')
        phone.text = self.phone
        org_address.append(phone)

        return root


class OrderParameters(object):

    def __init__(self):
        self.csr = ''
        self.domain_name = ''
        self.order_partner_order_id = ''
        self.renewal_indicator = ''
        self.renewal_behavior = ''
        self.server_count = ''
        self.signature_hash_algorithm = ''
        self.special_instructions = ''
        self.valid_period = ''
        self.web_server_type = ''

    def serialize(self):
        """Serializes the Order Parameters section for thet request.

        note:: Symantec limits customers to 1, 12, 24, 36, and 48 month options
        :return: root element of OrderParameters
        """

        root = etree.Element('OrderParameters')

        #TODO(chellygel): Validate number of months for ValidityPeriod
        valid_period = etree.SubElement(root, 'ValidityPeriod')
        valid_period.text = self.valid_period
        server_count = etree.SubElement(root, 'ServerCount')
        server_count.text = self.server_count
        domain_name = etree.SubElement(root, 'DomainName')
        domain_name.text = self.domain_name
        order_partner_order_id = etree.SubElement(
            root, 'OriginalPartnerOrderID'
        )
        order_partner_order_id.text = self.order_partner_order_id
        csr = etree.SubElement(root, 'CSR')
        csr.text = self.csr
        web_server_type = etree.SubElement(root, 'WebServerType')
        web_server_type.text = self.web_server_type
        renewal_indicator = etree.SubElement(root, 'RenewalIndicator')
        renewal_indicator.text = self.renewal_indicator
        renewal_behavior = etree.SubElement(root, 'RenewalBehavior')
        renewal_behavior.text = self.renewal_behavior
        signature_hash_algorithm = etree.SubElement(
            root, 'SignatureHashAlgorithm'
        )
        signature_hash_algorithm.text = self.signature_hash_algorithm
        special_instructions = etree.SubElement(root, 'SpecialInstructions')
        special_instructions.text = self.special_instructions

        return root


class Request(object):

    def __init__(self):
        self.partner_code = ''
        self.username = ''
        self.password = ''
        self.from_date = ''
        self.to_date = ''
        self.request_header = RequestHeader()

    def set_credentials(self, partner_code, username, password):

        """Sets credentials for serialization.

        Sets credentials to allow user to make requests with Symantec SOAPXML
        API. These credentials are set with Symantec proper. Contact Symantec
        to determine your partner code and username.

        :param partner_code: partner code for Symantec SOAPXML API
        :param username: username for Symantec SOAPXML API
        :param password: password associated with user in Symantec SOAPXML API
        """

        self.request_header.partner_code = partner_code
        self.request_header.username = username
        self.request_header.password = password

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


class GetModifiedOrderRequest(Request):

    def __init__(self):
        super(GetModifiedOrderRequest, self).__init__()
        self.query_options = OrderQueryOptions()
        self.response_model = OrderDetails

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
            'GetModifiedOrders',
            nsmap={None: 'http://api.geotrust.com/webtrust/query'}
        )

        query_request_header = self.request_header.serialize(
            order_type=False
        )
        query_options = self.query_options.serialize()

        request = etree.SubElement(root, 'Request')

        from_date_ele = etree.Element('FromDate')
        to_date_ele = etree.Element('ToDate')
        from_date_ele.text = self.from_date
        to_date_ele.text = self.to_date

        request.append(query_request_header)
        request.append(query_options)
        request.append(from_date_ele)
        request.append(to_date_ele)

        return root

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


class QuickOrderRequest(Request):

    def __init__(self):
        super(QuickOrderRequest, self).__init__()
        self.order_parameters = OrderParameters()
        self.order_contacts = OrderContacts()
        self.approver_email = ApproverEmail()
        self.response_model = QuickOrderResponse

    def serialize(self):
        """Serializes the quick order request.

        :return: root element of the QuickOrderRequest section
        """

        root = etree.Element(
            'QuickOrder',
            nsmap={None: 'http://api.geotrust.com/webtrust/order'}
        )

        order_request_header = self.request_header.serialize(order_type=True)

        request = etree.SubElement(root, 'Request')
        order_parameters = self.order_parameters.serialize()
        admin_contact, tech_contact, billing_contact = (
            self.order_contacts.serialize()
        )
        approver_email = self.approver_email.serialize()

        request.append(order_request_header)
        request.append(order_parameters)
        request.append(admin_contact)
        request.append(tech_contact)
        request.append(billing_contact)
        request.append(approver_email)

        return root

    def set_order_parameters(
            self, csr, domain_name, partner_order_id, renewal_indicator,
            renewal_behavior, server_count, hash_algorithm,
            special_instructions, valid_period, web_server_type
        ):
        """Sets the parameters for the order request.

        :return:
        """

        self.order_parameters.csr = csr
        self.order_parameters.domain_name = domain_name
        self.order_parameters.order_partner_order_id = partner_order_id
        self.order_parameters.renewal_indicator = renewal_indicator
        self.order_parameters.renewal_behavior = renewal_behavior
        self.order_parameters.server_count = server_count
        self.order_parameters.signature_hash_algorithm = hash_algorithm
        self.order_parameters.special_instructions = special_instructions
        self.order_parameters.valid_period = valid_period
        self.order_parameters.web_server_type = web_server_type
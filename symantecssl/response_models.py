from __future__ import absolute_import, division, print_function

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

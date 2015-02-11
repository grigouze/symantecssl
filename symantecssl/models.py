from __future__ import absolute_import, division, print_function
from lxml import etree

from symantecssl import utils

NS = {
    'm': 'http://api.geotrust.com/webtrust/query'
}

ONS = {
    'm': 'http://api.geotrust.com/webtrust/order'
}


class OrderContacts(object):

    def __init__(self):
        self.admin = ContactInfo()
        self.tech = ContactInfo()
        self.billing = ContactInfo()
        self.approval_email = ''

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

    def serialize(self):
        """Serializes the order contacts section for request.

        :return: each of the contact elements
        """
        admin_ele = self.admin.serialize('AdminContact')
        tech_ele = self.tech.serialize('TechContact')
        billing_ele = self.billing.serialize('BillingContact')

        return admin_ele, tech_ele, billing_ele


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
        contact.first_name = utils.get_element_text(
            xml_node.find('.//m:FirstName', NS)
        )
        contact.last_name = utils.get_element_text(
            xml_node.find('.//m:LastName', NS)
        )
        contact.phone = utils.get_element_text(
            xml_node.find('.//m:Phone', NS)
        )
        contact.email = utils.get_element_text(
            xml_node.find('.//m:Email', NS)
        )
        contact.title = utils.get_element_text(
            xml_node.find('.//m:Title', NS)
        )

        return contact

    def serialize(self, element_name):
        """Serializes the contact information section in the request.

        :param element_name: contact element type. Limited to Admin, Tech, and
         Billing.
        :return: the contact element that is to be used for request.
        """

        ele = etree.Element(element_name)

        utils.create_subelement_with_text(ele, 'FirstName', self.first_name)
        utils.create_subelement_with_text(ele, 'LastName', self.last_name)
        utils.create_subelement_with_text(ele, 'Phone', self.phone)
        utils.create_subelement_with_text(ele, 'Email', self.email)
        utils.create_subelement_with_text(ele, 'Title', self.title)
        utils.create_subelement_with_text(
            ele, 'OrganizationName', self.org_name
        )
        utils.create_subelement_with_text(
            ele, 'AddressLine1', self.address_line_one
        )
        utils.create_subelement_with_text(
            ele, 'AddressLine2', self.address_line_two
        )
        utils.create_subelement_with_text(ele, 'City', self.city)
        utils.create_subelement_with_text(ele, 'Region', self.region)
        utils.create_subelement_with_text(ele, 'PostalCode', self.postal_code)
        utils.create_subelement_with_text(ele, 'Country', self.country)
        utils.create_subelement_with_text(ele, 'Fax', self.fax)

        return ele

    def set_contact_info(
            self, first_name, last_name, phone, email, title,
            org_name=None, address_one=None, address_two=None, city=None,
            region=None, postal_code=None, country=None, fax=None):
        """Sets information for Contact Info to be used in request.

        :param first_name:
        :param last_name:
        :param phone:
        :param email:
        :param title:
        :param org_name:
        :param address_one: line one of address for contact
        :param address_two: line two of address for contact
        :param city:
        :param region: region or state of contact
        :param postal_code:
        :param country:
        :param fax: do people still have fax numbers?
        """
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.title = title
        self.org_name = org_name
        self.address_line_one = address_one
        self.address_line_two = address_two
        self.city = city
        self.region = region
        self.postal_code = postal_code
        self.country = country
        self.fax = fax

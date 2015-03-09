from __future__ import absolute_import, division, print_function
import datetime

from symantecssl.models import ContactInfo
from symantecssl.request_models import (
    GetModifiedOrderRequest, GetOrderByPartnerOrderID, OrderQueryOptions,
    OrderChanges, QuickOrderRequest, RequestHeader, RequestEnvelope, Reissue,
    ReissueEmail
)


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

        qrh = RequestHeader()
        qrh.username = "Axton"
        qrh.password = "IHateCL4P-TP!"
        qrh.partner_code = "BL2"

        root = qrh.serialize(order_type=False)

        assert root.find('.//PartnerCode').text == "BL2"
        assert root.find('.//UserName').text == "Axton"
        assert root.find('.//Password').text == "IHateCL4P-TP!"
        assert len(root.findall('.//AuthToken')) == 1

    def test_set_request_header(self):

        qrh = RequestHeader()
        qrh.set_request_header('SSL123', '2364')

        root = qrh.serialize(order_type=True)

        assert root.find('.//ProductCode').text == "SSL123"
        assert root.find('.//PartnerOrderID').text == "2364"


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

        assert gmor.request_header.username == username
        assert gmor.request_header.password == password
        assert gmor.request_header.partner_code == partner_code

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


class TestQuickOrderRequest(object):

    def test_serialize_quick_order_request(self):

        qor = QuickOrderRequest()
        qor.approver_email.set_approver_email('salvadore@email.com')
        qor.set_order_parameters(
            csr='Fake CSR',
            domain_name='example.com',
            partner_order_id='09182012',
            renewal_indicator='false',
            renewal_behavior='Thing',
            hash_algorithm='SHA2-256',
            special_instructions='Go to Flamerock',
            valid_period='12',
            web_server_type='apacheopenssl',
            wildcard='true',
            dns_names='www.email.com, www.example.com'
        )
        root = qor.serialize()

        assert root.find('.//ApproverEmail').text == 'salvadore@email.com'
        assert root.find('.//CSR').text == 'Fake CSR'
        assert root.find('.//DomainName').text == 'example.com'
        assert root.find('.//OriginalPartnerOrderID').text == '09182012'
        assert root.find('.//RenewalIndicator').text == 'false'
        assert root.find('.//RenewalBehavior').text == 'Thing'
        assert root.find('.//SignatureHashAlgorithm').text == 'SHA2-256'
        assert root.find('.//SpecialInstructions').text == 'Go to Flamerock'
        assert root.find('.//ValidityPeriod').text == '12'
        assert root.find('.//WebServerType').text == 'apacheopenssl'
        assert root.find('.//WildCard').text == 'true'
        assert root.find('.//DNSNames').text == (
            'www.email.com, www.example.com'
        )


class TestContactInfo(object):

    def assert_contact(self, contact_type, instance):
        root = instance.serialize(contact_type)

        assert root.find('.//FirstName').text == 'Tiny'
        assert root.find('.//LastName').text == 'Tina'
        assert root.find('.//Phone').text == '210-555-5555'
        assert root.find('.//Email').text == 'tinytina@email.com'
        assert root.find('.//Title').text == 'Explosives Expert'
        assert root.find('.//OrganizationName').text == 'Crimson Raiders'
        assert root.find('.//AddressLine1').text == 'Dragon Keep'
        assert root.find('.//AddressLine2').text == 'Chambers'
        assert root.find('.//City').text == 'Flamerock'
        assert root.find('.//Region').text == 'Unassuming Docks'
        assert root.find('.//PostalCode').text == '131333'
        assert root.find('.//Country').text == 'Pandora'
        assert root.find('.//Fax').text == '210-555-5554'

    def test_serialize(self):

        ci = ContactInfo()
        ci.first_name = 'Tiny'
        ci.last_name = 'Tina'
        ci.phone = '210-555-5555'
        ci.email = 'tinytina@email.com'
        ci.title = 'Explosives Expert'
        ci.org_name = 'Crimson Raiders'
        ci.address_line_one = 'Dragon Keep'
        ci.address_line_two = 'Chambers'
        ci.city = "Flamerock"
        ci.region = 'Unassuming Docks'
        ci.postal_code = '131333'
        ci.country = 'Pandora'
        ci.fax = '210-555-5554'

        self.assert_contact('AdminContact', ci)

    def test_set_contact_info(self):

        ci = ContactInfo()
        ci.set_contact_info(
            first_name='Tiny',
            last_name='Tina',
            phone='210-555-5555',
            email='tinytina@email.com',
            title='Explosives Expert',
            org_name='Crimson Raiders',
            address_one='Dragon Keep',
            address_two='Chambers',
            city="Flamerock",
            region='Unassuming Docks',
            postal_code='131333',
            country='Pandora',
            fax='210-555-5554'
        )

        self.assert_contact('TechContact', ci)


class TestGetOrderByPartnerOrderID(object):

    def test_serialize(self):

        gopoid = GetOrderByPartnerOrderID()
        gopoid.partner_order_id = '1989'
        root = gopoid.serialize()

        assert root.find('.//PartnerOrderID').text == '1989'

    def test_set_partner_order_id(self):

        gopoid = GetOrderByPartnerOrderID()
        gopoid.set_partner_order_id('2464')
        root = gopoid.serialize()

        assert root.find('.//PartnerOrderID').text == '2464'


class TestReissue(object):

    def test_serialize(self):

        r = Reissue()
        r.order_parameters.order_partner_order_id = '1989'
        r.add_san('torgue.domain.com')
        r.delete_san('jack.domain.com')
        r.edit_san('box.domain.com', 'gear.domain.com')
        root = r.serialize()

        assert len(root.findall('.//ChangeType')) == 3
        assert root.find('.//OriginalPartnerOrderID').text == '1989'

    def test_serialize_without_changes(self):
        r = Reissue()
        r.order_parameters.csr = 'Scav'
        root = r.serialize()

        assert not root.findall('.//OrderChange')

    def test_add_san(self):

        r = Reissue()
        r.add_san('handsome.domain.com')

        assert r.order_changes.add[0] == 'handsome.domain.com'

    def test_delete_san(self):

        r = Reissue()
        r.delete_san('siren.domain.com')

        assert r.order_changes.delete[0] == 'siren.domain.com'

    def test_edit_san(self):

        r = Reissue()
        r.edit_san('soldier.domain.com', 'sniper.domain.com')

        assert r.order_changes.edit[0] == (
            'soldier.domain.com', 'sniper.domain.com'
        )


class TestOrderChanges(object):

    def test_serialize_with_add(self):
        oc = OrderChanges()
        oc.add = ['mechromancer.domain.com', 'assassin.domain.com']
        root = oc.serialize()

        add_types = root.findall('.//ChangeType')
        add_values = root.findall('.//NewValue')

        assert len(add_types) == 2
        assert len(add_values) == 2
        assert add_types[0].text == 'Add_SAN'
        assert add_values[0].text == 'mechromancer.domain.com'

    def test_serialize_with_delete(self):
        oc = OrderChanges()
        oc.delete = ['psycho.domain.com', 'gunzerker.domain.com']
        root = oc.serialize()

        delete_types = root.findall('.//ChangeType')
        delete_values = root.findall('.//OldValue')

        assert len(delete_types) == 2
        assert len(delete_values) == 2
        assert delete_types[0].text == 'Delete_SAN'
        assert delete_values[0].text == 'psycho.domain.com'

    def test_serialize_with_edit(self):
        oc = OrderChanges()
        oc.edit = [
            ('gladiator.domain.com', 'lawbringer.domain.com'),
            ('enforcer.domain.com', 'fragtrap.domain.com')
        ]
        root = oc.serialize()

        edit_types = root.findall('.//ChangeType')
        edit_old_values = root.findall('.//OldValue')
        edit_new_values = root.findall('.//NewValue')

        for item in [edit_types, edit_old_values, edit_new_values]:
            assert len(item) == 2

        assert edit_types[0].text == 'Edit_SAN'
        assert edit_old_values[0].text == 'gladiator.domain.com'
        assert edit_new_values[0].text == 'lawbringer.domain.com'
        assert edit_old_values[1].text == 'enforcer.domain.com'
        assert edit_new_values[1].text == 'fragtrap.domain.com'


class TestReissueEmail(object):

    def test_serialize(self):
        re = ReissueEmail()
        re.reissue_email = 'nisha@domain.com'
        root = re.serialize()

        assert root.text == 'nisha@domain.com'

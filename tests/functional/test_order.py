import datetime
import pytest
import random
import string
import textwrap
import time

from symantecssl.order import ModifyOperation
from symantecssl.order import ProductCode
from symantecssl.exceptions import SymantecError


def order_with_order_id(symantec, order_id):
    return symantec.order(
        partnercode=symantec.partner_code,
        productcode=ProductCode.QuickSSLPremium,
        partnerorderid=order_id,
        organizationname="MyOrg",
        addressline1="5000 Walzem",
        city="San Antonio",
        region="TX",
        postalcode="78218",
        country="US",
        organizationphone="2103124000",
        validityperiod="12",
        serverCount="1",
        webservertype="20",
        admincontactfirstname="John",
        admincontactlastname="Doe",
        admincontactphone="2103122400",
        admincontactemail="admincontact@example.com",
        admincontacttitle="Caesar",
        admincontactaddressline1="123 Road",
        admincontactcity="San Antonio",
        admincontactregion="TX",
        admincontactpostalcode="78218",
        admincontactcountry="US",
        techsameasadmin="True",
        billsameastech="True",
        approveremail="admin@example.com",
        csr=textwrap.dedent("""
            -----BEGIN CERTIFICATE REQUEST-----
            MIICwjCCAaoCAQAwWTELMAkGA1UEBhMCVVMxDjAMBgNVBAgTBVRleGFzMRQwEgYD
            VQQHEwtTYW4gQW50b25pbzEOMAwGA1UEChMFTXlPcmcxFDASBgNVBAMTC2V4YW1w
            bGUuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0rJys+HbQuOH
            1ONUSrA2N6VTjinRLbtwZ3ylR/Q7Xba+lfEtS1joGG/sySTdT/AxMHg72e4xBIw9
            8VOVhSanb8qzdLUXevA/BnxVVS6OqXVXsSXhcsCvE7A6lgsDqPOJcwIJlUpjSHgj
            hops4sIUO+oZFAB9cY+ET+E7AdayT2GcE+Zk4LuoY5UWqBegJ3DvK14uEdvg+ONm
            AfFdwY8DH/MXiQXP99ARP1/J7Jh6cDBjil0faEVJDRBO64HTgOCGdWU9Uou6ugov
            nKsN1JS4+vvCyuexzNZrAZgFX7mL4TCvVtCOmL1bBJ/g4AXNqHaBECjHKyN/auIQ
            F3iT4u/XjQIDAQABoCQwIgYJKoZIhvcNAQkOMRUwEzARBglghkgBhvhCAQEEBAMC
            BkAwDQYJKoZIhvcNAQEFBQADggEBAGz2cvYacjgFwLNO7Iy6ga5nvTNwHg8X+gGD
            HAyqzM7thxoAr8U2D285KK14tlfsWuG/J2NbgV8uItPPkPlb3W3w3IHLfzjRMSXg
            0n6v+u/13E3rg5A6Q1bKLHY/Tp7Nd3bPB3JzQ0DQEOaznvUKadAl1oc5EGCx7S9w
            5bwYdeFYaVfh6iUCAwu68rv6nluLbtqbGrqAStMeoH3UbfLIJX1woNxa4qImvJ3b
            +dlJH6W/Rsour4OY5VffllA4F43CV4Ob3t5fd9tnMTy2X8uCGZbngxAMrR//JyXb
            KCbp2ufNNMANWpF2SdZ4EvhjbFUQ07eOu5RyUUVseTEwMvbtPRA=
            -----END CERTIFICATE REQUEST-----
        """)
    )


def test_get_orders_by_date_range(symantec):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    orderids = []
    for _ in range(2):
        orderids.append("".join(random.choice(string.ascii_letters)
                        for _ in range(30)))

    for order_id in orderids:
        order_with_order_id(symantec, order_id)

    order_list = symantec.get_orders_by_date_range(
        fromdate=date,
        todate=date,
        partnercode=symantec.partner_code
    )

    assert len(order_list) > 1
    order_data = order_list.pop()
    assert order_data["PartnerOrderID"]
    assert order_data["OrderDate"]


def test_get_order_by_partner_order_id(symantec):
    order_id = "".join(random.choice(string.ascii_letters) for _ in range(30))

    order_with_order_id(symantec, order_id)

    order_data = symantec.get_order_by_partner_order_id(
        partnerorderid=order_id,
        partnercode=symantec.partner_code
    )

    assert order_data["OrderInfo"]["PartnerOrderID"] == order_id


def test_modify_order(symantec):
    order_id = "".join(random.choice(string.ascii_letters) for _ in range(30))

    order_with_order_id(symantec, order_id)

    symantec.modify_order(
        partnerorderid=order_id,
        partnercode=symantec.partner_code,
        productcode=ProductCode.QuickSSLPremium,
        modifyorderoperation=ModifyOperation.Cancel,
    )

    order_data = symantec.get_order_by_partner_order_id(
        partnerorderid=order_id,
        partnercode=symantec.partner_code,
    )

    assert order_data["OrderInfo"]["OrderStatusMajor"] == "CANCELLED"


def test_get_modified_orders(symantec):
    now = datetime.datetime.now()
    date1 = now.strftime("%Y-%m-%d")
    date2 = (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    orderids = []
    for _ in range(2):
        orderids.append("".join(random.choice(string.ascii_letters)
                        for _ in range(30)))

    for order_id in orderids:
        order_with_order_id(symantec, order_id)

    for order_id in orderids:
        symantec.modify_order(
            partnerorderid=order_id,
            partnercode=symantec.partner_code,
            productcode=ProductCode.QuickSSLPremium,
            modifyorderoperation=ModifyOperation.Cancel,
        )

    order_list = symantec.get_modified_orders(
        fromdate=date1,
        todate=date2,
        partnercode=symantec.partner_code
    )

    assert len(order_list) > 1
    order_data = order_list.pop()
    assert order_data["OrderInfo"]["PartnerOrderID"]
    assert order_data["ModificationEvents"].pop()


def test_get_quick_approver_list(symantec):
    approver_list = symantec.get_quick_approver_list(
        partnercode=symantec.partner_code,
        domain="testingsymantecssl.com"
    )

    assert len(approver_list) > 0
    for approver in approver_list:
        assert set(approver.keys()) == set(["ApproverType", "ApproverEmail"])


def test_change_approver_email(symantec):
    order_id = "".join(random.choice(string.ascii_letters) for _ in range(30))
    order_with_order_id(symantec, order_id)
    symantec.change_approver_email(
        partnercode=symantec.partner_code,
        partnerorderid=order_id,
        approveremail="administrator@example.com"
    )

    new_email = symantec.get_order_by_partner_order_id(
        partnerorderid=order_id,
        partnercode=symantec.partner_code,
        returnproductdetail=True
    )["QuickOrderDetail"]["ApproverEmailAddress"]

    assert new_email == "administrator@example.com"


@pytest.fixture
def order_kwargs():
    order_id = "".join(random.choice(string.ascii_letters) for _ in range(30))
    return {
        "partnerorderid": order_id,
        "productcode": ProductCode.QuickSSLPremium,
        "organizationname": "MyOrg",
        "addressline1": "5000 Walzem",
        "city": "San Antonio",
        "region": "TX",
        "postalcode": "78218",
        "country": "US",
        "organizationphone": "2103124000",
        "validityperiod": "12",
        "serverCount": "1",
        "webservertype": "20",
        "admincontactfirstname": "John",
        "admincontactlastname": "Doe",
        "admincontactphone": "2103122400",
        "admincontactemail": "admincontact@example.com",
        "admincontacttitle": "Caesar",
        "admincontactaddressline1": "123 Road",
        "admincontactcity": "San Antonio",
        "admincontactregion": "TX",
        "admincontactpostalcode": "78218",
        "admincontactcountry": "US",
        "techsameasadmin": "True",
        "billsameastech": "True",
        "approveremail": "administrator@example.com",
        "csr": textwrap.dedent("""
            -----BEGIN CERTIFICATE REQUEST-----
            MIICwjCCAaoCAQAwWTELMAkGA1UEBhMCVVMxDjAMBgNVBAgTBVRleGFzMRQwEgYD
            VQQHEwtTYW4gQW50b25pbzEOMAwGA1UEChMFTXlPcmcxFDASBgNVBAMTC2V4YW1w
            bGUuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0rJys+HbQuOH
            1ONUSrA2N6VTjinRLbtwZ3ylR/Q7Xba+lfEtS1joGG/sySTdT/AxMHg72e4xBIw9
            8VOVhSanb8qzdLUXevA/BnxVVS6OqXVXsSXhcsCvE7A6lgsDqPOJcwIJlUpjSHgj
            hops4sIUO+oZFAB9cY+ET+E7AdayT2GcE+Zk4LuoY5UWqBegJ3DvK14uEdvg+ONm
            AfFdwY8DH/MXiQXP99ARP1/J7Jh6cDBjil0faEVJDRBO64HTgOCGdWU9Uou6ugov
            nKsN1JS4+vvCyuexzNZrAZgFX7mL4TCvVtCOmL1bBJ/g4AXNqHaBECjHKyN/auIQ
            F3iT4u/XjQIDAQABoCQwIgYJKoZIhvcNAQkOMRUwEzARBglghkgBhvhCAQEEBAMC
            BkAwDQYJKoZIhvcNAQEFBQADggEBAGz2cvYacjgFwLNO7Iy6ga5nvTNwHg8X+gGD
            HAyqzM7thxoAr8U2D285KK14tlfsWuG/J2NbgV8uItPPkPlb3W3w3IHLfzjRMSXg
            0n6v+u/13E3rg5A6Q1bKLHY/Tp7Nd3bPB3JzQ0DQEOaznvUKadAl1oc5EGCx7S9w
            5bwYdeFYaVfh6iUCAwu68rv6nluLbtqbGrqAStMeoH3UbfLIJX1woNxa4qImvJ3b
            +dlJH6W/Rsour4OY5VffllA4F43CV4Ob3t5fd9tnMTy2X8uCGZbngxAMrR//JyXb
            KCbp2ufNNMANWpF2SdZ4EvhjbFUQ07eOu5RyUUVseTEwMvbtPRA=
            -----END CERTIFICATE REQUEST-----
        """),
    }


def test_order(symantec, order_kwargs):
    order_kwargs["partnercode"] = symantec.partner_code
    order_id = order_kwargs["partnerorderid"]

    order_data = symantec.order(**order_kwargs)

    assert set(order_data.keys()) == set(["GeoTrustOrderID", "PartnerOrderID"])
    assert order_data["PartnerOrderID"] == order_id


def test_validate_order_parameters_success(symantec, order_kwargs):
    order_kwargs["partnercode"] = symantec.partner_code

    response = symantec.validate_order_parameters(**order_kwargs)

    expected_keys = set(["ValidityPeriod", "Price", "ParsedCSR", "RenewalInfo",
                         "CertificateSignatureHashAlgorithm"])
    assert set(response.keys()) == set(expected_keys)


def test_validate_order_parameters_error(symantec, order_kwargs):
    order_kwargs["partnercode"] = symantec.partner_code
    order_kwargs["webservertype"] = "9999"

    with pytest.raises(SymantecError) as e:
        symantec.validate_order_parameters(**order_kwargs)

    assert str(e).endswith("The Symantec API call ValidateOrderParameters"
                           " returned an error: 'Missing or Invalid Field:"
                           "  WebServerType'")


def test_reissue(symantec, order_kwargs):
    one_minute = 60

    order_kwargs["partnercode"] = symantec.partner_code
    product_code = order_kwargs["productcode"]
    order_id = order_kwargs['partnerorderid']

    def query_order():
        return symantec.get_order_by_partner_order_id(
            partnercode=symantec.partner_code,
            productcode=product_code,
            partnerorderid=order_id,
            returncertificateinfo="true",
        )

    def modify_order(operation):
        return symantec.modify_order(
            partnercode=symantec.partner_code,
            productcode=product_code,
            partnerorderid=order_id,
            modifyorderoperation=operation,
        )

    def ensure_order_completed():
        query_resp = query_order()
        order_status = query_resp["OrderInfo"]["OrderStatusMajor"].lower()
        if order_status == 'complete':
            return

        # Force approval of the order. The approval initially fails with a
        # 'SECURITY REVIEW FAILED'. Per the API docs, do a push_order_state
        # to force the order to COMPLETED state.
        #
        # For SSL123, this takes up to 15 minutes or so.
        # For QuickSSLPremium and RapidSSL, this happens immediately.
        try:
            modify_order(ModifyOperation.Approve)
        except SymantecError:
            modify_order(ModifyOperation.PushState)

        # wait until the order is finished; timeout after five minutes
        start = time.time()
        while True:
            query_resp = query_order()
            order_status = query_resp["OrderInfo"]["OrderStatusMajor"].lower()
            if order_status == 'complete':
                break
            elif time.time() - start > 5 * one_minute:
                raise Exception("Order approval timed out")
            time.sleep(10)

    symantec.order(**order_kwargs)
    ensure_order_completed()
    reissue_resp = symantec.reissue(
        partnercode=symantec.partner_code,
        productcode=product_code,
        partnerorderid=order_id,
        reissueemail=order_kwargs["admincontactemail"],
        csr=order_kwargs['csr'],
    )

    assert set(reissue_resp.keys()) == set(['GeoTrustOrderID',
                                            'PartnerOrderID'])
    assert reissue_resp['PartnerOrderID'] == order_id

    query_resp = query_order()
    cert_status = query_resp['CertificateInfo']['CertificateStatus']
    assert cert_status == 'PENDING_REISSUE'

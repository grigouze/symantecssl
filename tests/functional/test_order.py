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
        productcode=ProductCode.SSL123,
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
        admincontactemail="someone@email.com",
        admincontacttitle="Caesar",
        admincontactaddressline1="123 Road",
        admincontactcity="San Antonio",
        admincontactregion="TX",
        admincontactpostalcode="78218",
        admincontactcountry="US",
        techsameasadmin="True",
        billsameastech="True",
        approveremail="admin@testingsymantecssl.com",
        csr=textwrap.dedent("""
            -----BEGIN CERTIFICATE REQUEST-----
            MIICpjCCAY4CAQAwYTELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAlRYMRQwEgYDVQQH
            DAtTYW4gQW50b25pbzEOMAwGA1UECgwFTXlPcmcxHzAdBgNVBAMMFnRlc3Rpbmdz
            eW1hbnRlY3NzbC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDf
            klapgfE7MDlB++19m/I8TlzGJcIoiFUhqJN2TdCoiTPA+5eHkRRY9WWIS3R4xxQG
            fA52dxynLRtce1Sr4zxeP5HkxtWKWbIdir2YVqnjWSoqyf0+8VNX4cYhCRu3BETu
            Dfej5xjt7EH7++BoA5kGzcwv+7jb9U73XRREuZEq0l26QTd7EZjGZYATHJvz2idv
            Z784+iGrO0Qw76rYHCnhffWDld9lgMKXcgRJpESIDQHRsPMJSREyWAOr0Fov/z75
            YU3n4vXIFZSeSa7fGbyLFFXMNJpu4xG6x8JufgJkGZlgCEiX8aG6YjqV2Z3LrYld
            4jzT408Uqyw2GftzZMDZAgMBAAGgADANBgkqhkiG9w0BAQUFAAOCAQEAPxIjS7g/
            MUfNsRYuplgHh9BbZl13SVdFXc9POSJwSCy1pQhEhM+e7izGD3po+V0TlZ5DZohT
            djrGMEZvBm4OkwB7g/9hzEI5kyHfBXzBVn9ybcIzEMlRqAWc0tS1Kn+EyyDlbGnh
            iFEk178Q0KTuOIZfPVBKZjji0o5gj13wrRBAxJARf/0/MRqpg3mL932QgjmSB2dL
            /57yk0hXh1ChA8d2htKdwb3RnRJHOjVxWbWjYGcuAMz7RTEN9pWviTM3y7FfTWTP
            Q24Nrp12Ez1cALXb5t/lZkbrCtizCjUuEpREzIRMUYnWZEa7pw/CGbSTYH4a2x7n
            L5mReDt1ijwjGg==
            -----END CERTIFICATE REQUEST-----
        """)
    )


def test_order(symantec):
    order_id = "".join(random.choice(string.ascii_letters) for _ in range(30))

    order_data = order_with_order_id(symantec, order_id)

    assert set(order_data.keys()) == set(["GeoTrustOrderID", "PartnerOrderID"])
    assert order_data["PartnerOrderID"] == order_id


@pytest.fixture
def order_kwargs():
    order_id = "".join(random.choice(string.ascii_letters) for _ in range(30))
    return {
        "partnerorderid": order_id,
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
        "admincontactemail": "someone@email.com",
        "admincontacttitle": "Caesar",
        "admincontactaddressline1": "123 Road",
        "admincontactcity": "San Antonio",
        "admincontactregion": "TX",
        "admincontactpostalcode": "78218",
        "admincontactcountry": "US",
        "techsameasadmin": "True",
        "billsameastech": "True",
        "approveremail": "admin@testingsymantecssl.com",
        "csr": textwrap.dedent("""
            -----BEGIN CERTIFICATE REQUEST-----
            MIICpjCCAY4CAQAwYTELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAlRYMRQwEgYDVQQH
            DAtTYW4gQW50b25pbzEOMAwGA1UECgwFTXlPcmcxHzAdBgNVBAMMFnRlc3Rpbmdz
            eW1hbnRlY3NzbC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDf
            klapgfE7MDlB++19m/I8TlzGJcIoiFUhqJN2TdCoiTPA+5eHkRRY9WWIS3R4xxQG
            fA52dxynLRtce1Sr4zxeP5HkxtWKWbIdir2YVqnjWSoqyf0+8VNX4cYhCRu3BETu
            Dfej5xjt7EH7++BoA5kGzcwv+7jb9U73XRREuZEq0l26QTd7EZjGZYATHJvz2idv
            Z784+iGrO0Qw76rYHCnhffWDld9lgMKXcgRJpESIDQHRsPMJSREyWAOr0Fov/z75
            YU3n4vXIFZSeSa7fGbyLFFXMNJpu4xG6x8JufgJkGZlgCEiX8aG6YjqV2Z3LrYld
            4jzT408Uqyw2GftzZMDZAgMBAAGgADANBgkqhkiG9w0BAQUFAAOCAQEAPxIjS7g/
            MUfNsRYuplgHh9BbZl13SVdFXc9POSJwSCy1pQhEhM+e7izGD3po+V0TlZ5DZohT
            djrGMEZvBm4OkwB7g/9hzEI5kyHfBXzBVn9ybcIzEMlRqAWc0tS1Kn+EyyDlbGnh
            iFEk178Q0KTuOIZfPVBKZjji0o5gj13wrRBAxJARf/0/MRqpg3mL932QgjmSB2dL
            /57yk0hXh1ChA8d2htKdwb3RnRJHOjVxWbWjYGcuAMz7RTEN9pWviTM3y7FfTWTP
            Q24Nrp12Ez1cALXb5t/lZkbrCtizCjUuEpREzIRMUYnWZEa7pw/CGbSTYH4a2x7n
            L5mReDt1ijwjGg==
            -----END CERTIFICATE REQUEST-----
        """),
    }


def test_validate_order_parameters_success(symantec, order_kwargs):
    order_kwargs["partnercode"] = symantec.partner_code
    order_kwargs["productcode"] = ProductCode.SSL123

    response = symantec.validate_order_parameters(**order_kwargs)

    expected_keys = set(["ValidityPeriod", "Price", "ParsedCSR", "RenewalInfo",
                         "CertificateSignatureHashAlgorithm"])
    assert set(response.keys()) == set(expected_keys)


def test_validate_order_parameters_error(symantec, order_kwargs):
    order_kwargs["partnercode"] = symantec.partner_code
    order_kwargs["productcode"] = ProductCode.SSL123
    order_kwargs["webservertype"] = "9999"

    with pytest.raises(SymantecError) as e:
        symantec.validate_order_parameters(**order_kwargs)

    assert str(e).endswith("The Symantec API call ValidateOrderParameters"
                           " returned an error: 'Missing or Invalid Field:"
                           "  WebServerType'")


def test_reissue(symantec, order_kwargs):
    one_minute = 60

    order_kwargs["partnercode"] = symantec.partner_code
    order_kwargs["productcode"] = product_code = ProductCode.SSL123
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
        # For QuickSSLPremium, this happens immediately but sends an email.
        try:
            modify_order(ModifyOperation.Approve)
        except SymantecError:
            modify_order(ModifyOperation.PushState)

        # wait until the order is finished; timeout after thirty minutes
        start = time.time()
        while True:
            query_resp = query_order()
            order_status = query_resp["OrderInfo"]["OrderStatusMajor"].lower()
            if order_status == 'complete':
                break
            elif time.time() - start > 30 * one_minute:
                raise Exception("Order approval timed out")
            time.sleep(one_minute)

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

import datetime
import pytest
import random
import string
import subprocess
import time

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

from symantecssl.order import ModifyOperation
from symantecssl.order import ProductCode
from symantecssl.exceptions import SymantecError

try:
    from subprocess import check_output
except ImportError:
    def check_output(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError(
                'stdout argument not allowed, it will be overridden.'
            )
        process = subprocess.Popen(
            stdout=subprocess.PIPE,
            *popenargs,
            **kwargs
        )
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd, output=output)
        return output


def create_csr():
    return b"".join(
        check_output([
            "openssl", "req", "-new", "-newkey", "rsa:2048", "-nodes",
            "-keyout", "/dev/null", "-text", "-batch", "-subj",
            "/C=US/ST=Texas/L=San Antonio/O=MyOrg/CN=example.com",
        ]).partition(b"-----BEGIN CERTIFICATE REQUEST-----")[1:]
    ).decode("ascii")


def order_with_order_id(symantec, order_id, csr):
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
        csr=csr,
    )


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
        "csr": create_csr(),
    }


def test_get_orders_by_date_range(symantec, vcr):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    orderids = []
    csrs = []
    for _ in range(2):
        orderids.append("".join(random.choice(string.ascii_letters)
                        for _ in range(30)))
        csrs.append(create_csr())

    with vcr.use_cassette(
        placeholders=(
            [{"placeholder": "<<CSR{0}>>".format(i), "replace": csr}
             for i, csr in enumerate(csrs)]
            +
            [{"placeholder": "<<CSR{0}_QUOTED>>".format(i),
              "replace": quote_plus(csr)}
             for i, csr in enumerate(csrs)]
            +
            [{"placeholder": "<<OrderID{0}>>".format(i), "replace": oid}
             for i, oid in enumerate(orderids)])):
        for order_id, csr in zip(orderids, csrs):
            order_with_order_id(symantec, order_id, csr)

        order_list = symantec.get_orders_by_date_range(
            fromdate=date,
            todate=date,
            partnercode=symantec.partner_code
        )

    assert len(order_list) > 1
    order_data = order_list.pop()
    assert order_data["PartnerOrderID"]
    assert order_data["OrderDate"]


def test_get_order_by_partner_order_id(symantec, vcr):
    order_id = "".join(random.choice(string.ascii_letters) for _ in range(30))
    csr = create_csr()

    with vcr.use_cassette(
        placeholders=(
            [
                {"placeholder": "<<CSR>>", "replace": csr},
                {"placeholder": "<<CSR_QUOTED>>", "replace": quote_plus(csr)},
                {"placeholder": "<<OrderID>>", "replace": order_id},
            ])):
        order_with_order_id(symantec, order_id, csr)

        order_data = symantec.get_order_by_partner_order_id(
            partnerorderid=order_id,
            partnercode=symantec.partner_code
        )

    assert order_data["OrderInfo"]["PartnerOrderID"] == order_id


def test_modify_order(symantec, vcr):
    order_id = "".join(random.choice(string.ascii_letters) for _ in range(30))
    csr = create_csr()

    with vcr.use_cassette(
        placeholders=(
            [
                {"placeholder": "<<CSR>>", "replace": csr},
                {"placeholder": "<<CSR_QUOTED>>", "replace": quote_plus(csr)},
                {"placeholder": "<<OrderID>>", "replace": order_id},
            ])):
        order_with_order_id(symantec, order_id, csr)

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


def test_get_modified_orders(symantec, vcr):
    now = datetime.datetime.now()
    date1 = now.strftime("%Y-%m-%d")
    date2 = (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    orderids = []
    csrs = []
    for _ in range(2):
        orderids.append("".join(random.choice(string.ascii_letters)
                        for _ in range(30)))
        csrs.append(create_csr())

    with vcr.use_cassette(
        placeholders=(
            [{"placeholder": "<<CSR{0}>>".format(i), "replace": csr}
             for i, csr in enumerate(csrs)]
            +
            [{"placeholder": "<<CSR{0}_QUOTED>>".format(i),
              "replace": quote_plus(csr)}
             for i, csr in enumerate(csrs)]
            +
            [{"placeholder": "<<OrderID{0}>>".format(i), "replace": oid}
             for i, oid in enumerate(orderids)])):
        for order_id, csr in zip(orderids, csrs):
            order_with_order_id(symantec, order_id, csr)

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


def test_get_quick_approver_list(symantec, vcr):
    with vcr.use_cassette():
        approver_list = symantec.get_quick_approver_list(
            partnercode=symantec.partner_code,
            domain="testingsymantecssl.com"
        )

    assert len(approver_list) > 0
    for approver in approver_list:
        assert set(approver.keys()) == set(["ApproverType", "ApproverEmail"])


def test_change_approver_email(symantec, vcr):
    order_id = "".join(random.choice(string.ascii_letters) for _ in range(30))
    csr = create_csr()

    with vcr.use_cassette(
        placeholders=(
            [
                {"placeholder": "<<CSR>>", "replace": csr},
                {"placeholder": "<<CSR_QUOTED>>", "replace": quote_plus(csr)},
                {"placeholder": "<<OrderID>>", "replace": order_id},
            ])):
        order_with_order_id(symantec, order_id, csr)
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


def test_order_call(symantec, order_kwargs, vcr):
    order_kwargs["partnercode"] = symantec.partner_code
    order_id = order_kwargs["partnerorderid"]
    csr = order_kwargs["csr"]

    with vcr.use_cassette(
        placeholders=(
            [
                {"placeholder": "<<CSR>>", "replace": csr},
                {"placeholder": "<<CSR_QUOTED>>", "replace": quote_plus(csr)},
                {"placeholder": "<<OrderID>>", "replace": order_id},
            ])):
        order_data = symantec.order(**order_kwargs)

    assert set(order_data.keys()) == set(["GeoTrustOrderID", "PartnerOrderID"])
    assert order_data["PartnerOrderID"] == order_id


def test_validate_order_parameters_success(
        symantec, order_kwargs, vcr):
    order_kwargs["partnercode"] = symantec.partner_code
    order_id = order_kwargs["partnerorderid"]
    csr = order_kwargs["csr"]

    with vcr.use_cassette(
        placeholders=(
            [
                {"placeholder": "<<CSR>>", "replace": csr},
                {"placeholder": "<<CSR_QUOTED>>", "replace": quote_plus(csr)},
                {"placeholder": "<<OrderID>>", "replace": order_id},
            ])):
        response = symantec.validate_order_parameters(**order_kwargs)

    expected_keys = set(["ValidityPeriod", "Price", "ParsedCSR", "RenewalInfo",
                         "CertificateSignatureHashAlgorithm"])
    assert set(response.keys()) == set(expected_keys)


def test_validate_order_parameters_error(symantec, order_kwargs, vcr):
    order_kwargs["partnercode"] = symantec.partner_code
    order_kwargs["webservertype"] = "9999"

    order_id = order_kwargs["partnerorderid"]
    csr = order_kwargs["csr"]

    with vcr.use_cassette(
        placeholders=(
            [
                {"placeholder": "<<CSR>>", "replace": csr},
                {"placeholder": "<<CSR_QUOTED>>", "replace": quote_plus(csr)},
                {"placeholder": "<<OrderID>>", "replace": order_id},
            ])):
        with pytest.raises(SymantecError) as e:
            symantec.validate_order_parameters(**order_kwargs)

    assert str(e).endswith("The Symantec API call ValidateOrderParameters"
                           " returned an error: 'Missing or Invalid Field:"
                           "  WebServerType'")


def test_reissue(symantec, order_kwargs, vcr):
    one_minute = 60

    order_kwargs["partnercode"] = symantec.partner_code
    product_code = order_kwargs["productcode"]
    order_id = order_kwargs['partnerorderid']
    csr = order_kwargs["csr"]

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

    with vcr.use_cassette(
        placeholders=(
            [
                {"placeholder": "<<CSR>>", "replace": csr},
                {"placeholder": "<<CSR_QUOTED>>", "replace": quote_plus(csr)},
                {"placeholder": "<<OrderID>>", "replace": order_id},
            ])):
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

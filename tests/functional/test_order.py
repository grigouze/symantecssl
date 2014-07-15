import datetime
import random
import string
import textwrap

from symantecssl.order import ProductCode


def test_order(symantec):
    order_id = "".join(random.choice(string.ascii_letters) for _ in range(30))

    order_data = symantec.order(
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

    assert set(order_data.keys()) == set(["GeoTrustOrderID", "PartnerOrderID"])
    assert order_data["PartnerOrderID"] == order_id


def test_get_orders_by_date_range(symantec):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    orderids = []
    for _ in range(2):
        orderids.append("".join(random.choice(string.ascii_letters)
                        for _ in range(30)))

    for orderid in orderids:
        symantec.order(
            partnercode=symantec.partner_code,
            productcode=ProductCode.SSL123,
            partnerorderid=orderid,
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

    order_list = symantec.get_orders_by_date_range(**{
        "fromdate": date,
        "todate": date,
        "partnercode": symantec.partner_code
    })

    assert len(order_list) > 1
    order_data = order_list.pop()
    assert order_data["PartnerOrderID"]
    assert order_data["OrderDate"]

import pytest
import random
import string


def create_csr():
    return b"".join(
        check_output([
            "openssl", "req", "-new", "-newkey", "rsa:2048", "-nodes",
            "-keyout", "/dev/null", "-text", "-batch", "-subj",
            "/C=US/ST=Texas/L=San Antonio/O=MyOrg/CN=example.com",
        ]).partition(b"-----BEGIN CERTIFICATE REQUEST-----")[1:]
    ).decode("ascii")


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

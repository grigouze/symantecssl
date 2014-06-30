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
            MIICzDCCAbQCAQAwYzELMAkGA1UEBhMCVVMxDjAMBgNVBAgTBVRleGFzMRQwEgYD
            VQQHEwtTYW4gQW50b25pbzENMAsGA1UEChMEVGVzdDEfMB0GA1UEAxMWdGVzdGlu
            Z3N5bWFudGVjc3NsLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB
            AOO5cCIKIGegzQDEK/Ng3+6EdY4H7ZFAvSsFFdDTXfckpBznm/j3sbjKv7LlnyoQ
            SVEhhr/mErtXfe19mSPCzJ3jUSotONnKpjvbZSLn7xJ4tZzIxS5OOY/VeLQc0V7A
            jheswmFN9+BFHMjNHEYc8KzPEe67BS2exiagwUQD+g55bQr0iZnKIYRuDQ8X5Kaq
            ivPDfGFNCo29Mwyzo6sy6fFjqFzul/kjSmIRizaxuPT6zLKAMCLIkpxVp+YPA7tB
            QORu+UvgTtsIerG8EM4SQC53Ctwxw+V2lH5t9UH4UtX+IEDn8pUVbgNHfrt8TPqZ
            ynsCKdwJQ7VmgK8wwAdM7r0CAwEAAaAkMCIGCSqGSIb3DQEJDjEVMBMwEQYJYIZI
            AYb4QgEBBAQDAgZAMA0GCSqGSIb3DQEBBQUAA4IBAQCdF9dZg6KH4VgWTJcPskCX
            feIAc+BU+7B4eA4RS7StuABz+x6ff39R9g62IM6ppIZU3VKmb3jClD/xPjHTrsiE
            0WgTG7iWBF6oOyqiTX5/w6KlWddaBq/m2YzhnpDb/IQJhxRgxt0alHBtlcglzPms
            CbbHMcSlYXIr32S20rhS1oaiI0aIPjbbEjzSViFN7IIDUCXPgb0DgQXKrZZpT9fh
            +6MlhlabtkSDrRzZXOeOFOxQBRjRlv/ZiwGhfD0u/xTnKyOU8p8XFHRFpg/zRyBf
            M7HcFYsHVIgPB1M303pLtdN91Iig7D8LLIMDl9p+HTEpNLmAVefUeq20hPZTVee6
            -----END CERTIFICATE REQUEST-----
        """)
    )

    assert set(order_data.keys()) == set(["GeoTrustOrderID", "PartnerOrderID"])
    assert order_data["PartnerOrderID"] == order_id

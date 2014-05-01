from __future__ import absolute_import, division, print_function

import pytest

from symantecssl.exceptions import SymantecError
from symantecssl.email import ResendEmail


def test_resend_email_response_success():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <ResendEmail>
        <OrderResponseHeader>
            <Timestamp>2014-05-29T19:22:45.749+0000</Timestamp>
            <PartnerOrderID>1234</PartnerOrderID>
            <SuccessCode>0</SuccessCode>
        </OrderResponseHeader>
    </ResendEmail>
    """.strip()

    assert ResendEmail().response(xml) is None


def test_resend_email_response_error():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <ResendEmail>
        <OrderResponseHeader>
            <Timestamp>2014-05-19T12:35:45.250+0000</Timestamp>
            <Errors>
                <Error>
                    <ErrorMessage>An Error Message!!</ErrorMessage>
                </Error>
            </Errors>
            <PartnerOrderID>1234</PartnerOrderID>
            <SuccessCode>-1</SuccessCode>
        </OrderResponseHeader>
    </ResendEmail>
    """.strip()

    with pytest.raises(SymantecError) as exc_info:
        ResendEmail().response(xml).response(xml)

    assert exc_info.value.args == (
        "There was an error resending the email: 'An Error Message!!'",
    )
    assert exc_info.value.errors == [{"ErrorMessage": "An Error Message!!"}]

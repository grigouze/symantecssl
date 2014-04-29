from __future__ import absolute_import, division, print_function

import pytest

from symantecssl.exceptions import SymantecValueError
from symantecssl.order import Order


def test_order_response_success():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <QuickOrder>
        <OrderResponseHeader>
            <PartnerOrderID>1234</PartnerOrderID>
            <SuccessCode>0</SuccessCode>
        </OrderResponseHeader>
        <GeoTrustOrderID>abcdefg</GeoTrustOrderID>
    </QuickOrder>
    """.strip()

    assert Order().response(xml) == {
        "PartnerOrderID": "1234",
        "GeoTrustOrderID": "abcdefg",
    }


def test_order_response_failure():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <QuickOrder>
        <OrderResponseHeader>
            <Errors>
                <Error>
                    <ErrorMessage>An Error!</ErrorMessage>
                </Error>
            </Errors>
            <SuccessCode>1</SuccessCode>
        </OrderResponseHeader>
    </QuickOrder>
    """.strip()

    with pytest.raises(SymantecValueError) as exc_info:
        Order().response(xml)

    assert exc_info.value.args == (
        "There was an error submitting this SSL certificate: 'An Error!'",
    )
    assert exc_info.value.errors == [{"ErrorMessage": "An Error!"}]

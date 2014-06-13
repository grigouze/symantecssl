from __future__ import absolute_import, division, print_function

import pytest

from symantecssl.exceptions import SymantecError
from symantecssl.order import(
    Order, GetOrderByPartnerOrderID, GetOrdersByDateRange, ModifyOrder
)


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

    with pytest.raises(SymantecError) as exc_info:
        Order().response(xml)

    assert exc_info.value.args == (
        "There was an error submitting this SSL certificate: 'An Error!'",
    )
    assert exc_info.value.errors == [{"ErrorMessage": "An Error!"}]


def test_get_order_by_partner_order_id_response_success():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <GetOrderByPartnerOrderID>
        <QueryResponseHeader>
            <Timestamp>2014-05-29T17:36:43.318+0000</Timestamp>
            <SuccessCode>0</SuccessCode>
            <ReturnCount>1</ReturnCount>
        </QueryResponseHeader>
        <OrderDetail>
            <OrderInfo>
                <Method>RESELLER</Method>
                <DomainName>testingsymantecssl.com</DomainName>
                <ProductCode>SSL123</ProductCode>
                <PartnerOrderID>1234</PartnerOrderID>
                <ServerCount>1</ServerCount>
                <ValidityPeriod>12</ValidityPeriod>
                <OrderStatusMajor>PENDING</OrderStatusMajor>
                <OrderState>WF_DOMAIN_APPROVAL</OrderState>
                <OrderDate>2014-05-29T17:36:39.000+0000</OrderDate>
                <RenewalInd>N</RenewalInd>
                <Price>35</Price>
                <GeoTrustOrderID>1806482</GeoTrustOrderID>
            </OrderInfo>
        </OrderDetail>
    </GetOrderByPartnerOrderID>
    """.strip()

    assert GetOrderByPartnerOrderID().response(xml) == {
        "OrderStatusMajor": "PENDING",
        "GeoTrustOrderID": "1806482",
        "DomainName": "testingsymantecssl.com",
        "ProductCode": "SSL123",
        "ValidityPeriod": "12",
        "OrderDate": "2014-05-29T17:36:39.000+0000",
        "Price": "35",
        "RenewalInd": "N",
        "Method": "RESELLER",
        "PartnerOrderID": "1234",
        "OrderState": "WF_DOMAIN_APPROVAL",
        "ServerCount": "1",
    }


def test_get_order_by_partner_order_id_response_failure():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <GetOrderByPartnerOrderID>
        <QueryResponseHeader>
            <Timestamp>2014-05-29T17:49:18.880+0000</Timestamp>
            <Errors>
                <Error>
                    <ErrorMessage>An Error Message!</ErrorMessage>
                </Error>
            </Errors>
            <SuccessCode>-1</SuccessCode>
            <ReturnCount>0</ReturnCount>
        </QueryResponseHeader>
    <OrderDetail/>
    </GetOrderByPartnerOrderID>
    """.strip()

    with pytest.raises(SymantecError) as exc_info:
        GetOrderByPartnerOrderID().response(xml).response(xml)

    assert exc_info.value.args == (
        "There was an error getting the order details: 'An Error Message!'",
    )
    assert exc_info.value.errors == [{"ErrorMessage": "An Error Message!"}]


def test_get_orders_by_date_range_success():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <GetOrderByPartnerOrderID>
        <QueryResponseHeader>
            <Timestamp>2014-05-29T17:36:43.318+0000</Timestamp>
            <SuccessCode>0</SuccessCode>
            <ReturnCount>1</ReturnCount>
        </QueryResponseHeader>
        <OrderDetails>
            <OrderDetail>
                <OrderInfo>
                    <Method>RESELLER</Method>
                    <DomainName>testingsymantecssl.com</DomainName>
                    <ProductCode>SSL123</ProductCode>
                    <PartnerOrderID>1234</PartnerOrderID>
                    <ServerCount>1</ServerCount>
                    <ValidityPeriod>12</ValidityPeriod>
                    <OrderStatusMajor>PENDING</OrderStatusMajor>
                    <OrderState>WF_DOMAIN_APPROVAL</OrderState>
                    <OrderDate>2014-05-29T17:36:39.000+0000</OrderDate>
                    <RenewalInd>N</RenewalInd>
                    <Price>35</Price>
                    <GeoTrustOrderID>1806482</GeoTrustOrderID>
                </OrderInfo>
            </OrderDetail>
            <OrderDetail>
                <OrderInfo>
                    <Method>RESELLER</Method>
                    <DomainName>testingsymantecssl.com</DomainName>
                    <ProductCode>SSL123</ProductCode>
                    <PartnerOrderID>1234</PartnerOrderID>
                    <ServerCount>1</ServerCount>
                    <ValidityPeriod>12</ValidityPeriod>
                    <OrderStatusMajor>PENDING</OrderStatusMajor>
                    <OrderState>WF_DOMAIN_APPROVAL</OrderState>
                    <OrderDate>2014-05-29T17:36:39.000+0000</OrderDate>
                    <RenewalInd>N</RenewalInd>
                    <Price>35</Price>
                    <GeoTrustOrderID>1806485</GeoTrustOrderID>
                </OrderInfo>
            </OrderDetail>
        </OrderDetails>
    </GetOrderByPartnerOrderID>
    """.strip()

    response = GetOrdersByDateRange().response(xml)
    assert type(response) is list
    assert response[0] == {
        "OrderStatusMajor": "PENDING",
        "GeoTrustOrderID": "1806482",
        "DomainName": "testingsymantecssl.com",
        "ProductCode": "SSL123",
        "ValidityPeriod": "12",
        "OrderDate": "2014-05-29T17:36:39.000+0000",
        "Price": "35",
        "RenewalInd": "N",
        "Method": "RESELLER",
        "PartnerOrderID": "1234",
        "OrderState": "WF_DOMAIN_APPROVAL",
        "ServerCount": "1",
    }
    assert response[1] == {
        "OrderStatusMajor": "PENDING",
        "GeoTrustOrderID": "1806485",
        "DomainName": "testingsymantecssl.com",
        "ProductCode": "SSL123",
        "ValidityPeriod": "12",
        "OrderDate": "2014-05-29T17:36:39.000+0000",
        "Price": "35",
        "RenewalInd": "N",
        "Method": "RESELLER",
        "PartnerOrderID": "1234",
        "OrderState": "WF_DOMAIN_APPROVAL",
        "ServerCount": "1",
    }


def test_get_orders_by_date_range_response_failure():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <GetOrdersByDateRange>
        <QueryResponseHeader>
            <Timestamp>2014-05-29T17:49:18.880+0000</Timestamp>
            <Errors>
                <Error>
                    <ErrorMessage>An Error Message!</ErrorMessage>
                </Error>
            </Errors>
            <SuccessCode>-1</SuccessCode>
            <ReturnCount>0</ReturnCount>
        </QueryResponseHeader>
    <OrderDetail/>
    </GetOrdersByDateRange>
    """.strip()

    with pytest.raises(SymantecError) as exc_info:
        GetOrdersByDateRange().response(xml).response(xml)

    assert exc_info.value.args == (
        "There was an error getting the order details: 'An Error Message!'",
    )
    assert exc_info.value.errors == [{"ErrorMessage": "An Error Message!"}]


def test_modify_order_response_success():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <ModifyOrder>
        <OrderResponseHeader>
            <Timestamp>2014-05-19T12:38:01.835+0000</Timestamp>
            <PartnerOrderID>OxJL7QuR2gyX7LiQHJun0</PartnerOrderID>
            <SuccessCode>0</SuccessCode>
        </OrderResponseHeader>
    </ModifyOrder>
    """.strip()

    assert ModifyOrder().response(xml) is None


def test_modify_order_response_error():
    xml = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <ModifyOrder>
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
    </ModifyOrder>
    """.strip()

    with pytest.raises(SymantecError) as exc_info:
        ModifyOrder().response(xml).response(xml)

    assert exc_info.value.args == (
        "There was an error modifying the order: 'An Error Message!!'",
    )
    assert exc_info.value.errors == [{"ErrorMessage": "An Error Message!!"}]

from mock import patch

import pytest

from symantecssl.order import FailedRequest, post_request
from symantecssl.models import GetModifiedOrderRequest, OrderDetails


class TestPostRequest(object):

    @patch("requests.post")
    def test_successful_post_request(self, mocked_post):

        endpoint = "http://www.example.com/"
        request_model = GetModifiedOrderRequest()
        credentials = {
            "partner_code": "123456",
            "username": "Krieg",
            "password": "TrainConductor"
        }

        mocked_post.return_value.status_code = 200
        mocked_post.return_value.content = (
            """
        <env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
<env:Header/>
<env:Body>
<m:GetOrderByPartnerOrderIDResponse
xmlns:m="http://api.geotrust.com/webtrust/query">
    <m:GetOrderByPartnerOrderIDResult>
        <m:QueryResponseHeader>
            <m:SuccessCode>0</m:SuccessCode>
            <m:Timestamp>2014-12-01T23:14:01.332+00:00</m:Timestamp>
            <m:ReturnCount>1</m:ReturnCount>
        </m:QueryResponseHeader>
        <m:OrderDetail>
            <m:OrderInfo>
                <m:PartnerOrderID>131000-00000</m:PartnerOrderID>
                <m:GeoTrustOrderID>10630000</m:GeoTrustOrderID>
                <m:DomainName>www.example.com</m:DomainName>
                <m:OrderDate>2013-12-27T16:01:32+00:00</m:OrderDate>
        <m:OrderCompleteDate>2013-12-27T18:02:54+00:00</m:OrderCompleteDate>
                <m:Price>000.0</m:Price>
                <m:Method>RESELLER</m:Method>
                <m:OrderStatusMajor>COMPLETE</m:OrderStatusMajor>
                <m:ValidityPeriod>3</m:ValidityPeriod>
                <m:ServerCount>1</m:ServerCount>
                <m:RenewalInd>Y</m:RenewalInd>
                <m:ProductCode>SECURESITEEV</m:ProductCode>
                <m:OrderState>COMPLETED</m:OrderState>
                <m:SealPreference>IN_TS_IN_MS</m:SealPreference>
                <m:SealStatus>TRUST_SEAL</m:SealStatus>
                <m:VulnerabilityScanInfo>
                    <m:ServiceStatus>INACTIVE</m:ServiceStatus>
                    <m:OnDemandScanInProgress>false</m:OnDemandScanInProgress>
                </m:VulnerabilityScanInfo>
            </m:OrderInfo>
            <m:QuickOrderDetail>
                <m:OrderStatusMinor>
            <m:OrderStatusMinorCode>ORDER_COMPLETE</m:OrderStatusMinorCode>
             <m:OrderStatusMinorName>Order Complete</m:OrderStatusMinorName>
                </m:OrderStatusMinor>
                <m:OrganizationInfo>
                    <m:OrganizationName>Org</m:OrganizationName>
                    <m:Division>none</m:Division>
                    <m:RegistrationNumber>S1480000</m:RegistrationNumber>
                    <m:JurisdictionRegion>Region</m:JurisdictionRegion>
                    <m:JurisdictionCountry>Country</m:JurisdictionCountry>
                    <m:OrganizationAddress>
                        <m:City>City</m:City>
                        <m:Region>Region</m:Region>
                        <m:Country>US</m:Country>
                    </m:OrganizationAddress>
                </m:OrganizationInfo>
    <m:ApproverNotifiedDate>2013-12-27T16:01:32+00:00</m:ApproverNotifiedDate>
            </m:QuickOrderDetail>
            <m:OrderContacts>
                <m:AdminContact>
                    <m:FirstName>The First</m:FirstName>
                    <m:LastName>The Last</m:LastName>
                    <m:Phone>0000000000</m:Phone>
                    <m:Email>administrator@example.com</m:Email>
                    <m:Title>Some Title</m:Title>
                    <m:OrganizationName>Some Org</m:OrganizationName>
                    <m:AddressLine1>Some Address</m:AddressLine1>
                    <m:City>Some City</m:City>
                    <m:Region>Some Region</m:Region>
                    <m:PostalCode>00000</m:PostalCode>
                    <m:Country>US</m:Country>
                </m:AdminContact>
                <m:TechContact>
                    <m:FirstName>The First</m:FirstName>
                    <m:LastName>The Last</m:LastName>
                    <m:Phone>8000000000</m:Phone>
                    <m:Email>ssl@example.com</m:Email>
                    <m:Title>SSL Ops</m:Title>
                    <m:OrganizationName>Some Org</m:OrganizationName>
                    <m:AddressLine1>Some Address</m:AddressLine1>
                    <m:City>Some City</m:City>
                    <m:Region>Some Region</m:Region>
                    <m:PostalCode>00000</m:PostalCode>
                    <m:Country>US</m:Country>
                </m:TechContact>
                <m:BillingContact>
                    <m:FirstName>Person</m:FirstName>
                    <m:LastName>Last</m:LastName>
                    <m:Phone>0000000000</m:Phone>
                    <m:Email>billing@example.com</m:Email>
                    <m:Title>Random Title</m:Title>
                    <m:OrganizationName>Nope</m:OrganizationName>
                    <m:AddressLine1>Address goes here</m:AddressLine1>
                    <m:City>A City</m:City>
                    <m:Region>A Region</m:Region>
                    <m:PostalCode>00000-0000</m:PostalCode>
                    <m:Country>US</m:Country>
                </m:BillingContact>
            </m:OrderContacts>
            <m:CertificateInfo>
                <m:CertificateStatus>ACTIVE</m:CertificateStatus>
                <m:StartDate>2014-10-21T00:00:00+00:00</m:StartDate>
                <m:EndDate>2014-12-30T23:59:59+00:00</m:EndDate>
                <m:CommonName>www.example.com</m:CommonName>
                <m:SerialNumber>A5E411</m:SerialNumber>
                <m:Locality>A Location</m:Locality>
                <m:State>Some state</m:State>
                <m:Organization>Nope</m:Organization>
                <m:Country>US</m:Country>
                <m:OrganizationalUnit>none</m:OrganizationalUnit>
                <m:RegistrationNumber>S1480000</m:RegistrationNumber>
                <m:JurisdictionRegion>Region</m:JurisdictionRegion>
                <m:JurisdictionCountry>US</m:JurisdictionCountry>
                <m:WebServerType>other</m:WebServerType>
                <m:AlgorithmInfo>
            <m:SignatureHashAlgorithm>SHA2-256</m:SignatureHashAlgorithm>
        <m:SignatureEncryptionAlgorithm>RSA</m:SignatureEncryptionAlgorithm>
                </m:AlgorithmInfo>
            </m:CertificateInfo>
            <m:Fulfillment>
                <m:CACertificates>
                    <m:CACertificate>
                        <m:Type>INTERMEDIATE</m:Type>
                        <m:CACert>-----BEGIN CERTIFICATE-----
                       ...
                        -----END CERTIFICATE-----</m:CACert>
                    </m:CACertificate>
                    <m:CACertificate>
                        <m:Type>INTERMEDIATE</m:Type>
                        <m:CACert>-----BEGIN CERTIFICATE-----
                        ...
                        -----END CERTIFICATE-----</m:CACert>
                    </m:CACertificate>
                    <m:CACertificate>
                        <m:Type>ROOT</m:Type>
                        <m:CACert>-----BEGIN CERTIFICATE-----
                        ...
                        -----END CERTIFICATE-----</m:CACert>
                    </m:CACertificate>
                </m:CACertificates>
                <m:ServerCertificate>-----BEGIN CERTIFICATE-----
               ...
                -----END CERTIFICATE-----
            </m:ServerCertificate>
        </m:Fulfillment>
        <m:AuthenticationComments/>
        <m:AuthenticationStatuses>
            <m:AuthenticationStatus>
        <m:AuthenticationStep>DOMAIN_VERIFICATION</m:AuthenticationStep>
                <m:Status>COMPLETED</m:Status>
                <m:LastUpdated>2014-10-21T15:05:05+00:00</m:LastUpdated>
            </m:AuthenticationStatus>
            <m:AuthenticationStatus>
        <m:AuthenticationStep>ORGANIZATION_VERIFICATION</m:AuthenticationStep>
                <m:Status>COMPLETED</m:Status>
                <m:LastUpdated>2014-10-21T15:05:05+00:00</m:LastUpdated>
            </m:AuthenticationStatus>
            <m:AuthenticationStatus>
                <m:AuthenticationStep>VERIFICATION_CALL</m:AuthenticationStep>
                <m:Status>COMPLETED</m:Status>
                <m:LastUpdated>2014-10-21T15:05:05+00:00</m:LastUpdated>
            </m:AuthenticationStatus>
        </m:AuthenticationStatuses>
        <m:TrustServicesDetails/>
        <m:TrialDetails>
            <m:OrderPlacedAsTrial>false</m:OrderPlacedAsTrial>
        </m:TrialDetails>
    </m:OrderDetail>
</m:GetOrderByPartnerOrderIDResult>
</m:GetOrderByPartnerOrderIDResponse>
</env:Body>
</env:Envelope>
        """
        )

        response = post_request(
            endpoint, request_model, credentials
        )

        detail = response.model[0]

        assert detail.organization_contacts.admin.email == (
            "administrator@example.com"
        )
        assert detail.organization_info.city == "City"
        assert detail.organization_info.country == "US"
        assert detail.status_code == "ORDER_COMPLETE"

    @patch("requests.post")
    def test_bad_response(self, mocked_post):

        endpoint = "http://www.example.com/"
        request_model = GetModifiedOrderRequest()
        credentials = {
            "partner_code": "123456",
            "username": "Krieg",
            "password": "TrainConductor"
        }

        mocked_post.return_value.status_code = 500
        with pytest.raises(FailedRequest):
            post_request(
                endpoint, request_model, credentials
            )

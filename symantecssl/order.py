from __future__ import absolute_import, division, print_function

import enum

from .utils import xml_to_dict
from .models import BaseModel


class ProductCode(enum.Enum):
    QuickSSLPremium = "QuickSSLPremium"
    QuickSSL = "QuickSSL"
    FreeSSL = "FreeSSL"
    RapidSSL = "RapidSSL"
    EnterpriseSSL = "ESSL"

    TrueBusinessID = "TrueBizID"
    TrueCredentials = "TrueCredentials"
    GeoCenterAdmin = "GeoCenterAdmin"

    TrueBusinessIDWithEV = "TrueBizIDEV"

    SecureSite = "SecureSite"
    SecureSitePro = "SecureSitePro"
    SecureSiteWithEV = "SecureSiteEV"
    SecureSiteProWithEV = "SecureSiteProEV"

    SSL123 = "SSL123"
    SSL123AdditionalLicense = "SSL123ASL"

    SGCSuperCerts = "SGCSuperCerts"
    SGCSuperCertAdditionalLicense = "SGCSuperCertsASL"

    SSLWebServer = "SSLWebServer"
    SSLWebServerWithEV = "SSLWebServerEV"
    SSLWebServerAdditionalLicense = "SSLWebServerASL"
    SSLWebServerWithEVAdditionalLicense = "SSLWebServerEVASL"

    SymantecCodeSigningCertificate = "VeriSignCSC"
    ThawteCodeSigningCertificate = "thawteCSC"

    GeoTrustFreeTrial = "GeoTrustFreeTrial"

    PartnerAuth = "PartnerAuth"

    VerifiedSiteSealOrg = "VerifiedSiteSealOrg"
    TrustSealInd = "TrustSealInd"
    TrustSealOrg = "TrustSealOrg"

    HourlyUsage = "HourlyUsage"

    MalwareBasic = "Malwarebasic"
    MalwareScan = "Malwarescan"


class ValidityPeriod(enum.IntEnum):
    Month = 1
    OneYear = 12
    TwoYears = 24
    ThreeYears = 36
    FourYears = 48


class WebServer(enum.IntEnum):
    ApacheSSL = 1
    ApacheRaven = 2
    ApacheSSLeay = 3
    ApacheOpenSSL = 20
    Apache2 = 21
    ApacheApacheSSL = 22

    IIS4 = 12
    IIS5 = 13
    IIS = 33

    LotusDominoGo4625 = 9
    LotusDominoGo4626 = 10
    LotusDomino = 11

    C2NetStronghold = 4
    IBMHTTP = 7
    iPlanet = 8
    NetscapeEnterpriseFastrack = 14
    ZeusV3 = 17
    CobaltSeries = 23
    Cpanel = 24
    Ensim = 25
    Hsphere = 26
    Ipswitch = 27
    Plesk = 28
    JakartTomcat = 29
    WebLogic = 30
    OReillyWebSiteProfessional = 31
    WebStar = 32

    Other = 18


class Order(BaseModel):

    _command = "QuickOrder"

    def response_result(self, xml):
        return {
            "PartnerOrderID": xml.xpath(
                "OrderResponseHeader/PartnerOrderID/text()"
            )[0],
            "GeoTrustOrderID": xml.xpath("GeoTrustOrderID/text()")[0],
        }


class GetOrderByPartnerOrderID(BaseModel):

    _command = "GetOrderByPartnerOrderID"

    def response_result(self, xml):
        return xml_to_dict(xml.xpath("OrderDetail")[0])


class GetOrdersByDateRange(BaseModel):

    _command = "GetOrdersByDateRange"

    def response_result(self, xml):
        results = []
        for order in xml.xpath("OrderDetails//OrderInfo"):
            results.append(dict((i.tag, i.text) for i in order))
        return results


class GetModifiedOrders(BaseModel):

    _command = "GetModifiedOrders"

    def response_result(self, xml):
        results = []
        for order in xml.xpath("OrderDetails/OrderDetail"):
            # Since we are grabbing both OrderInfo and Modification Events,
            # results is a dict for each category, which is easier than
            # predicting the order these two will be in.
            nodes = {}
            categories = dict((i.tag, i) for i in order)

            # Same as in the other "get" methods.
            nodes["OrderInfo"] = dict(
                (i.tag, i.text) for i in categories["OrderInfo"]
            )

            # A list of events; each entry contains a dict of values.
            events = []
            for event in categories["ModificationEvents"]:
                events.append(dict((i.tag, i.text) for i in event))
            nodes["ModificationEvents"] = events

            results.append(nodes)
        return results


class ChangeApproverEmail(BaseModel):

    _command = "ChangeApproverEmail"

    def response_result(self, xml):
        return


class Reissue(BaseModel):

    _command = "Reissue"

    def response_result(self, xml):
        return {
            "PartnerOrderID": xml.xpath(
                "OrderResponseHeader/PartnerOrderID/text()"
            )[0],
            "GeoTrustOrderID": xml.xpath("GeoTrustOrderID/text()")[0],
        }


class Revoke(BaseModel):

    _command = "Revoke"

    def response_result(self, xml):
        return {
            "PartnerOrderID": xml.xpath(
                "OrderResponseHeader/PartnerOrderID/text()"
            )[0],
            "GeoTrustOrderID": xml.xpath("GeoTrustOrderID/text()")[0],
            "SerialNumber": xml.xpath("SerialNumber/text()")[0],
        }


class ModifyOperation(enum.Enum):
    Approve = "APPROVE"
    ApproveESSL = "APPROVE_ESSL"
    ResellerApprove = "RESELLER_APPROVE"
    ResellerDisapprove = "RESELLER_DISAPPROVE"
    Reject = "REJECT"
    Cancel = "CANCEL"
    Deactivate = "DEACTIVATE"
    RequestOnDemandScan = "REQUEST_ON_DEMAND_SCAN"
    RequestVulnerabilityScan = "REQUEST_VULNERABILITY_SCAN"
    UpdateSealPreferences = "UPDATE_SEAL_PREFERENCES"
    UpdatePostStatus = "UPDATE_POST_STATUS"
    PushState = "PUSH_ORDER_STATE"


class ModifyOrder(BaseModel):

    _command = "ModifyOrder"

    def response_result(self, xml):
        return


class ValidateOrderParameters(BaseModel):

    _command = "ValidateOrderParameters"

    def response_result(self, xml):
        result = {}
        for outer in xml.xpath("/ValidateOrderParameters/child::*"):
            if outer.tag == "OrderResponseHeader":
                continue

            if outer.xpath('count(child::*)') > 0:
                result[outer.tag] = dict((i.tag, i.text) for i in outer)
            else:
                result[outer.tag] = outer.text
        return result


class GetQuickApproverList(BaseModel):

    _command = "GetQuickApproverList"

    def response_result(self, xml):
        result = []
        for approver in xml.xpath("ApproverList/Approver"):
            result.append(dict(
                (i.tag, i.text) for i in approver
            ))
        return result

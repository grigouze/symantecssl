from __future__ import absolute_import, division, print_function

import enum

import lxml.etree

from .exceptions import SymantecError
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

    def response(self, data):
        xml = lxml.etree.fromstring(data)
        success = (
            int(xml.xpath("OrderResponseHeader/SuccessCode/text()")[0]) == 0
        )

        if success:
            return {
                "PartnerOrderID": xml.xpath(
                    "OrderResponseHeader/PartnerOrderID/text()"
                )[0],
                "GeoTrustOrderID": xml.xpath("GeoTrustOrderID/text()")[0],
            }
        else:
            errors = []
            for error in xml.xpath("OrderResponseHeader/Errors/Error"):
                errors.append(dict((i.tag, i.text) for i in error))

            # We only display the first error message here, but all of them
            # will be available on the exception
            raise SymantecError(
                "There was an error submitting this SSL certificate: "
                "'{0}'".format(errors[0]["ErrorMessage"]),
                errors=errors,
            )


class GetOrderByPartnerOrderID(BaseModel):

    _command = "GetOrderByPartnerOrderID"

    def response(self, data):
        xml = lxml.etree.fromstring(data)
        success = (
            int(xml.xpath("QueryResponseHeader/SuccessCode/text()")[0]) == 0
        )

        if success:
            return dict(
                (i.tag, i.text)
                for i in xml.xpath("OrderDetail/OrderInfo/child::*")
            )
        else:
            errors = []
            for error in xml.xpath("QueryResponseHeader/Errors/Error"):
                errors.append(dict((i.tag, i.text) for i in error))

            # We only display the first error message here, but all of them
            # will be available on the exception
            raise SymantecError(
                "There was an error getting the order details: "
                "'{0}'".format(errors[0]["ErrorMessage"]),
                errors=errors,
            )


class GetOrdersByDateRange(BaseModel):
    _command = "GetOrdersByDateRange"

    def response(self, data):
        xml = lxml.etree.fromstring(data)
        success = (
            int(xml.xpath("QueryResponseHeader/SuccessCode/text()")[0]) == 0
        )

        if success:
            results = []
            for order in xml.xpath("OrderDetails//OrderInfo"):
                results.append(dict((i.tag, i.text) for i in order))
            return results

        else:
            errors = []
            for error in xml.xpath("QueryResponseHeader/Errors/Error"):
                errors.append(dict((i.tag, i.text) for i in error))

            # We only display the first error message here, but all of them
            # will be available on the exception
            raise SymantecError(
                "There was an error getting the order details: "
                "'{0}'".format(errors[0]["ErrorMessage"]),
                errors=errors,
            )


class GetModifiedOrders(BaseModel):
    _command = "GetModifiedOrders"

    def response(self, data):
        xml = lxml.etree.fromstring(data)
        success = (
            int(xml.xpath("QueryResponseHeader/SuccessCode/text()")[0]) == 0
        )

        if success:
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

        else:
            errors = []
            for error in xml.xpath("QueryResponseHeader/Errors/Error"):
                errors.append(dict((i.tag, i.text) for i in error))

            # We only display the first error message here, but all of them
            # will be available on the exception
            raise SymantecError(
                "There was an error getting the order details: "
                "'{0}'".format(errors[0]["ErrorMessage"]),
                errors=errors,
            )


class ChangeApproverEmail(BaseModel):

    _command = "ChangeApproverEmail"

    def response(self, data):
        xml = lxml.etree.fromstring(data)
        success = (
            int(xml.xpath("OrderResponseHeader/SuccessCode/text()")[0]) == 0
        )

        if not success:
            errors = []
            for error in xml.xpath("OrderResponseHeader/Errors/Error"):
                errors.append(dict((i.tag, i.text) for i in error))

            # We only display the first error message here, but all of them
            # will be available on the exception
            raise SymantecError(
                "There was an error changing the approver email: "
                "'{0}'".format(errors[0]["ErrorMessage"]),
                errors=errors,
            )


class Reissue(BaseModel):

    _command = "Reissue"

    def response(self, data):
        xml = lxml.etree.fromstring(data)
        success = (
            int(xml.xpath("OrderResponseHeader/SuccessCode/text()")[0]) == 0
        )

        if success:
            return {
                "PartnerOrderID": xml.xpath(
                    "OrderResponseHeader/PartnerOrderID/text()"
                )[0],
                "GeoTrustOrderID": xml.xpath("GeoTrustOrderID/text()")[0],
            }
        else:
            errors = []
            for error in xml.xpath("OrderResponseHeader/Errors/Error"):
                errors.append(dict((i.tag, i.text) for i in error))

            # We only display the first error message here, but all of them
            # will be available on the exception
            raise SymantecError(
                "There was an error reissuing: "
                "'{0}'".format(errors[0]["ErrorMessage"]),
                errors=errors,
            )


class ModifyOperation(enum.Enum):
    Approve = "APPROVE"
    ApproveESSL = "APPROVE_ESSL"
    ResellerApprove = "RESELLER_APPROVE"
    ResellerDisapprove = "REELLER_DISAPPROVE"
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

    def response(self, data):
        xml = lxml.etree.fromstring(data)
        success = (
            int(xml.xpath("OrderResponseHeader/SuccessCode/text()")[0]) == 0
        )

        if not success:
            errors = []
            for error in xml.xpath("OrderResponseHeader/Errors/Error"):
                errors.append(dict((i.tag, i.text) for i in error))

            # We only display the first error message here, but all of them
            # will be available on the exception
            raise SymantecError(
                "There was an error modifying the order: "
                "'{0}'".format(errors[0]["ErrorMessage"]),
                errors=errors,
            )


class GetQuickApproverList(BaseModel):

    _command = "GetQuickApproverList"

    def response(self, data):
        xml = lxml.etree.fromstring(data)
        success = (
            int(xml.xpath("QueryResponseHeader/SuccessCode/text()")[0]) == 0
        )

        if success:
            result = []
            for approver in xml.xpath("ApproverList/Approver"):
                result.append(dict(
                    (i.tag, i.text) for i in approver
                ))
            return result
        else:
            errors = []
            for error in xml.xpath("QueryResponseHeader/Errors/Error"):
                errors.append(dict((i.tag, i.text) for i in error))

            # We only display the first error message here, but all of them
            # will be available on the exception
            raise SymantecError(
                "There was an error getting the approver list: "
                "'{0}'".format(errors[0]["ErrorMessage"]),
                errors=errors,
            )

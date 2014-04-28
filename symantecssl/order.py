from __future__ import absolute_import, division, print_function

import enum

import lxml.etree

from .exceptions import SymantecValueError
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
            raise SymantecValueError(
                "There was an error submitting this SSL certificate: "
                "'{0}'".format(errors[0]["ErrorMessage"]),
                errors=errors,
            )

        return data

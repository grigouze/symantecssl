from __future__ import absolute_import, division, print_function

import enum

import lxml.etree

from .exceptions import SymantecError
from .models import BaseModel


class EmailType(enum.Enum):
    InviteEmail = "InviteEmail"
    ApproverEmail = "ApproverEmail"
    FulfillmentEmail = "FulfillmentEmail"
    PhoneAuthEmail = "PhoneAuthEmail"
    PickUpEmail = "PickUpEmail"


class ResendEmail(BaseModel):

    _command = "ResendEmail"

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
                "There was an error resending the email: "
                "'{0}'".format(errors[0]["ErrorMessage"]),
                errors=errors,
            )

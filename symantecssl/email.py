from __future__ import absolute_import, division, print_function

import enum

from .models import BaseModel


class EmailType(enum.Enum):
    InviteEmail = "InviteEmail"
    ApproverEmail = "ApproverEmail"
    FulfillmentEmail = "FulfillmentEmail"
    PhoneAuthEmail = "PhoneAuthEmail"
    PickUpEmail = "PickUpEmail"


class ResendEmail(BaseModel):

    _command = "ResendEmail"

    def response_result(self, xml):
        return

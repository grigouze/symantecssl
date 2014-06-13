from __future__ import absolute_import, division, print_function

from .auth import SymantecAuth
from .order import(
    Order, GetOrderByPartnerOrderID, GetOrdersByDateRange,
    GetModifiedOrders, ModifyOrder, ChangeApproverEmail, Reissue,
    GetQuickApproverList
)
from .email import ResendEmail
from .session import SymantecSession


class Symantec(object):

    order_class = Order
    get_order_by_partner_order_id_class = GetOrderByPartnerOrderID
    get_orders_by_date_range_class = GetOrdersByDateRange
    get_modified_orders_class = GetModifiedOrders
    get_quick_approver_list_class = GetQuickApproverList
    modify_order_class = ModifyOrder
    change_approver_email_class = ChangeApproverEmail
    reissue_class = Reissue
    resend_email_class = ResendEmail

    def __init__(self, username, password,
                 url="https://api.geotrust.com/webtrust/partner"):
        self.url = url
        self.session = SymantecSession()
        self.session.auth = SymantecAuth(username, password)

    def submit(self, obj):
        resp = self.session.post(self.url, obj.serialize())
        resp.raise_for_status()

        return obj.response(resp.content)

    def order(self, **kwargs):
        obj = self.order_class(**kwargs)
        return self.submit(obj)

    def get_order_by_partner_order_id(self, **kwargs):
        return self.submit(self.get_order_by_partner_order_id_class(**kwargs))

    def get_orders_by_date_range(self, **kwargs):
        return self.submit(self.get_orders_by_date_range_class(**kwargs))

    def get_modified_orders(self, **kwargs):
        return self.submit(self.get_modified_orders_class(**kwargs))

    def modify_order(self, **kwargs):
        return self.submit(self.modify_order_class(**kwargs))

    def change_approver_email(self, **kwargs):
        return self.submit(self.change_approver_email_class(**kwargs))

    def reissue(self, **kwargs):
        return self.submit(self.reissue_class(**kwargs))

    def resend_email(self, **kwargs):
        obj = self.resend_email_class(**kwargs)
        return self.submit(obj)

    def get_quick_approver_list(self, **kwargs):
        return self.submit(self.get_quick_approver_list_class(**kwargs))

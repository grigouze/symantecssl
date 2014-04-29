from __future__ import absolute_import, division, print_function

from .auth import SymantecAuth
from .order import Order
from .session import SymantecSession


class Symantec(object):

    order_class = Order

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

from __future__ import absolute_import, division, print_function

from requests.auth import AuthBase
from six.moves import urllib_parse


__all__ = ["SymantecAuth"]


class SymantecAuth(AuthBase):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, request):
        if request.method == "POST":
            data = urllib_parse.parse_qs(request.body)
            data["username"] = [self.username]
            data["password"] = [self.password]

            request.prepare_body(data, None)

        return request

from __future__ import absolute_import, division, print_function

import pretend
import pytest

from symantecssl.auth import SymantecAuth


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ("", {}),
        ("foo=bar", {"foo": ["bar"]}),
        ("foo=bar&wat=yes", {"foo": ["bar"], "wat": ["yes"]}),
    ],
)
def test_auth_on_post(body, expected):
    request = pretend.stub(
        method="POST",
        body=body,
        prepare_body=pretend.call_recorder(lambda data, files: None)
    )

    auth = SymantecAuth("testuser", "p@ssw0rd")

    expected = expected.copy()
    expected.update({"username": ["testuser"], "password": ["p@ssw0rd"]})

    assert auth(request) is request
    assert request.prepare_body.calls == [pretend.call(expected, None)]


def test_auth_on_get():
    request = pretend.stub(method="GET")
    auth = SymantecAuth("testuser", "p@ssw0rd")
    assert auth(request) is request

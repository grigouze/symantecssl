from __future__ import absolute_import, division, print_function

from symantecssl.exceptions import SymantecError


class TestSymantecError:

    def test_basic(self):
        errors = ["Some Error", "Another Error", "Oh No!"]

        assert SymantecError(errors=errors).errors == errors

from __future__ import absolute_import, division, print_function

from symantecssl.exceptions import SymantecValueError


class TestSymantecValueError:

    def test_basic(self):
        errors = ["Some Error", "Another Error", "Oh No!"]

        assert SymantecValueError(errors=errors).errors == errors

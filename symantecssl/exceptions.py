from __future__ import absolute_import, division, print_function


class SymantecError(Exception):

    def __init__(self, *args, **kwargs):
        self.errors = kwargs.pop("errors")
        super(SymantecError, self).__init__(*args, **kwargs)

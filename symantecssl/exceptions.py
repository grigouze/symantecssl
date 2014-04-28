from __future__ import absolute_import, division, print_function


class SymantecValueError(ValueError):

    def __init__(self, *args, **kwargs):
        self.errors = kwargs.pop("errors")
        super(SymantecValueError, self).__init__(*args, **kwargs)

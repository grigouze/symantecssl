from __future__ import absolute_import, division, print_function

import enum

from .datastructures import CaseInsensitiveDict


class BaseModel(object):

    _responsetype = "XML"

    def __init__(self, **kwargs):
        self.data = CaseInsensitiveDict(kwargs)

    def __setattr__(self, name, value):
        # Allow us to set our data attribute
        if name == "data":
            return super(BaseModel, self).__setattr__(name, value)

        self.data[name] = value

    def __getattr__(self, name):
        if name not in self.data:
            raise AttributeError(
                "'{0}' object has no attribute '{1}'".format(
                    self.__class__.__name__,
                    name,
                )
            )

        return self.data[name]

    def __delattr__(self, name):
        if name not in self.data:
            raise AttributeError(
                "'{0}' object has no attribute '{1}'".format(
                    self.__class__.__name__,
                    name,
                )
            )

        del self.data[name]

    def serialize(self):
        data = {}

        # Serialize the user provided data
        for key, value in self.data.items():
            # Turn our enums into "real" data
            if isinstance(value, enum.Enum):
                value = value.value

            data[key] = value

        # Add the command and response type
        data.update({
            "command": self._command,
            "responsetype": self._responsetype,
        })

        return data

    def response(self, data):
        # TODO: Figure out if there is some common pattern that we can extract
        #       from the various models so that they don't need to implement
        #       their own response method, or at least they only have to
        #       implement a subset.
        raise NotImplementedError

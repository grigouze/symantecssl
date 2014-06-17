from __future__ import absolute_import, division, print_function

import enum

import lxml

from .datastructures import CaseInsensitiveDict
from .exceptions import SymantecError


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
        xml = lxml.etree.fromstring(data)
        success_code = int(xml.xpath(
            "*[ "
            "     substring(  name(),  string-length(name() ) - 13  ) "
            "     = 'ResponseHeader' "
            "]"
            "/SuccessCode/text()"
        )[0])

        if success_code == 0:
            return self.response_result(xml)
        else:
            return self.response_error(xml)

    def response_error(self, xml):
        errors = []
        for error in xml.xpath(
                "*[ "
                "     substring(  name(),  string-length(name() ) - 13  ) "
                "     = 'ResponseHeader' "
                "]"
                "/Errors/Error"):
            errors.append(dict((i.tag, i.text) for i in error))

        # We only display the first error message here, but all of them
        # will be available on the exception
        raise SymantecError(
            "The Symantec API call {0} returned an error: '{1}'".format(
                self.__class__.__name__,
                errors[0]["ErrorMessage"],
            ),
            errors=errors,
        )

    def response_result(self, xml):
        raise NotImplementedError

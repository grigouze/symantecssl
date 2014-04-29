from __future__ import absolute_import, division, print_function

import enum

import pytest

from symantecssl.models import BaseModel


class FakeEnum(enum.Enum):

    thing = "thing value"


class TestBaseModel:

    def test_basic_init(self):
        m = BaseModel(a="one", B="two")
        assert m.data == {"A": "one", "b": "two"}

    def test_setattr(self):
        m = BaseModel()
        m.foo = "bar"

        assert m.data["foo"] == "bar"

    def test_getattr(self):
        assert BaseModel(foo="bar").foo == "bar"

        with pytest.raises(AttributeError):
            BaseModel().foo

    def test_delattr(self):
        m = BaseModel(foo="bar")

        assert m.foo == "bar"
        del m.foo

        with pytest.raises(AttributeError):
            m.foo

        with pytest.raises(AttributeError):
            del BaseModel().foo

    def test_serialize(self):
        class TestModel(BaseModel):
            _command = "wat wat wat"

        m = TestModel(foo="bar", thing=FakeEnum.thing)

        assert m.serialize() == {
            "foo": "bar",
            "thing": "thing value",
            "command": "wat wat wat",
            "responsetype": "XML",
        }

    def test_response(self):
        m = BaseModel()
        with pytest.raises(NotImplementedError):
            m.response(None)

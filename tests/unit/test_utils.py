from __future__ import absolute_import, division, print_function

import lxml.etree

from symantecssl.utils import xml_to_dict


def test_xml_to_dict():
    xml = b"""
    <A>
        <B>Something</B>
        <C>
            <D>MoreSomething</D>
        </C>
        <E>1234</E>
    </A>
    """.strip()

    assert xml_to_dict(lxml.etree.fromstring(xml)) == {
        "B": "Something",
        "C": {
            "D": "MoreSomething",
        },
        "E": "1234",
    }

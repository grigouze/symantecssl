from __future__ import absolute_import, division, print_function
from lxml import etree


def get_element_text(element):
    """Checks if element is NoneType.

    :param element: element to check for NoneType
    :return: text of element or "None" text
    """
    if element is not None:
        return element.text
    else:
        return "None"


def create_subelement_with_text(root_element, element, text):
    """Creates an element with given text attribute.

    :param element:
    :param text:
    :return:
    """

    ele = etree.SubElement(root_element, element)
    ele.text = text

    return ele

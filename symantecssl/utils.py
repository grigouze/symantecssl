from __future__ import absolute_import, division, print_function


def get_element_text(element):
    """Checks if element is NoneType.

    :param element: element to check for NoneType
    :return: text of element or "None" text
    """
    if element is not None:
        return element.text
    else:
        return "None"

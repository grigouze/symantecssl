from __future__ import absolute_import, division, print_function


def xml_to_dict(node):
    """
    node should be an lxml.etree element.
    """
    result = {}
    for child in node:
        if child.xpath("count(child::*)") > 0:
            result[child.tag] = xml_to_dict(child)
        else:
            result[child.tag] = child.text
    return result

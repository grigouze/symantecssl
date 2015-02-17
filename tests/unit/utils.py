from __future__ import absolute_import, division, print_function
from lxml import etree

import os


def open_xml_file(filename, mode):
    """Opens an XML file for use.

    :param filename: XML file to create file from
    :param mode: file mode for open
    :return:
    """
    base = os.path.dirname(__file__) + '/xml_test_files/'
    return open(os.path.join(base, filename), mode)


def create_node_from_file(filename):
    """Creates an xml node from a given XML file.

    :param filename: XML file to create node from
    :return: node
    """
    node = etree.parse(open_xml_file(filename, 'r'))
    return node

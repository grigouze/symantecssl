from __future__ import absolute_import, division, print_function


def open_xml_file(filename, mode):
    base = os.path.dirname(__file__)
    return open(os.path.join(base, filename), mode)
import unittest

from symantecssl.main import add


def suite():
    suite = unittest.TestSuite()
    suite.addTest(WhenTestingMain())
    return suite


class WhenTestingMain(unittest.TestCase):

    def setUp(self):
        pass

    def test_add(self):
        self.assertEqual(add(5, 2), 7)
        print('HI!')

if __name__ == '__main__':
    unittest.main()

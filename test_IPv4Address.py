import unittest
from IPv4Address import IPv4Address, IllegalArgumentException


class MyTestCase(unittest.TestCase):
    def test_create_with_string(self):
        ip = IPv4Address('127.12.45.22')
        self.assertEqual(int(ip), 2131504406)
        self.assertEqual(str(ip), '127.12.45.22')

        ip = IPv4Address('0.0.0.0')
        self.assertEqual(int(ip), 0)
        self.assertEqual(str(ip), '0.0.0.0')

        ip = IPv4Address('255.255.255.255')
        self.assertEqual(int(ip), 4294967295)
        self.assertEqual(str(ip), '255.255.255.255')

    def test_create_with_invalid_string(self):
        self.assertRaises(IllegalArgumentException, IPv4Address, '127.12.45000.22')
        self.assertRaises(IllegalArgumentException, IPv4Address, '127.-12.45.22')
        self.assertRaises(IllegalArgumentException, IPv4Address, '127.12.45.22s')
        self.assertRaises(IllegalArgumentException, IPv4Address, '127.12.45.256')
        self.assertRaises(IllegalArgumentException, IPv4Address, '127,12.45.256')

    def test_create_with_decimal(self):
        ip = IPv4Address('127.12.45.22')
        self.assertEqual(int(ip), 2131504406)
        self.assertEqual(str(ip), '127.12.45.22')

        ip = IPv4Address(0)
        self.assertEqual(int(ip), 0)
        self.assertEqual(str(ip), '0.0.0.0')

        ip = IPv4Address(4294967295)
        self.assertEqual(int(ip), 4294967295)
        self.assertEqual(str(ip), '255.255.255.255')

    def test_create_with_invalid_decimal(self):
        self.assertRaises(IllegalArgumentException, IPv4Address, -1)
        self.assertRaises(IllegalArgumentException, IPv4Address, 4294967296)

    def test_eq(self):
        self.assertEqual(IPv4Address('127.12.45.22'), IPv4Address(2131504406))
        self.assertEqual(IPv4Address('0.0.0.0'), IPv4Address(0))

    def test_gt(self):
        self.assertGreater(IPv4Address('127.12.45.23'), IPv4Address('127.12.45.22'))

    def test_lt(self):
        self.assertLess(IPv4Address('127.12.44.22'), IPv4Address('127.12.45.22'))



if __name__ == '__main__':
    unittest.main()

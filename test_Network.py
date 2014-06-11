import unittest
from Network import Network
from IPv4Address import IPv4Address, IllegalArgumentException


class MyTestCase(unittest.TestCase):

    def test_create_with_correct_params(self):
        net = Network(IPv4Address('192.168.128.1'), 25)
        self.assertEqual(str(net), '192.168.128.0/25')
        net = Network(IPv4Address('0.0.0.0'), 0)
        self.assertEqual(str(net), '0.0.0.0/0')
        net = Network(IPv4Address('255.255.255.255'), 32)
        self.assertEqual(str(net), '255.255.255.255/32')

    def test_create_with_incorrect_params(self):
        self.assertRaises(IllegalArgumentException, Network, IPv4Address('192.168.128.1'), 33)
        self.assertRaises(IllegalArgumentException, Network, IPv4Address('192.168.128.1'), -2)
        self.assertRaises(IllegalArgumentException, Network, IPv4Address('192.168.128.25'), -2)
        self.assertRaises(IllegalArgumentException, Network, IPv4Address('192.168.128.25'), '1')

    def test_broadcast_address(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(str(net.broadcast_address), '192.168.255.255')

    def test_first_usable_address(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(str(net.first_usable_address), '192.168.255.129')

    def test_last_usable_address(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(str(net.last_usable_address), '192.168.255.254')

    def test_int_mask(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(net.int_mask, 0b11111111111111111111111110000000)

    def test_str_mask(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(net.str_mask, '255.255.255.128')

    def test_mask_length(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(net.mask_length, 25)

    def test_subnets(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(str(net.subnets[0]), '192.168.255.128/26')
        self.assertEqual(str(net.subnets[1]), '192.168.255.192/26')

    def test_total_hosts(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(net.total_hosts, 126)

    def test_is_public(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertFalse(net.is_public())
        net = Network(IPv4Address('191.168.255.128'), 25)
        self.assertTrue(net.is_public())
        net = Network(IPv4Address('127.168.255.128'), 25)
        self.assertFalse(net.is_public())
        net = Network(IPv4Address('172.20.255.128'), 25)
        self.assertFalse(net.is_public())
        net = Network(IPv4Address('10.20.255.128'), 25)
        self.assertFalse(net.is_public())
















if __name__ == '__main__':
    unittest.main()

import unittest
from homework import IPv4Address, InvalidIpError, InvalidMaskError
from homework import Network
from homework import Route, Router


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
        self.assertRaises(InvalidIpError, IPv4Address, '127.12.45000.22')
        self.assertRaises(InvalidIpError, IPv4Address, '127.-12.45.22')
        self.assertRaises(InvalidIpError, IPv4Address, '127.12.45.22s')
        self.assertRaises(InvalidIpError, IPv4Address, '127.12.45.256')
        self.assertRaises(InvalidIpError, IPv4Address, '127,12.45.256')
        self.assertRaises(InvalidIpError, IPv4Address, '145.253')


    def test_create_with_invalid_type(self):
        self.assertRaises(InvalidIpError, IPv4Address, ['127.12.45.1'])
        self.assertRaises(InvalidIpError, IPv4Address, IPv4Address(0))



    def test_create_with_decimal(self):
        ip = IPv4Address('127.12.45.22')
        self.assertEqual(int(ip), 2131504406)
        self.assertEqual(str(ip), '127.12.45.22')

        ip = IPv4Address(0)
        self.assertEqual(int(ip), 0)
        self.assertEqual(str(ip), '0.0.0.0')

        ip = IPv4Address(4294967295)
        self.assertEqual(int(ip), 0xFFFFFFFF)
        self.assertEqual(str(ip), '255.255.255.255')

    def test_create_with_invalid_decimal(self):
        self.assertRaises(InvalidIpError, IPv4Address, -1)
        self.assertRaises(InvalidIpError, IPv4Address, 4294967296)
        self.assertRaises(InvalidIpError, IPv4Address, 0xFFFFFFFF1)
        self.assertRaises(InvalidIpError, IPv4Address, 1.0)

    def test_create_with_invalid_str(self):
        self.assertRaises(InvalidIpError, IPv4Address, '1.-0.1.2')
        self.assertRaises(InvalidIpError, IPv4Address, '1')
        self.assertRaises(InvalidIpError, IPv4Address, '1...')
        self.assertRaises(InvalidIpError, IPv4Address, '255.255.0.')
        self.assertRaises(InvalidIpError, IPv4Address, '.255.0.')
        self.assertRaises(InvalidIpError, IPv4Address, IPv4Address(0))
        self.assertRaises(InvalidIpError, IPv4Address, '123')
        self.assertRaises(InvalidIpError, IPv4Address, '123')
        self.assertRaises(InvalidIpError, IPv4Address, '255.255.255.255.255')
        self.assertRaises(InvalidIpError, IPv4Address, '255.255.255..255')


    def test_eq(self):
        self.assertEqual(IPv4Address('127.12.45.22'), IPv4Address(2131504406))
        self.assertEqual(IPv4Address('0.0.0.0'), IPv4Address(0))

    def test_neq(self):
        self.assertNotEqual(IPv4Address('127.12.45.21'), IPv4Address(2131504406))
        self.assertNotEqual(IPv4Address('0.0.0.1'), IPv4Address(0))

    def test_gt(self):
        self.assertGreater(IPv4Address('127.12.45.23'), IPv4Address('127.12.45.22'))

    def test_ge(self):
        self.assertGreaterEqual(IPv4Address('127.12.45.23'), IPv4Address('127.12.45.22'))
        self.assertGreaterEqual(IPv4Address('127.12.45.22'), IPv4Address('127.12.45.22'))

    def test_lt(self):
        self.assertLess(IPv4Address('127.12.44.22'), IPv4Address('127.12.45.22'))

    def test_le(self):
        self.assertLessEqual(IPv4Address('127.12.44.22'), IPv4Address('127.12.45.22'))
        self.assertLessEqual(IPv4Address('127.12.44.22'), IPv4Address('127.12.44.22'))

    def test_add(self):
        ip_address = IPv4Address('0.0.0.1') + (2)
        self.assertEqual(ip_address, 3)
        self.assertRaises(InvalidIpError, ip_address.__add__, IPv4Address('255.255.255.255'))

    def test_sub(self):
        ip_address = IPv4Address('0.0.0.3') - (2)
        self.assertEqual(ip_address, 1)
        self.assertRaises(InvalidIpError, ip_address.__sub__, IPv4Address('0.0.0.10'))


    def test_create_with_correct_params(self):
        net = Network(IPv4Address('192.168.128.1'), 25)
        self.assertEqual(str(net), '192.168.128.0/25')
        net = Network(IPv4Address('0.0.0.0'), 0)
        self.assertEqual(str(net), '0.0.0.0/0')
        net = Network(IPv4Address('255.255.255.255'), 32)
        self.assertEqual(str(net), '255.255.255.255/32')

    def test_create_with_incorrect_params(self):
        self.assertRaises(InvalidMaskError, Network, IPv4Address('192.168.128.1'), 33)
        self.assertRaises(InvalidMaskError, Network, IPv4Address('192.168.128.1'), -2)
        self.assertRaises(InvalidMaskError, Network, IPv4Address('192.168.128.25'), -2)
        self.assertRaises(InvalidMaskError, Network, IPv4Address('192.168.128.25'), '1')

    def test_broadcast_address(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(str(net.broadcast_address), '192.168.255.255')
        net = Network(IPv4Address('192.168.255.0'), 30)
        self.assertEqual(str(net.broadcast_address), '192.168.255.3')


    def test_first_usable_address(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(str(net.first_usable_address), '192.168.255.129')
        net = Network(IPv4Address('0.0.0.0'), 0)
        self.assertEqual(str(net.first_usable_address), '0.0.0.1')
        net = Network(IPv4Address('10.10.10.0'), 30)
        self.assertEqual(str(net.first_usable_address), '10.10.10.1')
        net = Network(IPv4Address('10.10.10.0'), 31)
        self.assertEqual(str(net.first_usable_address), 'None')
        net = Network(IPv4Address('10.10.10.0'), 32)
        self.assertEqual(str(net.first_usable_address), '10.10.10.0')

    def test_last_usable_address(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(str(net.last_usable_address), '192.168.255.254')
        net = Network(IPv4Address('192.168.255.255'), 32)
        net = Network(IPv4Address('0.0.0.0'), 0)
        self.assertEqual(str(net.last_usable_address), '255.255.255.254')
        net = Network(IPv4Address('10.10.10.0'), 30)
        self.assertEqual(str(net.last_usable_address), '10.10.10.2')
        net = Network(IPv4Address('10.10.10.0'), 31)
        self.assertEqual(str(net.last_usable_address), 'None')
        net = Network(IPv4Address('10.10.10.0'), 32)
        self.assertEqual(str(net.last_usable_address), '10.10.10.0')

    def test_mask(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(net.mask, 0b11111111111111111111111110000000)
        net = Network(IPv4Address('10.10.10.0'), 18)
        self.assertEqual(net.mask, IPv4Address('255.255.192.0'))


    def test_mask_length(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(net.mask_length, 25)

    def test_subnets(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(str(net.subnets[0]), '192.168.255.128/26')
        self.assertEqual(str(net.subnets[1]), '192.168.255.192/26')
        net = Network(IPv4Address('192.168.255.128'), 30)
        self.assertEqual(str(net.subnets[0]), '192.168.255.128/31')
        self.assertEqual(str(net.subnets[1]), '192.168.255.130/31')
        net = Network(IPv4Address('192.168.255.128'), 31)
        self.assertEqual(str(net.subnets[0]), '192.168.255.128/32')
        self.assertEqual(str(net.subnets[1]), '192.168.255.129/32')
        net = Network(IPv4Address('192.168.255.128'), 32)
        self.assertEqual(str(net.subnets), str([]))

    def test_total_hosts(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertEqual(net.total_hosts, 126)
        net = Network(IPv4Address('192.168.255.128'), 32)
        self.assertEqual(net.total_hosts, 1)
        net = Network(IPv4Address('192.168.255.128'), 31)
        self.assertEqual(net.total_hosts, 0)
        net = Network(IPv4Address('192.168.255.128'), 30)
        self.assertEqual(net.total_hosts, 2)

    def test_is_public(self):
        net = Network(IPv4Address('192.168.255.128'), 25)
        self.assertFalse(net.public)
        net = Network(IPv4Address('191.168.255.128'), 25)
        self.assertTrue(net.public)
        net = Network(IPv4Address('127.168.255.128'), 25)
        self.assertFalse(net.public)
        net = Network(IPv4Address('172.20.255.128'), 25)
        self.assertFalse(net.public)
        net = Network(IPv4Address('10.20.255.128'), 25)
        self.assertFalse(net.public)
        net = Network(IPv4Address('225.20.255.128'), 25)
        self.assertFalse(net.public)
        net = Network(IPv4Address('182.20.255.128'), 25)
        self.assertTrue(net.public)
        net = Network(IPv4Address('10.1.1.1'), 32)
        self.assertFalse(net.public)

    def test_route_creation(self):
        route = Route(Network(IPv4Address('10.123.1.0'), 24), '192.168.0.1', 'en0', 10)
        self.assertEqual(str(route), 'net: 10.123.1.0/24, gateway: 192.168.0.1, interface: en0, metric: 10')
        route = Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 10)
        self.assertEqual(str(route), 'net: 10.123.1.0/24, interface: en0, metric: 10')

    def test_router_creation(self):
        routes = set([Route(Network(IPv4Address('10.123.1.0'), 24), '192.168.0.1', 'en0', 10),
                  Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 10)])
        router = Router(routes)
        self.assertEqual(1, 1)

    def test_add_route(self):
        routes = set([Route(Network(IPv4Address('10.123.1.0'), 24), '192.168.0.1', 'en0', 10),
        Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 10)])
        router = Router(routes)
        routes_quantity = len(router.routes)
        router.add_route(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 11))
        routes_quantity2 = len(router.routes)
        self.assertEqual(routes_quantity2, routes_quantity+1)

    def test_remove_route(self):
        routes = set([Route(Network(IPv4Address('10.123.1.0'), 24), '192.168.0.1', 'en0', 10),
              Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 10),
              Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 100)])
        router = Router(routes)
        router.routes.remove(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 100))
        self.assertEqual(len(router.routes), 2)

    def test_route_for_address(self):
        routes = set([Route(Network(IPv4Address('0.0.0.0'), 0), '192.168.0.1', 'en0', 10)])
        routes.add(Route(Network(IPv4Address('192.168.0.0'), 24), None, 'en0', 10))
        routes.add(Route(Network(IPv4Address('10.0.0.0'), 8), '10.123.0.1', 'en1', 10))
        routes.add(Route(Network(IPv4Address('10.123.1.0'), 20), None, 'en1', 100))
        routes.add(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en3', 102))
        routes.add(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en4', 103))
        routes.add(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en2', 101))

        router = Router(routes)
        self.assertEqual(str(router.route_for_address(IPv4Address('10.123.1.1'))),
                         'net: 10.123.1.0/24, interface: en2, metric: 101')

        routes.add(Route(Network(IPv4Address('10.123.1.0'), 25), None, 'en2', 101))
        self.assertEqual(str(router.route_for_address(IPv4Address('10.123.1.1'))),
                         'net: 10.123.1.0/25, interface: en2, metric: 101')

        routes.add(Route(Network(IPv4Address('10.123.1.0'), 25), None, 'en2', 10))
        self.assertEqual(str(router.route_for_address(IPv4Address('10.123.1.1'))),
                         'net: 10.123.1.0/25, interface: en2, metric: 10')

if __name__ == '__main__':
    unittest.main()

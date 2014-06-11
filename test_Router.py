from IPv4Address import IPv4Address, IllegalArgumentException
from Network import Network
from Router import Route, Router

import unittest


class MyTestCase(unittest.TestCase):
    def test_route_creation(self):
        route = Route(Network(IPv4Address('10.123.1.0'), 24), '192.168.0.1', 'en0', 10)
        self.assertEqual(str(route), 'net: 10.123.1.0/24, gateway: 192.168.0.1, interface: en0, metric: 10')
        route = Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 10)
        self.assertEqual(str(route), 'net: 10.123.1.0/24, interface: en0, metric: 10')

    def test_router_creation(self):
        routes = [Route(Network(IPv4Address('10.123.1.0'), 24), '192.168.0.1', 'en0', 10),
                  Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 10)]
        router = Router(routes)
        self.assertEqual(1, 1)

    def test_add_route(self):
        routes = [Route(Network(IPv4Address('10.123.1.0'), 24), '192.168.0.1', 'en0', 10),
              Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 10)]
        router = Router(routes)
        routes_quantity = len(router.routes)
        router.routes.append(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 10))
        routes_quantity2 = len(router.routes)
        self.assertEqual(routes_quantity2, routes_quantity+1)

    def test_remove_route(self):
        routes = [Route(Network(IPv4Address('10.123.1.0'), 24), '192.168.0.1', 'en0', 10),
              Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 10),
              Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 100)]
        router = Router(routes)
        router.routes.remove(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en0', 100))
        self.assertEqual(len(router.routes), 2)

    def test_route_for_address(self):
        routes = [Route(Network(IPv4Address('0.0.0.0'), 0), '192.168.0.1', 'en0', 10)]
        routes.append(Route(Network(IPv4Address('192.168.0.0'), 24), None, 'en0', 10))
        routes.append(Route(Network(IPv4Address('10.0.0.0'), 8), '10.123.0.1', 'en1', 10))
        routes.append(Route(Network(IPv4Address('10.123.0.0'), 20), None, 'en1', 100))
        routes.append(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en2', 101))
        routes.append(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en3', 102))
        routes.append(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en4', 103))

        router = Router(routes)
        self.assertEqual(str(router.route_for_address(IPv4Address('10.123.1.1'))),
                         'net: 10.123.1.0/24, interface: en2, metric: 101')













if __name__ == '__main__':
    unittest.main()

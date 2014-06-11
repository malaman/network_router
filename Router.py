from IPv4Address import IPv4Address, IllegalArgumentException
from Network import Network


class Route(object):
    def __init__(self, network, gateway, interface_name, metric):
        self.__class__._validate_route(network, interface_name, metric)
        self._network = network
        self._interface_name = interface_name
        self._metric = metric
        if gateway is not None:
            self._gateway = IPv4Address(gateway)
        else:
            self._gateway = None

    @classmethod
    def _validate_route(cls, network, interface_name, metric):
        if isinstance(network, Network)  \
                and isinstance(metric, int) and isinstance(interface_name, str):
            if metric >= 0:
                return True
        raise IllegalArgumentException

    @property
    def network(self):
        return self._network

    @property
    def gateway(self):
        return self._gateway

    @property
    def interface_name(self):
        return self._interface_name

    @property
    def metric(self):
        return self._metric

    @property
    def network(self):
        return self._network

    def __str__(self):
        if self._gateway:
            return 'net: {}, gateway: {}, interface: {}, metric: {}'.format(self._network, self._gateway,
                self._interface_name, self._metric)
        else:
            return 'net: {}, interface: {}, metric: {}'.format(self._network, self._interface_name, self._metric)

    def __eq__(self, other):
        if self._gateway is None and other.gateway is None:
            return self._network == other.network and self.interface_name == other.interface_name \
            and self._metric == other.metric
        if self._gateway and other.gateway:
            return self._network == other.network and self.interface_name == other.interface_name \
                and self._metric == other.metric and self._gateway == other.gateway
        return False


class Router(object):
    def __init__(self, routes):
        self._routes = routes

    def add_route(self, route):
        self._routes.append(route)

    @property
    def routes(self):
        return self._routes

    def remove_route(self, route):
        self._routes.remove(route)

    def route_for_address(self, address):
        """
        1. Filter routes, which match address. Find longest subnet mask for matched routes. If one route finded
        return the route.
        2. Filter routes with mask_length equal longest subnet mask. If one route finded, return the route
        3. Find first route with minimal metric and return the route
        """
        route_candidate_lst = []
        longest_mask = -1
        for route in self._routes:
            if route.network.address == int(address) & route.network.int_mask:
                route_candidate_lst.append(route)
                if route.network.mask_length > longest_mask:
                    longest_mask = route.network.mask_length

        if len(route_candidate_lst) == 0:
            return None
        if len(route_candidate_lst) == 1:
            return route_candidate_lst[0]

        route_candidate_lst = [route for route in route_candidate_lst if route.network.mask_length == longest_mask]
        min_metric = route_candidate_lst[0].metric
        min_route_index = 0
        for index, route in enumerate(route_candidate_lst):
            if min_metric > route.metric:
                min_metric = route.metric
                min_route_index = index
        return route_candidate_lst[min_route_index]

if __name__ == '__main__':
    routes = [Route(Network(IPv4Address('0.0.0.0'), 0), '192.168.0.1', 'en0', 10)]
    routes.append(Route(Network(IPv4Address('192.168.0.0'), 24), None, 'en0', 10))
    routes.append(Route(Network(IPv4Address('10.0.0.0'), 8), '10.123.0.1', 'en1', 10))
    routes.append(Route(Network(IPv4Address('10.123.0.0'), 20), None, 'en1', 100))
    routes.append(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en2', 101))
    routes.append(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en3', 102))
    routes.append(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en4', 103))

    router = Router(routes)
    print(router.route_for_address(IPv4Address('10.123.1.1')))



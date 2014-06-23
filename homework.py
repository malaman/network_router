class InvalidIpError(ValueError):
    pass


class InvalidMaskError(ValueError):
    pass


class IPv4Address(object):
    # void
    def __init__(self, address):
        # address is str or int
        # raises InvalidIpError
        (self._int_ip, self._string_ip) = self._validate_ip(address)

    @classmethod
    def _validate_ip(cls, ip_address):
        """
        Verifies correctness of ip_address according to IPv4 address format

        Args:
            ip_address: string or integer
        Returns:
            value1: representation of ip address in int format
            value2: representation of ip address in string format
        """
        if isinstance(ip_address, str):
            return cls.str_to_int(ip_address), ip_address
        if isinstance(ip_address, int):
            return ip_address, cls.int_to_str(ip_address)
        raise InvalidIpError

    # int
    @classmethod
    def str_to_int(cls, ip):
        octets = ip.split('.')
        if len(octets) < 4:
            raise InvalidIpError
        int_octets = []
        for index, octet in enumerate(octets):
            int_octets.append(cls.__octet_to_int(octet) << (32 - (index + 1) * 8))
        return sum(int_octets)

    # int
    @classmethod
    def __octet_to_int(cls, octet):
        if octet.isdigit():
            int_octet = int(octet)
            if 0 <= int_octet <= 255:
                return int_octet
        raise InvalidIpError


    # str
    @classmethod
    def int_to_str(cls, integer):
        if integer < 0 or integer > 4294967295:
            raise InvalidIpError
        octet_list = []
        for i in range(0, 32, 8):
            octet_list.insert(0, str((integer & 0xFF << i) >> i))
        return '.'.join(octet_list)

    # int
    def __int__(self):
        return self._int_ip

    # str
    def __repr__(self):
        return self._string_ip

    # bool
    def __eq__(self, ipv4address):
        return int(self) == int(ipv4address)

    # bool
    def __ne__(self, ipv4address):
        return int(self) != int(ipv4address)

    # bool
    def __lt__(self, ipv4address):
        return int(self) < int(ipv4address)

    # bool
    def __gt__(self, ipv4address):
        return int(self) > int(ipv4address)

    # bool
    def __le__(self, ipv4address):
        return int(self) <= int(ipv4address)

    # bool
    def __ge__(self, ipv4address):
        return int(self) >= int(ipv4address)

    # IPv4Address
    def __add__(self, ipv4address):
        return IPv4Address(int(self) + int(ipv4address))

    # IPv4Address
    def __sub__(self, ipv4address):
        return IPv4Address(int(self) - int(ipv4address))


class Network(object):
    # static
    private_networks = None

    # void
    def __init__(self, ipv4address, int_mask_length):
        # raises ValueError, InvalidMaskError
        if isinstance(ipv4address, IPv4Address):
            self._mask = self._validate_mask(int_mask_length)
            self._mask_length = int_mask_length
            self._address = IPv4Address(int(ipv4address) & self._mask)
        else:
            raise ValueError

    @classmethod
    def _validate_mask(cls, mask_length):
        if isinstance(mask_length, int):
            if 0 <= mask_length <= 32:
                mask = (2 ** mask_length - 1) << (32-mask_length)
                return mask
        raise InvalidMaskError

    # bool
    def __contains__(self, ipv4address):
        # raises ValueError
        if isinstance(ipv4address, IPv4Address):
            return int(ipv4address) & self._mask == self._address
        raise ValueError

    # IPv4Address
    @property
    def address(self):
        return self._address

    # IPv4Address
    @property
    def broadcast_address(self):
        return IPv4Address((int(self._address) | int(self.wildcard)))

    # IPv4Address
    @property
    def first_usable_address(self):
        if self._mask_length < 31:
            return IPv4Address(int(self._address)+1)
        if self._mask_length == 31:
            return None
        return IPv4Address(int(self._address))

    # IPv4Address
    @property
    def last_usable_address(self):
        if self._mask_length < 31:
            return IPv4Address((int(self._address) | int(self.wildcard) - 1))
        if self._mask_length == 31:
            return None
        return IPv4Address(int(self._address))

    # IPv4Address
    @property
    def mask(self):
        return IPv4Address(self._mask)

    # IPv4Address
    @property
    def wildcard(self):
        return IPv4Address(self._mask ^ 0xFFFFFFFF)

    # int
    @property
    def mask_length(self):
        return self._mask_length

    # list of two subnets, or an empty list
    @property
    def subnets(self):
        subnets_list = []
        if self._mask_length < 32:
            new_mask_length = self._mask_length + 1
            subnets_list = [Network(IPv4Address(int(self._address)), new_mask_length),
                            Network(IPv4Address(int(self._address) | 1 << (32-new_mask_length)), new_mask_length)]
        return subnets_list

    # int
    @property
    def total_hosts(self):
        return 2 ** (32-self._mask_length)

    # bool
    @property
    def public(self):
        if self.__class__.private_networks is None:
            self.__class__.private_networks = [Network(IPv4Address('10.0.0.0'), 8), Network(IPv4Address('127.0.0.0'), 8),
                        Network(IPv4Address('172.16.0.0'), 12), Network(IPv4Address('192.168.0.0'), 16),
                        Network(IPv4Address('224.0.0.0'), 3)]
        for network in self.__class__.private_networks:
            if self._address in network:
                return False
        return True

    # str
    def __repr__(self):
        return '{}/{}'.format(str(self._address), self._mask_length)

    # bool
    def __eq__(self, network):
        return self._address == network.address and self._mask_length == network.mask_length

    # bool
    def __ne__(self, network):
        return not self == network


class Route(object):
    # void
    def __init__(self, network, ipv4_gateway, str_interface_name, int_metric):
        # raises ValueError
        self.__class__._validate_route(network, str_interface_name, int_metric)
        self._network = network
        self._interface_name = str_interface_name
        self._metric = int_metric
        if ipv4_gateway is not None:
            self._gateway = IPv4Address(ipv4_gateway)
        else:
            self._gateway = IPv4Address('0.0.0.0')

    @classmethod
    def _validate_route(cls, network, interface_name, metric):
        if isinstance(network, Network)  \
                and isinstance(metric, int) and isinstance(interface_name, str):
            if metric >= 0:
                return True
        raise ValueError

    # IPv4Address
    @property
    def gateway(self):
        return self._gateway

    # str
    @property
    def interface_name(self):
        return self._interface_name

    # Network
    @property
    def network(self):
        return self._network

    # int
    @property
    def metric(self):
        return self._metric

    # str
    def __repr__(self):
        if int(self._gateway):
            return 'net: {}, gateway: {}, interface: {}, metric: {}'.format(self._network, self._gateway,
                                                                    self._interface_name, self._metric)
        else:
            return 'net: {}, interface: {}, metric: {}'.format(self._network, self._interface_name, self._metric)


    # bool
    def __eq__(self, route):
        return self._network == route.network and self.interface_name == route.interface_name \
            and self._metric == route.metric and self._gateway == route.gateway

    # bool
    def __ne__(self, route):
        return not self == route

    # int
    def __hash__(self):
        return super().__hash__()


class Router(object):
    # void
    def __init__(self, routes):
        self._routes = routes

    # void
    def add_route(self, route):
        self._routes.append(route)

    # Route or None
    def route_for_address(self, ipv4address):
        route_candidate_lst = []
        route_candidate_lst = [route for route in self._routes
                               if route.network.address == int(ipv4address) & int(route.network.mask)]
        if len(route_candidate_lst) == 0:
            return None
        if len(route_candidate_lst) == 1:
            return route_candidate_lst[0]
        longest_mask = max(route_candidate_lst, key=lambda x: x.network.mask_length).network.mask_length
        route_candidate_lst = [route for route in route_candidate_lst if route.network.mask_length == longest_mask]
        return min(route_candidate_lst, key=lambda x: x.metric)

    # set
    @property
    def routes(self):
        return self._routes

    # void
    def remove_route(self, route):
        self._routes.remove(route)


if __name__ == '__main__':
    ip = IPv4Address('0.0.145.253')
    print(ip)
    print(ip.int_to_str(2131504406))
    print(ip.str_to_int('127.2.3.255'))
    net = Network(IPv4Address('255.1.1.1'),17)
    print(net.first_usable_address)
    print(net.mask)
    routes = [Route(Network(IPv4Address('0.0.0.0'), 0), '192.168.0.1', 'en0', 10)]
    routes.append(Route(Network(IPv4Address('192.168.0.0'), 24), None, 'en0', 10))
    routes.append(Route(Network(IPv4Address('10.0.0.0'), 8), '10.123.0.1', 'en1', 10))
    routes.append(Route(Network(IPv4Address('10.123.0.0'), 20), None, 'en1', 100))
    routes.append(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en2', 101))
    routes.append(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en3', 102))
    routes.append(Route(Network(IPv4Address('10.123.1.0'), 24), None, 'en4', 103))

    router = Router(routes)
    print(router.routes)
    print(router.route_for_address(IPv4Address('10.123.1.1')))
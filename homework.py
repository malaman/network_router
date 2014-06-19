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
            if ip_address < 0 or ip_address > 4294967295:
                raise InvalidIpError
            binary_str = '{0:032b}'.format(ip_address)
            octets = []
            binary_octets = []
            for i in range(0, 32, 8):
                octet = binary_str[i:i+8]
                octets.append(str(int(octet, 2)))
                binary_octets.append(octet)
            if all(octet for octet in octets if cls._is_octet(octet)):
                return ip_address, '.'.join(octets)
        raise InvalidIpError

    @staticmethod
    def _is_octet(octet):
        """
        Verifies if particular octet is in IPv4 address format

        Args:
            octet: integer or string
        Returns:
            True or raises InvalidIpError
        """
        if isinstance(octet, int):
            octet = str(octet)
        if octet.isdigit():
            int_octet = int(octet)
            if 0 <= int_octet <= 255:
                return True
        raise InvalidIpError


    # int
    @classmethod
    def str_to_int(cls, ip):
        octets = ip.split('.')
        binary_octets = ['{0:08b}'.format(int(octet)) for octet in octets if cls._is_octet(octet)]
        return int(''.join(binary_octets), 2)

    # int
    @staticmethod
    def __octet_to_int(octet):
        pass

    # str
    @classmethod
    def int_to_str(cls, integer):
        if integer < 0 or integer > 4294967295:
            raise InvalidIpError
        binary_str = '{0:032b}'.format(integer)
        octets = []
        binary_octets = []
        for i in range(0, 32, 8):
            octet = binary_str[i:i+8]
            octets.append(str(int(octet, 2)))
            binary_octets.append(octet)
        if all(octet for octet in octets if cls._is_octet(octet)):
            return integer, '.'.join(octets)

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
        self._mask = self._validate(int_mask_length)
        self._mask_length = int_mask_length
        self._address = IPv4Address(int(ipv4address) & self._mask)

    @classmethod
    def _validate(cls, mask_length):
        if isinstance(mask_length, int):
            if 0 <= mask_length <= 32:
                mask = (2 ** mask_length - 1) << (32-mask_length)
                return mask
        raise InvalidMaskError

    # bool
    def __contains__(self, ipv4address):
        # raises ValueError
        result = int(ipv4address) & self._mask == self._address
        if result:
            return True
        raise ValueError

    # IPv4Address
    @property
    def address(self):
        return self._address

    # IPv4Address
    @property
    def broadcast_address(self):
        return IPv4Address((int(self._address) | self.wildcard))

    # IPv4Address
    @property
    def first_usable_address(self):
        return IPv4Address(int(self._address)+1)

    # IPv4Address
    @property
    def last_usable_address(self):
        return IPv4Address((int(self._address) | self.wildcard) - 1)

    # IPv4Address
    @property
    def mask(self):
        return self._mask

    # IPv4Address
    @property
    def wildcard(self):
        return self._mask ^ 0xFFFFFFFF

    # int
    @property
    def mask_length(self):
        return self._mask_length

    # list of two subnets, or an empty list
    @property
    def subnets(self):
        if self._mask_length < 32:
            new_mask_length = self._mask_length + 1
            subnets_list = [Network(int(self._address), new_mask_length)]
            bit_setter = 1 << (32-new_mask_length)
            subnets_list.append(Network(int(self._address) | bit_setter, new_mask_length))
            return subnets_list

    # int
    @property
    def total_hosts(self):
        return 2 ** (32-self._mask_length) - 2

    # bool
    @property
    def public(self):
        if self.__class__.private_networks is None:
            self.__class__.private_networks = [Network(IPv4Address('10.0.0.0'), 8), Network(IPv4Address('127.0.0.0'), 8),
                        Network(IPv4Address('172.16.0.0'), 12), Network(IPv4Address('192.168.0.0'), 16),
                        Network(IPv4Address('224.0.0.0'), 3)]
        for network in self.__class__.private_networks:
            try:
                if self._address in network:
                    return False
            except ValueError:
                pass
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
            self._gateway = None

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
        if self._gateway:
            return 'net: {}, gateway: {}, interface: {}, metric: {}'.format(self._network, self._gateway,
                                                                    self._interface_name, self._metric)
        else:
            return 'net: {}, interface: {}, metric: {}'.format(self._network, self._interface_name, self._metric)


    # bool
    def __eq__(self, route):
        if self._gateway is None and route.gateway is None:
            return self._network == route.network and self.interface_name == route.interface_name \
                and self._metric == route.metric
        if self._gateway and route.gateway:
            return self._network == route.network and self.interface_name == route.interface_name \
                and self._metric == route.metric and self._gateway == route.gateway
        return False

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
        longest_mask = -1
        for route in self._routes:
            if route.network.address == int(ipv4address) & route.network.mask:
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


    # set
    @property
    def routes(self):
        return self._routes

    # void
    def remove_route(self, route):
        self._routes.remove(route)

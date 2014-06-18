from IPv4Address import IPv4Address, IllegalArgumentException


class Network(object):
    def __init__(self, ip_address, mask_length):
        self._mask = self._validate(mask_length)
        self._mask_length = mask_length
        self._address = IPv4Address(int(ip_address) & self._mask)

    @classmethod
    def _validate(cls, mask_length):
        if isinstance(mask_length, int):
            if 0 <= mask_length <= 32:
                mask = (2 ** mask_length - 1) << (32-mask_length)
                return mask
        raise IllegalArgumentException

    def contains(self, address):
        return int(address) & self._mask == self._address

    @property
    def address(self):
        return self._address

    @property
    def broadcast_address(self):
        return IPv4Address((int(self._address) | self._mask ^ 0xFFFFFFFF))

    @property
    def first_usable_address(self):
        return IPv4Address(int(self._address)+1)

    @property
    def last_usable_address(self):
        return IPv4Address((int(self._address) | self._mask ^ 0xFFFFFFFF) - 1)

    @property
    def int_mask(self):
        return self._mask

    @property
    def str_mask(self):
        str_mask = '{0:032b}'.format(self._mask)
        return '.'.join(str(int(str_mask[i:i+8], 2)) for i in range(0, 32, 8))

    @property
    def mask_length(self):
        return self._mask_length

    @property
    def subnets(self):
        if self._mask_length < 32:
            new_mask_length = self._mask_length + 1
            subnets_list = [Network(int(self._address), new_mask_length)]
            bit_setter = 1 << (32-new_mask_length)
            subnets_list.append(Network(int(self._address) | bit_setter, new_mask_length))
            return subnets_list

    @property
    def total_hosts(self):
        return 2 ** (32-self._mask_length) - 2

    def is_public(self):
        if (IPv4Address('9.255.255.255') < self._address < IPv4Address('11.0.0.0')) or \
                (IPv4Address('126.255.255.255') < self._address < IPv4Address('128.0.0.0')):
            return False
        if (IPv4Address('172.15.255.255') < self._address < IPv4Address('172.32.0.0')) or \
                (IPv4Address('192.167.255.255') < self._address < IPv4Address('192.169.0.0')):
            return False
        if self._address > IPv4Address('223.255.255.255'):
            return False
        return True

    def __str__(self):
        return '{}/{}'.format(str(self._address), self._mask_length)

    def __eq__(self, other):
        return self._address == other.address and self._mask_length == other.mask_length

if __name__ == '__main__':
    ip_address = IPv4Address('172.16.128.128')
    net = Network(ip_address, 25)
    print(net)
    print(net.address)
    print(net.first_usable_address)
    print(net.last_usable_address)
    print(net.broadcast_address)
    print(net.str_mask)
    print(net.mask_length)
    print(net.contains(IPv4Address('192.168.1.128')))
    print(net.is_public())
    print(net.total_hosts)
    print(str(net.subnets[0]))
    print(str(net.subnets[1]))
    print(net.subnets[1].total_hosts)
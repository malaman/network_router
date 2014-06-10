class IllegalArgumentException(Exception):
    pass


class IPv4Address(object):
    def __init__(self, ip_address):
        (self._int_ip, self._string_ip) = self._validate_ip(ip_address)

    @classmethod
    def _validate_ip(cls, ip_address):
        if isinstance(ip_address, str):
            octets = ip_address.split('.')
            binary_octets = ['{0:08b}'.format(int(octet)) for octet in octets if cls._is_octet(octet)]
            return int(''.join(binary_octets), 2), ip_address
        if isinstance(ip_address, int):
            if ip_address < 0 or ip_address > 4294967295:
                raise IllegalArgumentException
            binary_str = '{0:032b}'.format(ip_address)
            octets = []
            binary_octets = []
            for i in range(0, 32, 8):
                octet = binary_str[i:i+8]
                octets.append(str(int(octet, 2)))
                binary_octets.append(octet)
            if all(octet for octet in octets if cls._is_octet(octet)):
                return ip_address, '.'.join(octets)
        raise IllegalArgumentException

    @classmethod
    def _is_octet(cls, octet):
        if isinstance(octet, int):
            octet = str(octet)
        if octet.isdigit():
            int_octet = int(octet)
            if 0 <= int_octet <= 255:
                return True
        raise IllegalArgumentException

    def to_string(self):
        return self._string_ip

    def to_long(self):
        return self._int_ip

    def __eq__(self, other):
        return self._int_ip == other.to_long()

    def __gt__(self, other):
        return self._int_ip > other.to_long()

    def __lt__(self, other):
        return self._int_ip < other.to_long()


if __name__ == '__main__':
    ip = IPv4Address('127.12.45.22')
    print(ip.to_long())
    print(ip.to_string())
#!env python3
# ==============================================================================================
# Copyright (c) 2013,2023 Gustavo Arzola
# ==============================================================================================
'''
This modules implements a class object useful in both Django and Flask.  Django has TRUSTED_IPs.
Flask DebugToolbar has DEBUG_TB_HOSTS.  In both cases, this class make it easier to specify any
combination of specific hosts and network ranges and in both IPv4 and IPv6.

See the README.md at https://github.com/garzola/cidrlist for more information
'''



__author__ = '"Gustavo Arzola" <gustavo@xcode.com>'
__license__ = 'GPL version 3 or later'



import ipaddress



class CIDRlist (list):
    """ this class make it easier to specify any combination of specific hosts and network
    ranges and in both IPv4 and IPv6.  See the end of this file for some usage examples.
    """


    def __init__(self, *cidrlist):
        """ create a list of CIDR objects from the list of strings passed in.  Accepted
            notations include:

                These all represent a specific host address
                '192.168.1.1'
                '192.168.1.1/255.255.255.255'
                '192.168.1.1/32'

                These all represent a specific network of addresses
                '192.168.0.0/16'
                '192.168.0.0/255.255.0.0'
                '192.168.0.0/0.0.255.255'

            @type cidrlist: list of strings
            @param cidrlist: a list of addresses and networks in CIDR notation
        """
        self.cidrs = []
        for cidr in cidrlist:
            self.append(ipaddress.ip_network(cidr, strict=False))

    def __contains__(self, ip):
        ''' Determine if the IP address provided is in one of the network or equal to one of the
            addresses provided when this object was instantiated.

            @rtype: boolean
            @returns: True if the IP address is in or matches a address previous provided.
        '''

        if ip.startswith('::ffff:'):
            #flup is annoying --  sometimes reports IPv6 when I was expecting IPv4
            addr = ipaddress.IPv4Network(ip[7:])
        else:
            addr = ipaddress.IPv4Network(ip)

        for cidr in self:
            if addr.overlaps(cidr):
                return True

        return False



if __name__ == '__main__':

    c = CIDRlist('10.0.0.0/8', '127.0.0.1/8', '1.2.3.0/24', '8.8.8.8')

    print("test 1: '10.10.10.1' in c")
    assert '10.10.10.1' in c

    print("test 2: '127.0.0.1' in c")
    assert '127.0.0.1' in c

    print("test 2: '127.0.0.2' in c")
    assert '127.0.0.2' in c

    print("test 3: '192.168.1.1' not in c")
    assert '192.168.1.1' not in c

    print("test 4: '1.2.3.4' in c")
    assert '1.2.3.4' in c

    print("test 5: '8.8.8.8' in c")
    assert '8.8.8.8' in c

    print("test 6: '8.8.4.4' not in c")
    assert '8.8.4.4' not in c

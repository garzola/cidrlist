#!env python
# ==============================================================================================
# Copyright (c) 2013 Gustavo Arzola
#
#                                     ALL RIGHTS RESERVED
#
#   This program is free software; you can redistribute it and/or modify it under the terms of
#   the GNU General Public License as published by the Free Software Foundation; either version
#   2 of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#   without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#   See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along with this program;
#   if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
#   02111-1307 USA
#
#   Written by Gustavo Arzola (gustavo@xcode.com)
# ---------------------------------------------------------------------------------------------
# $Id$
# ==============================================================================================
'''
module documentataion string.
'''



__author__ = '"Gustavo Arzola" <gustavo@xcode.com>'
__license__ = 'GPL version 3 or later'



import ipaddress



class CIDRlist (list):
    """ This class is only meant to be used for INTERNAL_IPS. The
    code below allows INTERNAL_IPS to have networks instead of
    individual addresses -- which makes it way more useful.
    
        Example usage:
    
        INTERNAL_IPS = CIDR_LIST('10.1.1.0/8', '10.3.0.0/16')
        
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
    

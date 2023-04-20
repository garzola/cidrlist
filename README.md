# CIDRlist

Both the Django and Flask frameworks support trusted IP addresses for testing and debugging. Both use a simple list of strings that represent IP addresses.  For example, Django uses "TRUSTED_IPS".  An example that allows "10.1.1.14" and "192.168.4.3" would look like this:

    TRUSTED_IPS = ("10.1.1.14", "192.168.4.3",)

This system works when you have only one or only a few addresses that you want to mark as trusted.  In corporate environments, you may want to include entire subnets.  The only way to make it work without this module is to list each address individually.  Which sucks when you want to include all of the private networks (10/8, 172.16/12, 192.168/16).

If you choose to use the CIDRlist implementation, the example above looks like:

    from cidrlist import CIDRlist
    TRUSTED_IPS = CIDRlist("10.1.1.14", "192.168.4.3",)

If you wanted to include a the RFC 1918 Private Networks, it would look like:

    from cidrlist import CIDRlist
    TRUSTED_IPS = CIDRlist("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16",)

IPv6 is also supported.  The following allows only the localhost to connect:

    from cidrlist import CIDRlist
    TRUSTED_IPS = CIDRlist("::1/128",)

You can mix all of these together and add a few more:

    from cidrlist import CIDRlist
    TRUSTED_IPS = CIDRlist("10.1.1.14", "192.168.4.3", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "::1/128", "fc00::/7", "2001:db8::/32",)
    

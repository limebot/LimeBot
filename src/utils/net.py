###
# Copyright (c) 2002-2005, Jeremiah Fincher
# Copyright (c) 2011, 2013, James McCoy
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

"""
Simple utility modules.
"""

import re
import socket

from .web import _ipAddr, _domain

emailRe = re.compile(r"^(\w&.+-]+!)*[\w&.+-]+@(%s|%s)$" % (_domain, _ipAddr),
                     re.I)

def getAddressFromHostname(host, port=None, attempt=0):
    addrinfo = socket.getaddrinfo(host, port)
    addresses = []
    for (family, socktype, proto, canonname, sockaddr) in addrinfo:
        if sockaddr[0] not in addresses:
            addresses.append(sockaddr[0])
    return addresses[attempt % len(addresses)]

def getSocket(host, port=None, socks_proxy=None, vhost=None, vhostv6=None):
    """Returns a socket of the correct AF_INET type (v4 or v6) in order to
    communicate with host.
    """
    if not socks_proxy:
        addrinfo = socket.getaddrinfo(host, port)
        host = addrinfo[0][4][0]
    if socks_proxy:
        import socks
        s = socks.socksocket()
        hostname, port = socks_proxy.rsplit(':', 1)
        s.setproxy(socks.PROXY_TYPE_SOCKS5, hostname, int(port),
                rdns=True)
        return s
    import supybot.conf as conf
    if isIPV4(host):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not vhost:
            vhost = conf.supybot.protocols.irc.vhost()
        if vhost:
            s.bind((vhost, 0))
        return s
    elif isIPV6(host):
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        if not vhostv6:
            vhostv6 = conf.supybot.protocols.irc.vhostv6()
        if vhostv6:
            s.bind((vhostv6, 0))
        return s
    else:
        raise socket.error('Something wonky happened.')

def isIP(s):
    """Returns whether or not a given string is an IP address.

    >>> isIP('255.255.255.255')
    1

    >>> isIP('::1')
    0
    """
    return isIPV4(s) or isIPV6(s)

def isIPV4(s):
    """Returns whether or not a given string is an IPV4 address.

    >>> isIPV4('255.255.255.255')
    1

    >>> isIPV4('abc.abc.abc.abc')
    0
    """
    try:
        return bool(socket.inet_aton(str(s)))
    except socket.error:
        return False

def bruteIsIPV6(s):
    if s.count('::') <= 1:
        L = s.split(':')
        if len(L) <= 8:
            for x in L:
                if x:
                    try:
                        int(x, 16)
                    except ValueError:
                        return False
            return True
    return False

def isIPV6(s):
    """Returns whether or not a given string is an IPV6 address."""
    try:
        if hasattr(socket, 'inet_pton'):
            return bool(socket.inet_pton(socket.AF_INET6, s))
        else:
            return bruteIsIPV6(s)
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, '::')
        except socket.error:
            # We gotta fake it.
            return bruteIsIPV6(s)
        return False

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

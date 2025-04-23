#!/usr/bin/env python3
"""
Simple asynchronous DNS server using asyncio and DatagramProtocol.

This example is from Chapter 13 of the book "Python 3 Object-Oriented Programming".
It responds to DNS queries for three hardcoded domains using a UDP socket.

Domains supported:
- facebook.com. → 173.252.120.6
- yougov.com. → 213.52.133.246
- wipo.int. → 193.5.93.80

To test:
Run this script, then in another terminal:
$ nslookup -port=4343 facebook.com localhost
"""

import asyncio
from contextlib import suppress

# Domain → IP map
ip_map = {
    b'facebook.com.': '173.252.120.6',
    b'yougov.com.': '213.52.133.246',
    b'wipo.int.': '193.5.93.80'
}

def lookup_dns(data):
    """Parse DNS query to extract the domain name."""
    domain = b''
    try:
        pointer, part_length = 13, data[12]
        while part_length:
            domain += data[pointer:pointer + part_length] + b'.'
            pointer += part_length + 1
            part_length = data[pointer - 1]
    except IndexError:
        domain = b'invalid.'

    ip = ip_map.get(domain, '127.0.0.1')
    return domain, ip

def create_response(data, ip):
    """Build a valid DNS response packet with the given IP."""
    ba = bytearray
    packet = ba(data[:2]) + ba([129, 128]) + data[4:6] * 2
    packet += ba([0, 0, 0, 1]) + data[12:]
    packet += ba([192, 12, 0, 1, 0, 1, 0, 0, 0, 60, 0, 4])
    for x in ip.split('.'): packet.append(int(x))
    return packet

class DNSProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print("Received request from", addr[0])
        domain, ip = lookup_dns(data)
        print("Sending IP", ip, "for", domain.decode(), "to", addr[0])
        response = create_response(data, ip)
        self.transport.sendto(response, addr)

# Setup event loop and UDP endpoint
loop = asyncio.get_event_loop()
transport, protocol = loop.run_until_complete(
    loop.create_datagram_endpoint(
        DNSProtocol,
        local_addr=('127.0.0.1', 4343)
    )
)
print("DNS Server running on UDP port 4343")

with suppress(KeyboardInterrupt):
    loop.run_forever()

# Gracefully close
transport.close()
loop.close()

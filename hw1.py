#! /usr/bin/python

import time

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, Switch
from mininet.cli import CLI

class Router(Node):
    "Node with Linux Router Function"
    
    def config(self, **params):
        super(Router, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(Router, self).terminate()

def topology():
    net = Mininet(autoStaticArp=True)

    # Initialize objects dicts
    hosts, switches, routers = {}, {}, {}

    # Create Host, from h1 to h8
    for i in range(2):
        host = net.addHost('h%d' % (i + 1))
        hosts['h%d' % (i + 1)] = host

    # Create Switch, from s1 to s6
    for i in range(6):
        switch = net.addSwitch('s%d' % (i + 1), failMode='standalone')
        switches['s%d' % (i + 1)] = switch

    # Create Router, from r1 to r5
    for i in range(3):
        router = net.addHost('r%d' % (i + 1), cls=Router)
        routers['r%d' % (i + 1)] = router

    links = [('h1', 'r1'), ('h2', 'r2'),
             ('r1', 'r3'),('r3','r2')]

    for link in links:
        src, dst = link
        net.addLink(src, dst)

    net.start()

    # Configure network manually
    config(hosts, switches, routers)

    # Comment this line if you don't need to debug
    CLI(net)

    # Checking homework's status
    net.stop()

def config(hosts, switches, routers):

    # Hosts, Routers IP configuration
    hosts['h1'].cmd('ifconfig h1-eth0 10.0.0.1/8')
    hosts['h1'].cmd('ip route add default dev h1-eth0')

    hosts['h2'].cmd('ifconfig h2-eth0 10.0.0.2/8')
    hosts['h2'].cmd('ip route add default via 10.0.0.9 dev h1-eth0')

    #routers['r1'].cmd('ifconfig r1-eth0 10.0.0.8/8')
    routers['r1'].cmd('ifconfig r1-eth1 172.20.0.1/16')
    routers['r1'].cmd('ip route add 140.114.0.0/24 via 172.20.0.2')
    routers['r1'].cmd('ip link add vxlan65535 type vxlan id 65535 dstport 4789 srcport 4789 4790 remote 140.114.0.1 dev r1-eth1')
    routers['r1'].cmd('ip link set vxlan65535 up')
    routers['r1'].cmd('ip link add br0 type bridge')
    routers['r1'].cmd('ip link set r1-eth0 master br0');
    routers['r1'].cmd('ip link set vxlan65535 master br0');
    routers['r1'].cmd('ip link set br0 up');

    #routers['r2'].cmd('ifconfig r2-eth0 10.0.0.9/24')
    routers['r2'].cmd('ifconfig r2-eth1 140.114.0.1/24')
    routers['r2'].cmd('ip route add 140.113.0.0/24 via 140.114.0.2')
    #routers['r2'].cmd('ip route add 172.20.0.0/16 via 140.114.0.2')
    routers['r2'].cmd('ip link add vxlan65535 type vxlan id 65535 dstport 4789 srcport 4789 4790 remote 1.2.3.4 dev r2-eth1')
    routers['r2'].cmd('ip link set vxlan65535 up')
    routers['r2'].cmd('ip link add br0 type bridge')
    routers['r2'].cmd('ip link set r2-eth0 master br0')
    routers['r2'].cmd('ip link set vxlan65535 master br0')
    routers['r2'].cmd('ip link set br0 up')

    routers['r3'].cmd('ifconfig r3-eth0 172.20.0.2/16')
    routers['r3'].cmd('ifconfig r3-eth1 140.114.0.2/24')
    routers['r3'].cmd('iptables -t nat -A POSTROUTING -s 172.20.0.0/16 -d 0.0.0.0/0 -o r3-eth1 -j SNAT --to-source 140.113.0.15')

if __name__ == '__main__':
    topology()



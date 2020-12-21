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

    # Create Host, from h1 to h6
    for i in range(6):
        host = net.addHost('h%d' % (i + 1))
        hosts['h%d' % (i + 1)] = host
    # Create DHCP server, hostA and host
    hostA = net.addHost('hostA')
    hostB = net.addHost('hostB')
    # Create Switch, from s1 to s7
    for i in range(7):
        switch = net.addSwitch('s%d' % (i + 1), failMode='standalone')
        switches['s%d' % (i + 1)] = switch

    # Create Router, from r1 to r6
    for i in range(6):
        router = net.addHost('r%d' % (i + 1), cls=Router)
        routers['r%d' % (i + 1)] = router
    # link pairs
    links = [('r4', 's5'), ('r5', 's5'),
             ('r4', 's4'), ('r5', 's6'), 
             ('r1', 's4'), ('r2', 's4'),
             ('r1', 's1'), ('r2', 's2'), 
             ('h1', 's2'), ('h2', 's2'), 
             ('r3', 's4'), ('r3', 's3'),
             ('h3', 's3'), ('h4', 's3'), 
             ('r6', 's6'), ('r6', 's7'), 
             ('h5', 's7'), ('h6', 's7'),
             ('hostA', 's1'), ('hostB', 's1')
            ]
    #create link
    for link in links:
        src, dst = link
        net.addLink(src, dst)

    net.start()

    # Configure network manually
    config(hosts, switches, routers, hostA, hostB)

    # Comment this line if you don't need to debug
    CLI(net)

    # Checking homework's status
    if check(hosts):
        print('\033[92mACCEPT\033[0m')
    else:
        print('\033[91mWRONG ANSWER\033[0m')

    net.stop()

def config(hosts, switches, routers, hostA, hostB):

    # Hosts, Routers IP configuration
    hosts['h1'].cmd('ifconfig h1-eth0 192.168.1.65/26')
    hosts['h2'].cmd('ifconfig h2-eth0 192.168.1.66/26')
    hosts['h3'].cmd('ifconfig h3-eth0 192.168.1.129/26')
    hosts['h4'].cmd('ifconfig h4-eth0 192.168.1.130/26')
    hosts['h5'].cmd('ifconfig h5-eth0 192.168.3.1/24')
    hosts['h6'].cmd('ifconfig h6-eth0 192.168.3.2/24')
    hostA.cmd('ifconfig hostA-eth0 192.168.1.1/26')
    hostB.cmd('ifconfig hostB-eth0 192.168.1.2/26')
    

    routers['r1'].cmd('ifconfig r1-eth0 10.0.1.2/24')
    routers['r1'].cmd('ifconfig r1-eth1 192.168.63/26')
    routers['r2'].cmd('ifconfig r2-eth0 10.0.1.3/24')
    routers['r2'].cmd('ifconfig r2-eth1 192.168.1.126/26')
    routers['r3'].cmd('ifconfig r3-eth0 10.0.1.4/24')
    routers['r3'].cmd('ifconfig r3-eth1 192.168.1.190/24')
    routers['r4'].cmd('ifconfig r4-eth0 10.0.0.1/24')
    routers['r4'].cmd('ifconfig r4-eth1 10.0.1.1/24')
    routers['r5'].cmd('ifconfig r5-eth0 10.0.0.2/24')
    routers['r5'].cmd('ifconfig r5-eth1 10.0.2.1/24')
    routers['r6'].cmd('ifconfig r6-eth0 10.0.2.3/24')
    routers['r6'].cmd('ifconfig r6-eth1 192.168.3.254/24') 


    # Host routing table configuration
    hosts['h1'].cmd('route add default gw 192.168.1.126')
    hosts['h2'].cmd('route add default gw 192.168.1.126')
    hosts['h3'].cmd('route add default gw 192.168.1.190')
    hosts['h4'].cmd('route add default gw 192.168.1.190')
    hosts['h5'].cmd('route add default gw 192.168.3.254')
    hosts['h6'].cmd('route add default gw 192.168.3.254')
    hostA.cmd('route add default gw 192.168.1.62')
    hostB.cmd('route add default gw 192.168.1.62')

    # Router routing table configuration
    routers['r1'].cmd('route add -net 192.168.3.0/24 gw 10.0.1.1')
    routers['r1'].cmd('route add -net 192.168.1.64/26 gw 10.0.1.3')
    routers['r1'].cmd('route add -net 192.168.1.128/26 gw 10.0.1.4')

    routers['r2'].cmd('route add -net 192.168.1.0/26 gw 10.0.1.2')
    routers['r2'].cmd('route add -net 192.168.1.128/26 gw 10.0.1.4')
    routers['r2'].cmd('route add -net 192.168.3.0/24 gw 10.0.1.1')

    routers['r3'].cmd('route add -net 192.168.1.0/26 gw 10.0.1.2')
    routers['r3'].cmd('route add -net 192.168.1.64/26 gw 10.0.1.3')
    routers['r3'].cmd('route add -net 192.168.3.0/24 gw 10.0.1.1')

    routers['r4'].cmd('route add -net 192.168.3.0/24 gw 10.0.0.2')
    routers['r4'].cmd('route add -net 192.168.1.0/26 gw 10.0.1.2')
    routers['r4'].cmd('route add -net 192.168.1.64/26 gw 10.0.1.3')
    routers['r4'].cmd('route add -net 192.168.1.128/26 gw 10.0.1.4')

    routers['r5'].cmd('route add -net 192.168.1.0/26 gw 10.0.0.1')
    routers['r5'].cmd('route add -net 192.168.1.64/26 gw 10.0.0.1')
    routers['r5'].cmd('route add -net 192.168.1.128/26 gw 10.0.0.1')
    routers['r5'].cmd('route add -net 192.168.3.0/24 gw 10.0.2.3')

    routers['r6'].cmd('route add -net 192.168.1.0/26 gw 10.0.2.1')
    routers['r6'].cmd('route add -net 192.168.1.64/26 gw 10.0.2.1')
    routers['r6'].cmd('route add -net 192.168.1.128/26 gw 10.0.2.1')



def check(hosts):
    correctFlag = True

    ips = {'h1': '192.168.1.65'  , 'h2': '192.168.1.66'  ,
           'h3': '192.168.1.129' , 'h4': '192.168.1.130' ,
           'h5': '192.168.3.1', 'h6': '192.168.3.2',
        }

    for pair in [(src[0], dst) for src in sorted(ips.items(), key=lambda d: d[0]) for dst in ips if src != dst]:
        src, dst = pair
        checkstr = hosts[src].cmd('ping %s -c 1 -W 1' % ips[dst])
        if '64 bytes from %s' % ips[dst] not in checkstr:
            print('\033[93m%s doesn\'t have connectivity to %s\033[0m' % (src, dst))
            correctFlag = False

    return correctFlag

if __name__ == '__main__':
    topology()



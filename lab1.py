#! /usr/bin/python

import time

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, Switch
from mininet.cli import CLI


def topology():
    net = Mininet()

    # Initialize objects dicts

    net.addHost('h1')
    net.addHost('h2')
    net.addHost('h3')
    net.addHost('h4')
    net.addSwitch('s1',failMode = 'standalone')
    net.addSwitch('s2',failMode = 'standalone')
    net.addSwitch('s3',failMode = 'standalone')

	

    net.addLink('h1','s1')
    net.addLink('h2','s1')
    net.addLink('h3','s2')
    net.addLink('h4','s2')
    net.addLink('s3','s1')
    net.addLink('s3','s2')
    net.start()

    CLI(net)

    net.stop()

if __name__ == '__main__':
    topology()



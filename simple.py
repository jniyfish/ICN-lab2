from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import Node,Switch
from mininet.node import Node,Switch
class MyTopo(Topo):
	def __init__(self):
		Topo.__init__(self)

		h1 = self.addHost("h1")
#		h1.cmd('ip link add vxlan100 type vxlan id 100 dstport 4789 srcport 4789 4890 remote 1,2,3,4 dev h1 -eth0')
		h2 = self.addHost("h2")
		r1 = self.addHost("r1")
		r2 = self.addHost("r2")
		r3 = self.addHost("r3")
		s1 = self.addSwitch("s1")
		s2 = self.addSwitch("s2")

		self.addLink(s1,h1)
		self.addLink(s2,h2)
		self.addLink(s1,r1)
		self.addLink(s2,r1)

topos = {"fuck": MyTopo}

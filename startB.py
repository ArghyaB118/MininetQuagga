#!/usr/bin/python

"""
Example network of Quagga routers
(QuaggaTopo + QuaggaService)
"""

import sys
import atexit

# patch isShellBuiltin
import mininet.util
import mininext.util
mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
sys.modules['mininet.util'] = mininet.util

from mininet.util import dumpNodeConnections
from mininet.node import OVSController
from mininet.log import setLogLevel, info

from mininext.cli import CLI
from mininext.net import MiniNExT

from topo import QuaggaTopo

net = None

import time

def pingh1h2():
	global net
	h1 = net.getNodeByName("h1")
	h2 = net.getNodeByName("h2")
	print h1.cmd('ping -c 10 %s' %h2.IP())	


def pingh1h2Convergence():
	global net
	h1 = net.getNodeByName("h1")
	h2 = net.getNodeByName("h2")
	for i in range(1,10):
		print h1.cmd('ping -c1 %s' % h2.IP())
		print "Time: " + str(time.time())
		time.sleep(1)

def linkDown():
	global net
	h1 = net.getNodeByName("h1")
	h2 = net.getNodeByName("h2")
	print "Taking link down"
	print "Time: " + str(time.time())
	net.configLinkStatus('r1', 'r3', 'down')
	for i in xrange(1,3):
		print h1.cmd('ping -c1 %s' % h2.IP())
		print"Time: " + str(time.time())
		time.sleep(1)



def startNetwork():
    "instantiates a topo, then starts the network and prints debug information"

    info('** Creating Quagga network topology\n')
    topo = QuaggaTopo()

    info('** Starting the network\n')
    global net
    net = MiniNExT(topo, controller=OVSController)
    net.start()

    # assign IPs to interfaces.
    topo.setIP(net)

    # change IP forwarding variable to 1
    for host in net.hosts:
        host.cmd("echo '1' > /proc/sys/net/ipv4/ip_forward")
	
	pingh1h2Convergence()
	#linkDown()
    # info('** Dumping host connections\n')
    # dumpNodeConnections(net.hosts)

    #info('** Dumping host processes\n')
    #for host in net.hosts:
     #   host.cmdPrint("ps aux")

  #  net.get('h1').cmdPrint("python /home/riplite.py h1 &")
  #  net.get('h2').cmdPrint("python /home/riplite.py h2 &")
  #  net.get('r1').cmdPrint("python /home/riplite.py r1 &")
  #  net.get('r2').cmdPrint("python /home/riplite.py r2 &")
  #  net.get('r3').cmdPrint("python /home/riplite.py r3 &")
  #  net.get('r4').cmdPrint("python /home/riplite.py r4 &")

    info('** Testing network connectivity\n')
    net.ping(net.hosts)

    info('** Running CLI\n')
    CLI(net)


def stopNetwork():
    "stops a network (only called on a forced cleanup)"

    if net is not None:
        info('** Tearing down Quagga network\n')
        net.stop()

if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()

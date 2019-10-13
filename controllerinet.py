#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Containernet
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.util import customClass
from mininet.link import TCLink
import subprocess
import time
# Compile and run sFlow helper script
# - configures sFlow on OVS
# - posts topology to sFlow-RT
# execfile('sflow-rt/extras/sflow.py') 

# # Rate limit links to 10Mbps
link = customClass({'tc':TCLink}, 'tc,bw=10')

class TestingTopo(Topo):
    def build(self, n=1):
        switch = self.addSwitch('s1')

def simpleTest():
    info('*** Starting network\n')
    topo = TestingTopo()
    c1 = RemoteController('c1', ip='127.0.0.1')
    net = Containernet(topo=topo, link=link, controller=c1) #
    d1 = net.addDocker('d1', dimage="tests", volumes=["/home/osboxes/Documents/tests/:/mnt/vol1:rw"])
    net.addLink(d1, net.get('s1'))
    s1 = net.get('s1')
    net.start()

    # Connect switch to Internet NAT
    s1.cmdPrint('ovs-vsctl add-port s1 enp0s3')

    # Setup mirrored port interface
    s1.cmdPrint('ovs-vsctl add-port s1 snort0')
    s1.cmdPrint('ovs-vsctl set interface snort0 type=internal')
    s1.cmdPrint('sudo ip link set snort0 up')
    s1.cmdPrint('ovs-vsctl show')

    # Disable docker NAT connection
    d1.cmdPrint('ifconfig eth0 down')
    
    # Reset and connect d1 to internet through s1
    d1.cmdPrint('ifconfig d1-eth0 0')
    d1.cmdPrint('dhclient d1-eth0')
    # Confirm d1 is connected to internet
    d1.cmdPrint('ping -c 2 google.com')
    info('*** Running CLI\n')
    CLI(net)
    # Quit CLI to start packet capture
    tcpdump = 'sudo timeout 930 tcpdump -i snort0 -w /home/osboxes/Documents/tests/pcaps/vulahometrain1.pcap'
    process = subprocess.Popen(tcpdump.split())
    # Start selenium powered application test (simulate website interaction)
    d1.cmdPrint('python /mnt/vol1/WebTrafficSDN/vulatest.py')
    #CLI(net)
    tcpdump = 'sudo timeout 930 tcpdump -i snort0 -w /home/osboxes/Documents/tests/pcaps/youtubehometrain1.pcap'
    process = subprocess.Popen(tcpdump.split())
    d1.cmdPrint('python /mnt/vol1/WebTrafficSDN/youtubetest.py')
    #CLI(net)
    tcpdump = 'sudo timeout 930 tcpdump -i snort0 -w /home/osboxes/Documents/tests/pcaps/outlookhometrain1.pcap'
    process = subprocess.Popen(tcpdump.split())
    d1.cmdPrint('python /mnt/vol1/WebTrafficSDN/outlooktest.py')
    

    info('*** Stopping network')
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()

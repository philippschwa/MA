# -*-  Mode: Python; -*-
# /*
#  * This program is free software; you can redistribute it and/or modify
#  * it under the terms of the GNU General Public License version 2 as
#  * published by the Free Software Foundation;
#  *
#  * This program is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  * GNU General Public License for more details.
#  *
#  * You should have received a copy of the GNU General Public License
#  * along with this program; if not, write to the Free Software
#  * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#  *
#  * Ported to Python by Mohit P. Tahiliani
#  */

import ns.core
import ns.network
#import ns.point_to_point
import ns.applications
#import ns.wifi
#import ns.mobility
import ns.csma
import ns.internet
import sys
import ns.CommandLine

############### Setup simple topo for first tests ###############

# //  Network Topology - Simple Ethernet with three nodes. n1 & n2 are normal nodes, n3 is the malicious attacker
# //
# //    n1   n2   n3
# //    |    |    |
# //    ============
# //    LAN 10.1.2.0


def main():

    dosEnabled = False
    
    cmd = ns.CommandLine()
    
    cmd.addValue("DoSEnabled", "DoS enabled", dosEnabled)
    cmd.Parse(argc, argv)
    
    # Enable logging
    ns.core.LogComponentEnable(
        "UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
    ns.core.LogComponentEnable(
        "UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

    # Node 1 & 2 are normal Peers
    # Node 3 is attacker
    csmaNodes = ns.network.NodeContainer()
    csmaNodes.Create(3)

    # set Ethernet parameters
    csma = ns.csma.CsmaHelper()
    csma.SetChannelAttribute("DataRate", ns.core.StringValue("100Mbps"))
    csma.SetChannelAttribute(
        "Delay", ns.core.TimeValue(ns.core.NanoSeconds(6560)))
    csmaDevices = csma.Install(csmaNodes)

    # Setting up IP adresses
    # n1 = 10.1.1.1
    # n2 = 10.1.1.2
    # n3 = 10.1.1.3
    stack = ns.internet.InternetStackHelper()
    stack.Install(csmaNodes)
    address = ns.internet.Ipv4AddressHelper()
    address.SetBase(ns.network.Ipv4Address("10.1.1.0"),
                    ns.network.Ipv4Mask("255.255.255.0"))
    csmaInterfaces = address.Assign(csmaDevices)

    ############### Sample application with n1 as EchoServer and n2 & n3 as EchoClients ###############
    if (dosEnabled):
        # install udpEchoServer on n1
        echoServer = ns.applications.UdpEchoServerHelper(9)
        serverApps = echoServer.Install(csmaNodes.Get(0))
        serverApps.Start(ns.core.Seconds(1.0))
        serverApps.Stop(ns.core.Seconds(10.0))

        # install echo Client on n1 & n2
        echoClient = ns.applications.UdpEchoClientHelper(
                csmaInterfaces.GetAddress(0), 9)
        echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(5))
        echoClient.SetAttribute(
                "Interval", ns.core.TimeValue(ns.core.Seconds(1.0)))
        echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

        clientApps = echoClient.Install(csmaNodes.Get(1))
        clientApps = echoClient.Install(csmaNodes.Get(2))

        clientApps.Start(ns.core.Seconds(2.0))
        clientApps.Stop(ns.core.Seconds(10.0))

        ns.internet.Ipv4GlobalRoutingHelper.PopulateRoutingTables()

        ns.core.Simulator.Stop(ns.core.Seconds(10.0))

        # Enable tracing
        csma.EnablePcap("EchoServer", csmaDevices.Get(0), True)
        csma.EnablePcap("EchoClient1", csmaDevices.Get(1), True)
        csma.EnablePcap("EchoClient2", csmaDevices.Get(2), True)

    """
    if (dosEnabled)
        NS_LOG_INFO("Enable DoS")
        uint16_t port = 7001
        #Discard port(RFC 863)
        OnOffHelper onoff("ns3::UdpSocketFactory",
                          Address(InetSocketAddress(Ipv4Address("172.24.2.29"), port)))
        onoff.SetConstantRate(DataRate("50Mbps"))
        # onoff.SetAttribute("OnTime", StringValue("ns3::ConstantRandomVariable[Constant=" + ON_TIME + "]"))
        #onoff.SetAttribute("OffTime", StringValue("ns3::ConstantRandomVariable[Constant=" + OFF_TIME + "]"))
        ApplicationContainer onOffapps = onoff.Install(n.Get(2))
        onOffapps.Start(Seconds(20.0))
        onOffapps.Stop(Seconds(50.0))
    """ 

    # Start Simulation
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()


if __name__ == "__main__":
    main()


"""

cmd = ns.core.CommandLine()
cmd.nCsma = 3
cmd.verbose = "True"
cmd.nWifi = 3
cmd.tracing = "False"

cmd.AddValue("nCsma", "Number of \"extra\" CSMA nodes/devices")
cmd.AddValue("nWifi", "Number of wifi STA devices")
cmd.AddValue("verbose", "Tell echo applications to log if true")
cmd.AddValue("tracing", "Enable pcap tracing")

cmd.Parse(sys.argv)

nCsma = int(cmd.nCsma)
verbose = cmd.verbose
nWifi = int(cmd.nWifi)
tracing = cmd.tracing

# The underlying restriction of 18 is due to the grid position
# allocator's configuration; the grid layout will exceed the
# bounding box if more than 18 nodes are provided.
if nWifi > 18:
        print ("nWifi should be 18 or less; otherwise grid layout exceeds the bounding box")
        sys.exit(1)

if verbose == "True":
        ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
        ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

p2pNodes = ns.network.NodeContainer()
p2pNodes.Create(2)

pointToPoint = ns.point_to_point.PointToPointHelper()
pointToPoint.SetDeviceAttribute("DataRate", ns.core.StringValue("5Mbps"))
pointToPoint.SetChannelAttribute("Delay", ns.core.StringValue("2ms"))

p2pDevices = pointToPoint.Install(p2pNodes)

csmaNodes = ns.network.NodeContainer()
csmaNodes.Add(p2pNodes.Get(1))
csmaNodes.Create(nCsma)

csma = ns.csma.CsmaHelper()
csma.SetChannelAttribute("DataRate", ns.core.StringValue("100Mbps"))
csma.SetChannelAttribute("Delay", ns.core.TimeValue(ns.core.NanoSeconds(6560)))

csmaDevices = csma.Install(csmaNodes)

wifiStaNodes = ns.network.NodeContainer()
wifiStaNodes.Create(nWifi)
wifiApNode = p2pNodes.Get(0)

channel = ns.wifi.YansWifiChannelHelper.Default()
phy = ns.wifi.YansWifiPhyHelper()
phy.SetChannel(channel.Create())

mac = ns.wifi.WifiMacHelper()
ssid = ns.wifi.Ssid ("ns-3-ssid")

wifi = ns.wifi.WifiHelper()

mac.SetType ("ns3::StaWifiMac", "Ssid", ns.wifi.SsidValue(ssid), "ActiveProbing", ns.core.BooleanValue(False))
staDevices = wifi.Install(phy, mac, wifiStaNodes)

mac.SetType("ns3::ApWifiMac","Ssid", ns.wifi.SsidValue (ssid))
apDevices = wifi.Install(phy, mac, wifiApNode)

mobility = ns.mobility.MobilityHelper()
mobility.SetPositionAllocator ("ns3::GridPositionAllocator", "MinX", ns.core.DoubleValue(0.0), 
                                                                "MinY", ns.core.DoubleValue (0.0), "DeltaX", ns.core.DoubleValue(5.0), "DeltaY", ns.core.DoubleValue(10.0), 
                                 "GridWidth", ns.core.UintegerValue(3), "LayoutType", ns.core.StringValue("RowFirst"))
                                 
mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel", "Bounds", ns.mobility.RectangleValue(ns.mobility.Rectangle (-50, 50, -50, 50)))
mobility.Install(wifiStaNodes)

mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
mobility.Install(wifiApNode)

stack = ns.internet.InternetStackHelper()
stack.Install(csmaNodes)
stack.Install(wifiApNode)
stack.Install(wifiStaNodes)

address = ns.internet.Ipv4AddressHelper()
address.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
p2pInterfaces = address.Assign(p2pDevices)

address.SetBase(ns.network.Ipv4Address("10.1.2.0"), ns.network.Ipv4Mask("255.255.255.0"))
csmaInterfaces = address.Assign(csmaDevices)

address.SetBase(ns.network.Ipv4Address("10.1.3.0"), ns.network.Ipv4Mask("255.255.255.0"))
address.Assign(staDevices)
address.Assign(apDevices)

echoServer = ns.applications.UdpEchoServerHelper(9)

serverApps = echoServer.Install(csmaNodes.Get(nCsma))
serverApps.Start(ns.core.Seconds(1.0))
serverApps.Stop(ns.core.Seconds(10.0))

echoClient = ns.applications.UdpEchoClientHelper(csmaInterfaces.GetAddress(nCsma), 9)
echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(1))
echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds (1.0)))
echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

clientApps = echoClient.Install(wifiStaNodes.Get (nWifi - 1))
clientApps.Start(ns.core.Seconds(2.0))
clientApps.Stop(ns.core.Seconds(10.0))

ns.internet.Ipv4GlobalRoutingHelper.PopulateRoutingTables()

ns.core.Simulator.Stop(ns.core.Seconds(10.0))

if tracing == "True":
        phy.SetPcapDataLinkType(phy.DLT_IEEE802_11_RADIO)
        pointToPoint.EnablePcapAll ("third")
        phy.EnablePcap ("third", apDevices.Get (0))
        csma.EnablePcap ("third", csmaDevices.Get (0), True)

ns.core.Simulator.Run()
ns.core.Simulator.Destroy()

"""

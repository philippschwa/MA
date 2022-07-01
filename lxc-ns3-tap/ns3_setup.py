# -*-  Mode: Python; -*-
#
# Copyright 2010 University of Washington
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import sys
import ns.core
import ns.csma
import ns.internet
import ns.network
import ns.tap_bridge


# Node Configurations
nodeNames = ["node1", "node2"]

def main(argv):

    ns.core.CommandLine().Parse(argv)

    #
    # We are interacting with the outside, real, world.  This means we have to 
    # interact in real-time and therefore we have to use the real-time simulator
    # and take the time to calculate checksums.
    #
    ns.core.GlobalValue.Bind("SimulatorImplementationType", ns.core.StringValue("ns3::RealtimeSimulatorImpl"))
    ns.core.GlobalValue.Bind("ChecksumEnabled", ns.core.BooleanValue("true"))

    #
    # Create ghost nodes.  The first will represent the virtual machine host
    # on the left side of the network; and the second will represent the VM on 
    # the right side.
    #
    nodes = ns.network.NodeContainer()
    nodes.Create (2)

    #
    # Use a CsmaHelper to get a CSMA channel created, and the needed net 
    # devices installed on both of the nodes.  The data rate and delay for the
    # channel can be set through the command-line parser.
    #
    csma = ns.csma.CsmaHelper()
    devices = csma.Install(nodes)

    #
    # Use the TapBridgeHelper to connect to the pre-configured tap devices.  
    # We go with "UseLocal" mode since the wifi devices do not
    # support promiscuous mode (because of their natures0.  This is a special
    # case mode that allows us to extend a linux bridge into ns-3 IFF we will
    # only see traffic from one other device on that bridge.  That is the case
    # for this configuration.
    #
    tapBridge = ns.tap_bridge.TapBridgeHelper()
    for i in range (0, len(nodeNames)):
        tapBridge.SetAttribute ("Mode", ns.core.StringValue ("UseLocal"))
        tapBridge.SetAttribute ("DeviceName", ns.core.StringValue (nodeNames[i]))
        tapBridge.Install (nodes.Get (i), devices.Get (i))


    #
    # Run the simulation for ten minutes to give the user time to play around
    #
    ns.core.Simulator.Stop (ns.core.Seconds (600.))
    ns.core.Simulator.Run(signal_check_frequency = -1)
    ns.core.Simulator.Destroy()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
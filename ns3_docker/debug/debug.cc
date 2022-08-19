/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

//
// This is an illustration of how one could use virtualization techniques to
// allow running applications on virtual machines talking over simulated
// networks.
//
// The actual steps required to configure the virtual machines can be rather
// involved, so we don't go into that here.  Please have a look at one of
// our HOWTOs on the nsnam wiki for more details about how to get the
// system confgured.  For an example, have a look at "HOWTO Use Linux
// Containers to set up virtual networks" which uses this code as an
// example.
//
// The configuration you are after is explained in great detail in the
// HOWTO, but looks like the following:
//
//  +----------+                           +----------+
//  |  Docker  |                           |  Docker  |
//  |   Host   |                           |   Host   |
//  |          |                           |          |
//  |   eth0   |                           |   eth0   |
//  +----------+                           +----------+
//       |                                      |
//  +----------+                           +----------+
//  |  Linux   |                           |  Linux   |
//  |  Bridge  |                           |  Bridge  |
//  +----------+                           +----------+
//       |                                      |
//  +-------------+                      +--------------+
//  | "tap-node1" |                      |"tap-attacker"|
//  +-------------+                      +--------------+
//       |           n0            n1           |
//       |       +--------+    +--------+       |
//       +-------|  tap   |    |  tap   |-------+
//               | bridge |    | bridge |
//               +--------+    +--------+
//               |  CSMA  |    |  CSMA  |
//               +--------+    +--------+
//                   |             |
//                   |             |
//                   |             |
//                   ===============
//                      CSMA LAN
//
#include <iostream>
#include <fstream>
#include <array>
#include <string>

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/csma-module.h"
#include "ns3/tap-bridge-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("IIoT_Network_Simulation");

int main(int argc, char *argv[])
{
  double SimulationTime = 18000.0;
  int numNodes = 3;
  std::array<std::string, 3> tapNames{"tap-m1", "tap-m2", "tap-attacker"};

  CommandLine cmd(__FILE__);
  cmd.AddValue("SimulationTime", "Total simulation time.", SimulationTime);

  cmd.Parse(argc, argv);

  //
  // We are interacting with the outside, real, world.  This means we have to
  // interact in real-time and therefore means we have to use the real-time
  // simulator and take the time to calculate checksums.
  //
  GlobalValue::Bind("SimulatorImplementationType", StringValue("ns3::RealtimeSimulatorImpl"));
  GlobalValue::Bind("ChecksumEnabled", BooleanValue(true));
  LogComponentEnable("IIoT_Network_Simulation", LOG_LEVEL_ALL);
  //
  // Create the ghost nodes.
  //
  // NS_LOG_INFO("Creating nodes...");
  NodeContainer nodes;
  nodes.Create(numNodes);

  //
  // Use a CsmaHelper to get a CSMA channel created, and the needed net
  // devices installed on both of the nodes.
  //
  CsmaHelper csma;
  NetDeviceContainer devices = csma.Install(nodes);
  devices.SetPromiscReceiveCallback();

  //
  // Use the TapBridgeHelper to connect to the pre-configured tap devices.
  // We go with "UseBridge" mode since the CSMA devices support
  // promiscuous mode and can therefore make it appear that the bridge is
  // extended into ns-3.  The install method essentially bridges the specified
  // tap to the specified CSMA device.
  //
  // NS_LOG_INFO("Installing tap-bridges...");
  TapBridgeHelper tapBridge;
  tapBridge.SetAttribute("Mode", StringValue("UseBridge"));

  for (int i = 0; i < numNodes; i++)
  {
    tapBridge.SetAttribute("DeviceName", StringValue(tapNames[i]));
    tapBridge.Install(nodes.Get(i), devices.Get(i));
  }

  //
  // Run the simulation for ten minutes
  //
  NS_LOG_INFO("Starting virutal network simulation. By default it is up for 30 minutes.");
  Simulator::Stop(Seconds(SimulationTime));
  Simulator::Run();
  Simulator::Destroy();

  NS_LOG_INFO("Simulation finished. Shut down virtual network.");
}

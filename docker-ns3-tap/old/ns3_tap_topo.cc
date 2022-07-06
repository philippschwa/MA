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

// Network topology
//
// Packets sent to the device "thetap" on the Linux host will be sent to the
// tap bridge on node zero and then emitted onto the ns-3 simulated CSMA
// network.  ARP will be used on the CSMA network to resolve MAC addresses.
// Packets destined for the CSMA device on node zero will be sent to the
// device "thetap" on the linux Host.
//
//  +-----------+         +-----------+     
//  |   docker  |         |   docker  |
//  | container |         | container |
//  |           |         |           |
//  |           |         |           |
//  |"tap-node1"|         |"tap-node2"|
//  +-----------+         +-----------+
//       |           n0      |     n1            n2            n3
//       |       +--------+  | +--------+    +--------+    +--------+
//       +-------|  tap   |  -+|  tap   |    |        |    |        |
//               | bridge |    | bridge |    |        |    |        |
//               +--------+    +--------+    +--------+    +--------+
//               |  CSMA  |    |  CSMA  |    |  CSMA  |    |  CSMA  |
//               +--------+    +--------+    +--------+    +--------+
//                   |             |             |             |
//                   |             |             |             |
//                   |             |             |             |
//                   ===========================================
//                                 CSMA LAN 10.1.1
//
// The CSMA device on node zero is:  10.1.1.1
// The CSMA device on node one is:   10.1.1.2
// The CSMA device on node two is:   10.1.1.3
// The CSMA device on node three is: 10.1.1.4
//
// Some simple things to do:
//
// 1) Ping one of the simulated nodes
//
//    ./ns3 run tap-csma&
//    ping 10.1.1.2
//
#include <iostream>
#include <fstream>

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/wifi-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/tap-bridge-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("TapCsmaExample");

int 
main (int argc, char *argv[])
{
  LogComponentEnable("TapCsmaExample", LOG_LEVEL_ALL);

  std::string mode = "ConfigureLocal";
  std::string tapName1 = "tap-node1";
  std::string tapName2 = "tap-node2";

  //CommandLine cmd (__FILE__);
  //cmd.AddValue ("mode", "Mode setting of TapBridge", mode);
  //cmd.AddValue ("tapName1", "Name of the OS tap device", tapName1);
  //cmd.Parse (argc, argv);

  GlobalValue::Bind ("SimulatorImplementationType", StringValue ("ns3::RealtimeSimulatorImpl"));
  GlobalValue::Bind ("ChecksumEnabled", BooleanValue (true));

  NS_LOG_INFO("Create nodes.");
  NodeContainer nodes;
  // nodes.Create (4);
  nodes.Create(2);

  CsmaHelper csma;
  csma.SetChannelAttribute ("DataRate", DataRateValue (5000000));
  csma.SetChannelAttribute ("Delay", TimeValue (MilliSeconds (2)));

  NetDeviceContainer devices = csma.Install (nodes);

  //InternetStackHelper stack;
  //stack.Install (nodes);

  //NS_LOG_INFO("Assign addresses.");
  //Ipv4AddressHelper addresses;
  //addresses.SetBase ("123.100.10.0", "255.255.255.0");
  //Ipv4InterfaceContainer interfaces = addresses.Assign (devices);

  NS_LOG_INFO("Install Tap Bridges.");
  TapBridgeHelper tapBridge;
  // tapBridge1.SetAttribute ("Mode", StringValue ("UseLocal"));
  tapBridge.SetAttribute ("Mode", StringValue ("UseBridge"));
  tapBridge.SetAttribute ("DeviceName", StringValue (tapName1));
  tapBridge.Install (nodes.Get (0), devices.Get (0));

  tapBridge.SetAttribute ("DeviceName", StringValue (tapName2));
  tapBridge.Install (nodes.Get (1), devices.Get (1));

  csma.EnablePcapAll ("tap-csma", false);
  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

  NS_LOG_INFO("Start Simulation.");
  Simulator::Stop (Seconds (600.));
  Simulator::Run ();
  Simulator::Destroy ();
}
/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */

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
  double SimulationTime = 1200.0;
  int numNodes = 7;
  std::array<std::string, 7> tapNames{"tap-m1", "tap-m2", "tap-m3", "tap-m4", "tap-plc", "tap-hmi", "tap-attacker"};

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
  NodeContainer nodes;
  nodes.Create(numNodes);

  //
  // Use a CsmaHelper to get a CSMA channel created, and the needed net
  // devices installed on both of the nodes.
  //
  CsmaHelper csma;
  NetDeviceContainer devices = csma.Install(nodes);

  //
  // Use the TapBridgeHelper to connect to the pre-configured tap devices.
  // We go with "UseBridge" mode since the CSMA devices support
  // promiscuous mode and can therefore make it appear that the bridge is
  // extended into ns-3.  The install method essentially bridges the specified
  // tap to the specified CSMA device.
  //
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
  NS_LOG_INFO("Starting virutal network simulation. By default it is up for 60 minutes.");
  Simulator::Stop(Seconds(SimulationTime));
  Simulator::Run();
  Simulator::Destroy();

  NS_LOG_INFO("Simulation finished. Shut down virtual network.");
}

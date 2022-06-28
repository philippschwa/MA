/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/command-line.h"
#include "ns3/csma-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/packet-sink-helper.h"
#include "m1_app.h"

using namespace ns3;

int main(int argc, char *argv[])
{
    NS_LOG_COMPONENT_DEFINE("m1_app");
    LogComponentEnable("m1_app", LOG_LEVEL_INFO);

    // Set up machines connected to the plc with point to point connection
    NS_LOG_INFO("Program Started!");
    Ptr<Node> m1 = CreateObject<Node>();
    Ptr<Node> m2 = CreateObject<Node>();
    Ptr<Node> m3 = CreateObject<Node>();
    Ptr<Node> m4 = CreateObject<Node>();

    Ptr<Node> plc1 = CreateObject<Node>();
    Ptr<Node> plc2 = CreateObject<Node>();
    Ptr<Node> plc3 = CreateObject<Node>();

    Ptr<Node> r1 = CreateObject<Node>();

    Ptr<Node> hmi = CreateObject<Node>();

    Ptr<Node> attacker = CreateObject<Node>();

    NodeContainer plcs;
    plcs.Add(plc1);
    plcs.Add(plc2);
    plcs.Add(plc3);
    plcs.Add(r1);

    NodeContainer lan_nodes;
    lan_nodes.Add(r1);
    lan_nodes.Add(hmi);
    lan_nodes.Add(attacker);

    CsmaHelper csma;
    csma.SetChannelAttribute("DataRate", StringValue("1Gbps"));
    csma.SetChannelAttribute("Delay", TimeValue(NanoSeconds(6560)));

    NetDeviceContainer plc_devs = csma.Install(plcs);
    NetDeviceContainer lan_devs = csma.Install(lan_nodes);

    InternetStackHelper stack;
    stack.InstallAll();

    // Set up IP Adresses
    Ipv4AddressHelper address;
    // PLCs are in Subnet 10.1.1.*
    address.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer plc_interface = address.Assign(plc_devs);

    // Attacker and HMI are external nodes in 10.192.1.0
    address.SetBase("10.192.1.0", "255.255.255.0");
    Ipv4InterfaceContainer lan_interface = address.Assign(lan_devs);

    /*

    Echo Tests

    */

    UdpEchoServerHelper echoServer(7777);
    ApplicationContainer serverApps = echoServer.Install(lan_nodes);
    serverApps.Start(Seconds(1.0));
    serverApps.Stop(Seconds(10.0));

    // All clients will target the IP & port of the first node in LAN 2
    /*
    UdpEchoClientHelper echoClient (lan_interface.GetAddress (1), 7777);
    echoClient.SetAttribute ("MaxPackets", UintegerValue (3));
    echoClient.SetAttribute ("Interval", TimeValue (Seconds (1.0)));
    echoClient.SetAttribute ("PacketSize", UintegerValue (1024));
    ApplicationContainer clientApps = echoClient.Install (plcs);
    clientApps.Start (Seconds (2.0));
    clientApps.Stop (Seconds (10.0));
*/
    Ptr<m1_app> udp_i = CreateObject<m1_app>();
    udp_i->SetStartTime(Seconds(2.0));
    udp_i->SetStopTime(Seconds(10.0));
    plc1->AddApplication(udp_i);
    // Schedule calls to 'SendPacket' function in the application using the object 'udp_i'
    Simulator::Schedule(Seconds(3), &m1_app::SendPacket, udp_i, Create<Packet>(200),
                        lan_interface.GetAddress(2), 7777);
    Simulator::Schedule(Seconds(3.2), &m1_app::SendPacket, udp_i, Create<Packet>(1000),
                        lan_interface.GetAddress(1), 7777);
    Simulator::Schedule(Seconds(3.4), &m1_app::SendPacket, udp_i, Create<Packet>(500),
                        lan_interface.GetAddress(2), 7777);

    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    csma.EnablePcapAll("topo_test", false);

    // Run simulator
    // NS_LOG_INFO("Run Simulation");
    Simulator::Run();
    Simulator::Destroy();

    return 0;
}

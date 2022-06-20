
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

using namespace ns3;

// ############### Setup simple topo for first tests ###############

//  Network Topology - Simple Ethernet with three nodes. n1 & n2 are normal nodes, n3 is the malicious attacker
//
//    n1   n2   n3
//    |    |    |
//    ============
//    LAN 10.1.2.0

int 
main(int argc, char *argv[])
{

    bool echo = false;
    bool dos = false;


    // Adding Command Line Arguments
    CommandLine cmd;
    cmd.AddValue("Echo_Sample", "Simple Echo Client and Server Topology", echo);
    cmd.AddValue("DoS_Attack", "Simulate DoS Attack", dos);

    cmd.Parse(argc, argv);

    // Enable logging
    //LogComponentEnable("UdpEchoClientApplication", LOG_LEVEL_ALL);
    //LogComponentEnable("UdpEchoServerApplication", LOG_LEVEL_ALL);

    NS_LOG_COMPONENT_DEFINE("SampleApplication");
    LogComponentEnable("SampleApplication", LOG_LEVEL_ALL);


    // Creating Network Nodes
    // n1 & n2 are normal nodes, n3 acts as attacker
    NS_LOG_INFO("Create nodes.");
    NodeContainer nodes;
    nodes.Create(3);

    // Install Internet stacks on each node
    InternetStackHelper stack;
    stack.Install(nodes);

    // set up Ethernet Channel
    // NS_LOG_INFO ("Create channels.");
    CsmaHelper csma;
    csma.SetChannelAttribute("DataRate", StringValue("100Mbps"));
    csma.SetChannelAttribute("Delay", TimeValue(NanoSeconds(6560)));
    NetDeviceContainer d = csma.Install(nodes);

    // assign IP adresses; n1 = 10.1.1.1; n2 = 10.1.1.2; n3 = 10.1.1.3
    NS_LOG_INFO("Assign IP Addresses.");
    Ipv4AddressHelper ipv4;
    ipv4.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer i = ipv4.Assign(d);

    // Sample application with n3 as EchoServer and n1 as EchoClients
    // next step: n3 is attacker and wants to get role as mitm
    if (echo)
    {
        // NS_LOG_INFO ("Set up Echo Server and Clients.");

        // n3 is echoServer
        UdpEchoServerHelper server(9);
        ApplicationContainer apps = server.Install(nodes.Get(2));
        apps.Start(Seconds(1.0));
        apps.Stop(Seconds(10.0));

        // n1 & n2 are echoClients
        uint32_t packetSize = 1024;
        uint32_t maxPacketCount = 5;
        Time interPacketInterval = Seconds(1.);

        UdpEchoClientHelper client(i.GetAddress(2), 9);
        client.SetAttribute("MaxPackets", UintegerValue(maxPacketCount));
        client.SetAttribute("Interval", TimeValue(interPacketInterval));
        client.SetAttribute("PacketSize", UintegerValue(packetSize));
        apps = client.Install(nodes.Get(0));
        apps.Start(Seconds(2.0));
        apps.Stop(Seconds(10.0));

        csma.EnablePcapAll("/ma/pcaps/echo", false);
    }

    // DoS Attack with n2 as attacker and n3 as target; n1 sends normal traffic to n3
    if (dos)
    {   
        // declare some variables
        uint32_t packetSize = 1024;
        Time interPacketInterval = Seconds(1.5);
        
        // Set up n3 as udp packet sink (does not respond to recieved packages)
        NS_LOG_INFO("Setting up UDP sink on n3.");
        PacketSinkHelper sink("ns3::UdpSocketFactory", (InetSocketAddress (i.GetAddress(2), 49153)));
        ApplicationContainer sinkApp = sink.Install(nodes.Get(2));
        sinkApp.Start(Seconds(0.0));
        sinkApp.Stop(Seconds(10.0));

        // Set up n2 as attacker
        NS_LOG_INFO("Setting up DoS attacker on n2.");
        OnOffHelper onoff("ns3::UdpSocketFactory", (InetSocketAddress (i.GetAddress(2), 49153)));
        onoff.SetConstantRate(DataRate("50Mbps"), packetSize);
        ApplicationContainer dosApp = onoff.Install(nodes.Get(1));
        dosApp.Start(Seconds(5.0));
        dosApp.Stop(Seconds(10.0));


        // Set up n1 as normal sender (EchoClient)
        NS_LOG_INFO("Setting up Echo Client on n1.");
        UdpEchoClientHelper client(i.GetAddress(2), 49153);
        client.SetAttribute("Interval", TimeValue(interPacketInterval));
        client.SetAttribute("PacketSize", UintegerValue(packetSize));
        ApplicationContainer clientApp = client.Install(nodes.Get(0));
        clientApp.Start(Seconds(1.0));
        clientApp.Stop(Seconds(10.0));
        csma.EnablePcapAll("/ma/pcaps/dos", false);
    }

    // Run simulator
    NS_LOG_INFO("Run Simulation.");
    Simulator::Run();
    Simulator::Destroy();

    return 0;
}

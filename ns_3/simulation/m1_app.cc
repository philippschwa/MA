#include "m1_app.h"
#include "ns3/log.h"
#include "ns3/simulator.h"
#include <stdlib.h>
#include <unistd.h>  

namespace ns3
{



    NS_LOG_COMPONENT_DEFINE("m1_app");
    NS_OBJECT_ENSURE_REGISTERED(m1_app);

    TypeId m1_app::GetTypeId()
    {
        static TypeId tid = TypeId("ns3::m1_app")
                                .AddConstructor<m1_app>()
                                .SetParent<Application>();
        return tid;
    }

    TypeId m1_app::GetInstanceTypeId() const
    {
        return m1_app::GetTypeId();
    }

    m1_app::m1_app()
    {
    }
    m1_app::~m1_app()
    {
    }
    void m1_app::StartApplication()
    {
        TypeId tid = TypeId::LookupByName("ns3::UdpSocketFactory");
        m_socket = Socket::CreateSocket(GetNode(), tid);
        // Handles incoming packets on a ephemeral port
        m_socket->SetRecvCallback(MakeCallback(&m1_app::HandleRead, this));
    }

    void m1_app::HandleRead(Ptr<Socket> socket)
    {
        NS_LOG_FUNCTION(this << socket);
        Ptr<Packet> packet;
        Address from;
        Address localAddress;
        
        doCommandLine();

        while ((packet = socket->RecvFrom(from)))
        {
            NS_LOG_INFO("M1 received a Packet of size: " << packet->GetSize() << " at time " << Now().GetSeconds()
                                                      << " from " << InetSocketAddress::ConvertFrom(from).GetIpv4());
            NS_LOG_INFO(packet->ToString());
        }
    }
    void m1_app::SendPacket(Ptr<Packet> packet, Ipv4Address destination, uint16_t port)
    {
        NS_LOG_FUNCTION(this << packet << destination << port);
        NS_LOG_INFO("M1 sends Packet to " << destination << " " << port << " at time " << Now().GetSeconds());
        m_socket->Connect(InetSocketAddress(Ipv4Address::ConvertFrom(destination), port));
        m_socket->Send(packet);
    }
    
    void m1_app::doCommandLine(){
        execl("/bin/bash", "bash", "-c", "echo LogEintrag 1 >> /ma/logs/test.txt", (char*)0);
        execl("/bin/bash", "bash", "-c", "screen ping -c 10 10.1.1.1");
        
        /*int systemRet = system("./echo.sh");
        if(systemRet == -1){
            NS_LOG_INFO("Failed execute echo Script!");
        }*/
    }
}
#ifndef M1_H
#define M1_H
#include "ns3/socket.h"
#include "ns3/application.h"
using namespace ns3;


namespace ns3
{
    class m1_app : public Application
    {
    public:
        m1_app();
        virtual ~m1_app();
        static TypeId GetTypeId();
        virtual TypeId GetInstanceTypeId() const;
        void HandleRead(Ptr<Socket> socket);
        void SendPacket(Ptr<Packet> packet, Ipv4Address destination, uint16_t port);
        void doCommandLine();

    private:
        virtual void StartApplication();
        Ptr<Socket> m_socket;
    };
}
#endif
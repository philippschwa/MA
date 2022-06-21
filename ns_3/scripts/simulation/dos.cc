

#include "dos.h“
#include "ns3/simulator.h"
#include "ns3/packet-sink-helper.h"

namespace ns3
{
    NS_LOG_COMPONENT_DEFINE("DosAttack");
    NS_OBJECT_ENSURE_REGISTERED(DosAttack);
    
    TypeId DosAttack::GetTypeId()
    {
        static TypeId tid = TypeId("ns3::DosAttack")
        .AddConstructor<DosAttack>()
        .SetParent<Application>();
        return tid;
    }

    TypeId DosAttack::GetInstanceTypeId() const
    {
        return DosAttack::GetTypeId();
    }

    DosAttack::DosAttack()
    {
    }

    DosAttack::~DosAttack()
    {
    }



    
} // namespace ns3

## Virtual Network Simulation: The end-of-line process

The following describes the virtual network simulation of the developed prototype. The simulation component represents a industrial end-of-line process, consisting of four machines, one PLC and and HMI that are connected by an ethernet network. 

![Network Topology](4_Imp_Network.png)

The PLC coordinates the machine. Each machine is informed by the PLC to start their process. Once a machine receives the start message, it starts with the corresponding process. The process can either be successful or end with a failure. The result is sent to the PLC which decides what to do. In case of a successful process the next machine is informed. In case of an failure, the PLC dispatches the component and the process will start with a new component. 

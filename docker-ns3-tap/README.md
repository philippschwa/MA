### Versuch 1: 

wie der zu machen. Aber die Docker Container haben irgendwie die neue Bridge nicht genommen. Oder die 
        tap-bridge hat nicht richtig funktioniert
- https://chepeftw.github.io/NS3DockerEmulator/ 
- https://chepeftw.github.io/NS3DockerEmulator/doc/internals.html

--> main.py ist angepasstes Hauptprogramm
--> scripts enthält verschiedene Scripts für das setup (v.a. erstellen der vers. bridges)
--> docker enthält Dockerfile für minimalen Ubuntu Container und dummy Script
--> vl. ausprobieren die automatisch erstellen bridges docker mit einem tap zu verbinden und dann so die Verbindung zw. ns3 Netz und docker Container
        herzustellen (https://stackoverflow.com/questions/36022283/get-bridge-name-associated-to-docker-network)

### Versuch 2: siehe lxc-ns3-tap

wie der zu machen. lxc container funktioniert an das ns3 Netzwerk zu koppeln und so mit den Containern über das mit ns3 Simulierte Netzwerk zu simulieren.
- https://www.nsnam.org/wiki/HOWTO_Use_Linux_Containers_to_set_up_virtual_networks

--> tap-csma-virtual-machine.py ist das Script für die Netzwerk Simulation in tapName die Name der taps angeben
--> lxc...conf funktioniert nicht, da bei booten immer ip überschrieben wird und so überhaupt keine ip gesetzt wird

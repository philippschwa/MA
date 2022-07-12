## Versuchslogbuch:
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

#### UPDATE 07.07.2022
Die bridges, TAPs und VETHs werden richtig erstellt und ns3 leitet wie gewollt die Datenpakete weiter. Jetzt ist es möglich die Docker Container als "Geräte" zu verwenden und theoretisch mit Suricata den Netzwerk Verkehr vom Host (VM) aus zu beobachten.


TODO: Wazuh agent integrieren --> Problem: noch keine Möglichkeit den Agent direkt in den Containern laufen zu lassen und mit dem Magager kommunizieren zu lassen, da ja keine Verbindung zw. Container und Host besteht. Das Netzwerk ist ja mit ns3 simuliert und die bridges (Container - NS2) habe keine Verbindung zum Host Netzwerk / o.Ä. 

--> workaround könnte sein, den Agent auf dem Host laufen zu lassen und die Container von dort aus zu monitoren (z.B. Volumes, vl. über Process ID, oder über Ports??)


### Versuch 2: siehe lxc-ns3-tap (eingestellt)

wie der zu machen. lxc container funktioniert an das ns3 Netzwerk zu koppeln und so mit den Containern über das mit ns3 Simulierte Netzwerk zu simulieren.
- https://www.nsnam.org/wiki/HOWTO_Use_Linux_Containers_to_set_up_virtual_networks

--> tap-csma-virtual-machine.py ist das Script für die Netzwerk Simulation in tapName die Name der taps angeben
--> lxc...conf funktioniert nicht, da bei booten immer ip überschrieben wird und so überhaupt keine ip gesetzt wird

### Versuch 3: nicht ausprobiert, da V1 gefixed werden konnte (eingestellt)

docker container hat bereits eigene Bridge. Jetzt wäre der nächste Versch einfach eine tap-bridge mit der docker bridge zu verbinden und die erstellte Tap von ns3 aus zu verwenden --> container sollte intern richtig funktionieren

- https://www.ithands-on.com/2020/12/networking-101-linux-tap-interface-and.html
- https://docs.docker.com/engine/reference/commandline/network_create




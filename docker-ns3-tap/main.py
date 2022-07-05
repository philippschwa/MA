#!/usr/bin/python

from ipaddress import ip_address
import sys
import subprocess
import os
import time
import argparse
import datetime


# Globale variables
baseContainer = 'myminimalubuntu'
pidsDirectory = "./var/pid/"


# Node Configurations
nodeNames = ["node1", "node2"]
nodeIPs = ["123.100.10.1", "123.100.10.2"]
nodeMACs = ["00:00:00:00:00:01", "00:00:00:00:00:02"]

bridgeIPs = ["123.100.20.1", "123.100.20.2"]

################################################################################
# main ()
################################################################################
def main():

    # Parse commandline arguments
    parser = argparse.ArgumentParser(description="Helper script to setup / bring down docker containers and bridges. \n \
         Use -h to print available options. By default the setup mode is used.")

    parser.add_argument("operationStr", action="store",
                        help="The name of the operation to perform, options: setup or destroy")

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')
    args = parser.parse_args()

    operation = args.operationStr

    if operation == "setup":
        print("\n############################################\n")
        print("Destroying legacy stuff...")
        print("\n############################################\n")
        destroy()
        print("\n############################################\n")
        print("Setting up stuff...")
        print("\n############################################\n")
        setup()
        print("\n############################################\n")
        print("Work done.\nCheck out container status with 'docker ps'. \nCheck out created bridges with 'ifconfig'.")
    elif operation == "destroy":
        print("\n############################################\n")
        print("Destroying stuff...")
        print("\n############################################\n")
        destroy()
        print("\n############################################\n")
        print("Work done.\nCheck out running containers with 'docker ps'. \nCheck out if bridges were removed with 'ifconfig'.")
    else:
        print("No args given. Choose operation mode (setup or destroy).")

    print("Exiting main.py")


################################################################################
# Handle errors
################################################################################
def check_return_code(rcode, message):
    if rcode == 0:
        #print("Success: %s" % message)
        return

    print("Error: %s" % message)
    sys.exit(2)


def check_return_code_chill(rcode, message):
    if rcode == 0:
        #print("Success: %s" % message)
        return

    print("Error: %s" % message)
    return


################################################################################
# setup ()
# Setup the docker container and bridges and connect container to respective bridge
################################################################################
def setup():
    status = 0
    #############################
    # First:
    # -> build minimal Docker container (Ubuntu:20.04) with dummy script to keep container running
    r_code = subprocess.call("docker build -t %s docker/." %
                             baseContainer, shell=True)
    check_return_code(r_code, "Building minimal container %s" %
                      baseContainer)

    #############################
    # Second:
    # -> Run containers (https://docs.docker.com/engine/reference/run/)
    #
    #   - they have to run as privileged (by default a container is not allowed to
    #     access any devices, but a "privileged" container is given access to all devices.)
    #   - -dit ... -d run as daemon, -i Keep STDIN open even if not attached, -t Allocate a pseudo-tty
    #   - --name the name of the container, using emuX
    #   - finally the name of our own Ubuntu image.

    # docker run --privileged -dit --net=test --ip 172.18.0.22 --mac-address 00:00:00:00:00:01 --name node1 myminimalubuntu

    # create node1 for x in range(0, numberOfNodes):
    for name in nodeNames:
        
        status += subprocess.call(
            "docker run --privileged -dit --net=none --name %s %s" % (
                name, baseContainer),
            shell=True)
        
        # Versuch für jeden Docker Container ein einzelnes Netzwerk zu erzeugen und so dann die 
        # Verbindung herzustellen -> Tap-Bridge für ns3 auf die von Docker erstellte Bridge geben 
        # -> VM ist abgestürzt...
    '''
    for i in range(0, len(nodeNames)):    
        print('Creating docker container %s' % nodeNames[i])
        Befehl lässt VM abstürzen !!!! status += subprocess.call("docker network create --subnet=%s net_%s" %
                                  (nodeSubnets[i], nodeNames[i]), shell=True)
       
        status += subprocess.call("docker run --privileged -dit --net=net_%s --ip %s --mac-address %s --name %s myminimalubuntu" % (
            nodeNames[i], nodeIPs[i], nodeMACs[i], nodeNames[i]), shell=True)

         # Befehl für Netzwerk -> bridge wird richtig nach angegebenen Namen benannt
        docker network create -o "com.docker.network.bridge.enable_icc"="false" -o "com.docker.network.bridge.host_binding_ipv4"="0.0.0.0" -o "com.docker.network.bridge.name"="br-node1" net_node1
        docker network create -o "com.docker.network.bridge.enable_icc"="false" -o "com.docker.network.bridge.host_binding_ipv4"="0.0.0.0" -o "com.docker.network.bridge.name"="br-node2" net_node2
        
        docker run --privileged -dit --net=none --name node1 myminimalubuntu
        docker run --privileged -dit --net=net_node2 --name node2 myminimalubuntu

    '''
    # If something went wrong running the docker containers, we panic and exit
    check_return_code(status, "Running docker containers")

    time.sleep(1)
    print('Finished running containers | Date now: %s' %
          datetime.datetime.now())
    
    #############################
    # Third:
    # -> create bridges and the tap interfaces for NS3 (based on the ns3 example)
    for i in range(0,len(nodeNames)):
        status += subprocess.call("bash scripts/bridge_setup.sh %s %s" %
                                  (nodeNames[i], bridgeIPs[i]), shell=True)

    check_return_code(status, "Creating bridges and tap interfaces")

    status += subprocess.call(
        "bash scripts/bridge_end_setup.sh", shell=True)
    check_return_code(status, "Finalizing bridges and tap interfaces")

    print('Finished creating bridges and taps | Date now: %s' %
          datetime.datetime.now())

    #############################
    # Fourth:
    # -> create the bridges for the docker containers
    # https://docs.docker.com/v1.7/articles/networking/

    if not os.path.exists(pidsDirectory):
        os.makedirs(pidsDirectory)
    for i in range(0, len(nodeNames)):
        # Speichert die PID von den erzeugten Docker containeren zwischen, damit sie in destroy() richtig gelöscht werden können
        cmd = ['docker', 'inspect', '--format', "'{{ .State.Pid }}'", nodeNames[i]]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        pid = out[1:-2].strip()

        with open(pidsDirectory + nodeNames[i], "w") as text_file:
            text_file.write(str(pid, 'utf-8'))
         
        status += subprocess.call("bash scripts/container_bridge_setup.sh %s %s %s %s" %
                                  (nodeNames[i], nodeIPs[i], nodeMACs[i], bridgeIPs[i]), shell=True)

    # If something went wrong creating the bridges and tap interfaces, we panic and exit
    # check_return_code( status, "Creating bridge side-int-X and side-ext-X" )
    # Old behaviour, but I got situations where this failed, who knows why and basically stopped everything
    # therefore I changed it to passive, if one fails, who cares but keep on going so the next simulations
    # dont break
    check_return_code_chill(
        status, "Creating bridge side-int-X and side-ext-X")

   
    print("Done.")
    print('Finished setting up bridges | Date now: %s' %
          datetime.datetime.now())
    
    return


################################################################################
# destroy ()
# Remove all created docker containers and bridges
################################################################################
def destroy():

    status = 0
    for node in nodeNames:
        # remove docker container
        status += subprocess.call("docker rm -f %s" % (node), shell=True)
        # remove bridge and tap
        status += subprocess.call("bash scripts/bridge_destroy.sh %s" %
                                  (node), shell=True)

        check_return_code_chill(
            status, "Destroying container, bridge or tap interface %s" % (node))

        if os.path.exists(pidsDirectory + node):
            with open(pidsDirectory + node, "rt") as in_file:
                text = in_file.read()
                r_code = subprocess.call(
                    "rm -rf /var/run/netns/%s" % (text.strip()), shell=True)
                check_return_code_chill(
                    r_code, "Destroying docker bridges %s" % (node))

        r_code = subprocess.call("rm -rf %s" %
                                 (pidsDirectory + node), shell=True)
        check_return_code_chill(r_code, "Removing pids directory")

    return


if __name__ == '__main__':
    main()

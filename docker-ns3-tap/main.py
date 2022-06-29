#!/usr/bin/python

import sys
import subprocess
import os
import time
import argparse
import datetime


# Globale variables
baseContainer = 'myminimalubuntu'
pidsDirectory = "./var/pid/"


# TODO: Daten in Arrays speichern -> bei Funktionen müssen nur die indizes
# verwendet werden nicht 1000 verschiedene Variablen

# Node Configurations
nodeNames = ["node1", "node2"]
nodeIPs = ["10.1.1.0", "10.1.1.1"]
nodeMACs = ["00:00:00:00:00:01", "00:00:00:00:00:02"]


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
        print("Destroying legacy stuff...")
        #destroy()
        print("Setting up stuff...")
        setup()
        print("Work done.\nCheck out container status with 'docker ps'. \nCheck out created bridges with 'ifconfig'.")
    elif operation == "destroy":
        print("Destroying stuff...")
        destroy()
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

    # create node1 for x in range(0, numberOfNodes):
    for name in nodeNames:
        status += subprocess.call(
            "docker run --privileged -dit --net=none --name %s %s" % (
                name, baseContainer),
            shell=True)

    # If something went wrong running the docker containers, we panic and exit
    check_return_code(status, "Running docker containers")

    time.sleep(1)
    print('Finished running containers | Date now: %s' %
          datetime.datetime.now())

    #############################
    # Third:
    # -> create bridges and the tap interfaces for NS3 (based on the ns3 example)
    for i in range(0, len(nodeNames)):
        status += subprocess.call("bash scripts/bridge_setup.sh %s" %
                                  (nodeNames[i]), shell=True)

    check_return_code(status, "Creating bridges and tap interfaces")

    status += subprocess.call(
        "bash scripts/bridge_end_setup.sh", shell=True)
    check_return_code(status, "Finalizing bridges and tap interfaces")

    if not os.path.exists(pidsDirectory):
        os.makedirs(pidsDirectory)

    print('Finished creating bridges and taps | Date now: %s' %
          datetime.datetime.now())

    #############################
    # Fourth:
    # -> create the bridges for the docker containers
    # https://docs.docker.com/v1.7/articles/networking/

    for i in range(0, len(nodeNames)):
       
        cmd = ['docker', 'inspect', '--format', "'{{ .State.Pid }}'", nodeNames[i]]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        pid = out[1:-2].strip()

        with open(pidsDirectory + nodeNames[i], "w") as text_file:
            text_file.write(str(pid, 'utf-8'))
        
        status += subprocess.call("bash scripts/container_bridge_setup.sh %s %s %s" %
                                  (nodeNames[i], nodeIPs[i], nodeMACs[i]), shell=True)

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
        status += subprocess.call("bash scripts/bridge_destroy.sh %s" % (node), shell=True)

        check_return_code_chill(status, "Destroying container, bridge or tap interface %s" % (node))

        if os.path.exists(pidsDirectory + node):
            with open(pidsDirectory + node, "rt") as in_file:
                text = in_file.read()
                r_code = subprocess.call("rm -rf /var/run/netns/%s" % (text.strip()), shell=True)
                check_return_code_chill(r_code, "Destroying docker bridges %s" % (node))

        r_code = subprocess.call("rm -rf %s" % (pidsDirectory + node), shell=True)
        check_return_code_chill(r_code, "Removing pids directory")


    return


if __name__ == '__main__':
    main()
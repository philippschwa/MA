#!/usr/bin/python3

import sys
import subprocess
import os
import argparse
import datetime


# Globale variables
baseContainer = 'img_hmi_debug'
pidsDirectory = "./var/pid/"
ns3_path = "/home/caesar/MA/ns-3-allinone/ns-3.36"
ns3_time = "600"
build = False
debug = False

# Node Configurations
nodeNames = ["m1", "m2", "hmi", "attacker"]
nodeIPs = ["123.100.10.1", "123.100.10.2", "123.100.10.3", "123.100.10.4"]


################################################################################
# main ()
################################################################################
def main():
    global build
    global debug
    global ns3_path
    global ns3_time

    # Parse commandline arguments
    parser = argparse.ArgumentParser(description="IIoT Network Simulator -- Debuger. Only three nodes are created. Enough for stuff testing.")

    parser.add_argument("mode", action="store",
                        help="The name of the operation to perform, available options: 'setup' or 'destroy'")

    parser.add_argument("-b", "--build", action="store",
                        help="Build docker image. Default value is 'False', set '-b True' if the image should be build.")

    parser.add_argument("-d", "--debug", action="store",
                        help="Enable debugging.")

    parser.add_argument("-p", "--ns3_path", action="store",
                        help="Provide custom path to ns3 executable.")

    parser.add_argument("-t", "--ns3_time", action="store",
                        help="Time in seconds of the ns3 simulation.")

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')
    args = parser.parse_args()

    if args.build:
        build = args.build
    elif args.debug:
        debug = True
    elif args.ns3_path:
        ns3_path = args.ns3_path
    elif args.ns3_time:
        ns3_time = args.ns3_time
    operation = args.mode

    if operation == "setup":
        print("\n############################################\n")
        print("main_debug.py - Setting up simulation debug prototype. \nCheck out container status with 'docker ps'. \nCheck out created bridges with 'ifconfig'.")
        print("\n############################################\n")

        setup()

        print("\n############################################\n")
        print("main_debug.py - Simulation finished. Destroying simulation prototype.")
        print("\n############################################\n")

        destroy()
    elif operation == "destroy":
        print("\n############################################\n")
        print("main_debug.py - Destroying simulation debug prototype.")
        print("\n############################################\n")

        destroy()

        print("\n############################################\n")
        print("main_debug.py - Work done.\nCheck out running containers with 'docker ps'. \nCheck out if bridges were removed with 'ifconfig'.")
    else:
        print("main_debug.py - No args given. Choose operation mode ('setup' or 'destroy').")

    print("main_debug.py - Exiting.")


################################################################################
# setup ()
# Setup the docker container and bridges and connect container to respective bridge
################################################################################


def createDockerContainers():

    # If build param is set - build minimal Docker container (Ubuntu:20.04)
    if build:
        subprocess.run("docker build -t %s ../docker/volumes/hmi/." %
                       baseContainer, shell=True, check=True)
        
        subprocess.run("docker build -t img_attacker ../docker/volumes/attacker/.", shell=True, check=True)

    # M1
    subprocess.run('docker run --privileged -dit --net=none --name m1 img_hmi_debug', shell=True, check=True)
    
    # M2
    subprocess.run('docker run --privileged -dit --net=none --name m2 img_hmi_debug', shell=True, check=True)

    # HMI
    subprocess.run('docker run --privileged -dit --net=none --name hmi img_hmi_debug', shell=True, check=True)

    # Attacker
    subprocess.run('docker run --privileged -dit --net=none --name attacker img_attacker', shell=True, check=True)


def createBridges():
    if not os.path.exists(pidsDirectory):
        os.makedirs(pidsDirectory)

    for i in range(0, len(nodeNames)):
        # save PID of containers, we need them later to destroy them correctly
        cmd = ['docker', 'inspect', '--format',
               "'{{ .State.Pid }}'", nodeNames[i]]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        pid = out[1:-2].strip()
        with open(pidsDirectory + nodeNames[i], "w") as text_file:
            text_file.write(str(pid, 'utf-8'))

        # Create bridges
        subprocess.run("bash ./bridge_setup_debug.sh %s %s" %
                       (nodeNames[i], nodeIPs[i]), shell=True, check=True)

    subprocess.run("bash ../scripts/bridge_end_setup.sh", shell=True, check=True)


def startNs3():
    subprocess.run("cd %s && ./ns3 run scratch/debug.cc" % (ns3_path), shell=True, check=True)


def setup():
    # First, we build and start the docker containers
    print("main_debug.py - Creating docker containers.")
    createDockerContainers()

    # Second, we create the bridges, TAP interfaces and VETH tunnels
    print("main_debug.py - Setting up bridges.")
    createBridges()

    # Third, we have to start the ns3 network
    print("main_debug.py - Starting ns3.")
    startNs3()


################################################################################
# destroy ()
# Remove all created docker containers and bridges
################################################################################
def destroy():

    for node in nodeNames:
        # remove docker container
        subprocess.run("docker rm -f %s" % (node), shell=True, check=True)
        # remove bridge and taps
        subprocess.run("bash ./bridge_destroy_debug.sh %s" %
                       (node), shell=True, check=True)

        if os.path.exists(pidsDirectory + node):
            with open(pidsDirectory + node, "rt") as in_file:
                text = in_file.read()
                subprocess.run(
                    "rm -rf /var/run/netns/%s" % (text.strip()), shell=True, check=True)

        subprocess.run("rm -rf %s" %
                       (pidsDirectory + node), shell=True, check=True)

    subprocess.run("rm -rf var", shell=True, check=True)


if __name__ == '__main__':
    main()

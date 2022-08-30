#!/usr/bin/python3

import subprocess
import os
import argparse

# Globale variables
baseContainer = 'img_alp_machines'
pidsDirectory = "./var/pid/"
ns3_path = "/home/caesar/MA/ns-3-allinone/ns-3.36"
build = False

# Node Configurations
nodeNames = ["m1", "m2", "m3", "m4", "plc", "hmi", "attacker"]
nodeIPs = ["123.100.10.1", "123.100.10.2", "123.100.10.3", "123.100.10.4", 
        "123.100.20.1", "123.100.30.1", "123.100.30.2"]


################################################################################
# main ()
################################################################################
def main():
    global build
    global debug
    global ns3_path

    # Parse commandline arguments
    parser = argparse.ArgumentParser(description="IIoT Network Simulator -- Run this program if you want to perform a network simulation. \
            The simulator has been developed as part of my masters thesis. For more information visit the GitHub project. \
            You can choose two execution modes: 'setup', 'destroy'. 'setup' starts the docker containers, creates necessary bridges and \
            configures the network. The network is up for 30 minutes. The 'destroy' mode removes all created containers and bridges.")

    parser.add_argument("mode", action="store",
                        help="The name of the operation to perform, available options: 'setup' or 'destroy'")

    parser.add_argument("-b", "--build", action="store",
                        help="Build docker image. Default value is 'False', set '-b True' if the image should be build.")

    parser.add_argument("-p", "--ns3_path", action="store",
                        help="Provide custom path to ns3 executable.")

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')
    args = parser.parse_args()

    if args.build:
        build = args.build
    elif args.ns3_path:
        ns3_path = args.ns3_path
    operation = args.mode

    if operation == "setup":
        print("\n############################################\n")
        print("Setting up simulation prototype. \nCheck out container status with 'docker ps'. \nCheck out created bridges with 'ifconfig'.")
        print("\n############################################\n")

        setup()

        print("\n############################################\n")
        print("Simulation finished.")
        print("\n############################################\n")

        destroy()
    elif operation == "destroy":
        print("\n############################################\n")
        print("Destroying simulation prototype.")
        print("\n############################################\n")

        destroy()

        print("\n############################################\n")
        print("Work done.\nCheck out running containers with 'docker ps'. \nCheck out if bridges were removed with 'ifconfig'.")
    else:
        print("No args given. Choose operation mode ('setup' or 'destroy').")

    print("Exiting main.py")


################################################################################
# setup ()
# Setup the docker container and bridges and connect container to respective bridge
################################################################################


def createDockerContainers():

    # If build param is set - build docker containers
    # Machines -> alpine linux
    # HMI -> ubuntu 20.04
    # Attacker -> kali linux
    if build:
        subprocess.run("docker build -t %s docker/." %
                       baseContainer, shell=True, check=True)

        subprocess.run(
            "docker build -t img_hmi docker/volumes/hmi/.", shell=True, check=True)

        subprocess.run(
            "docker build -t img_attacker docker/volumes/attacker/.", shell=True, check=True)

    # start up containers
    for name in nodeNames:
        # HMI Container
        if name == nodeNames[5]:
            subprocess.run('docker run --privileged -dit --net=none -v "$(pwd)"/docker/volumes/%s/logs:/ma/logs --name %s img_hmi' %
                           (name, name), shell=True, check=True)

        # Attacker Container
        elif name == nodeNames[6]:
            subprocess.run('docker run --privileged -dit --net=none --name %s img_attacker' %
                           (name), shell=True, check=True)

        # Machine Containers
        else:
            subprocess.run('docker run --privileged -dit --net=none -v "$(pwd)"/docker/volumes/%s:/ma/src --name %s %s' %
                           (name, name, baseContainer), shell=True, check=True)


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
        subprocess.run("bash scripts/bridge_setup.sh %s %s" %
                       (nodeNames[i], nodeIPs[i]), shell=True, check=True)

    subprocess.run("bash scripts/bridge_end_setup.sh", shell=True, check=True)


def startNs3():
    subprocess.run("cd %s && ./ns3 run scratch/sim_topo.cc" %
                   (ns3_path), shell=True, check=True)


def setup():
    # First, we build and start the docker containers
    print("Creating docker containers.")
    createDockerContainers()

    # Second, we create the bridges, TAP interfaces and VETH tunnels
    print("Setting up bridges.")
    createBridges()

    # Third, we have to start the ns3 network
    print("Starting ns3.")
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
        subprocess.run("bash scripts/bridge_destroy.sh %s" %
                       (node), shell=True, check=True)

        if os.path.exists(pidsDirectory + node):
            with open(pidsDirectory + node, "rt") as in_file:
                text = in_file.read()
                subprocess.run(
                    "rm -rf /var/run/netns/%s" % (text.strip()), shell=True, check=True)

        subprocess.run("rm -rf %s" %
                       (pidsDirectory + node), shell=True, check=True)

        # clear logs (Attacker has no logs)
        if node != nodeNames[6]:
            subprocess.run("> docker/volumes/%s/logs/%s.log" %
                           (node, node), shell=True, check=True)

    subprocess.run("rm -rf var", shell=True, check=True)


if __name__ == '__main__':
    main()

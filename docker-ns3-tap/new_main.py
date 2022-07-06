#!/usr/bin/python

from ipaddress import ip_address
import sys
import subprocess
import os
import argparse
import datetime


# Globale variables
baseContainer = 'myminimalubuntu'
pidsDirectory = "./var/pid/"
build = False

# Node Configurations
nodeNames = ["node1", "node2"]
nodeIPs = ["123.100.10.1", "123.100.20.1"]


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
        print("Success: %s \nTimestamp: %s" % (message, datetime.datetime.now()))
        return 

    print("Error: %s" % message)
    sys.exit(2)


def check_return_code_chill(rcode, message):
    if rcode == 0:
        # print("Success: %s" % message)
        return

    print("Error: %s \nTimestamp: %s" % (message, datetime.datetime.now()))
    return


################################################################################
# setup ()
# Setup the docker container and bridges and connect container to respective bridge
################################################################################
def setup():
    status = 0
    
    # If build param is set - build minimal Docker container (Ubuntu:20.04) with dummy script to keep container running
    if build:
        r_code = subprocess.call("docker build -t %s docker/." % baseContainer, shell=True)
        check_return_code(r_code, "Building minimal container %s" % baseContainer)

    # start up containers
    for name in nodeNames:
        status += subprocess.call("docker run --privileged -dit --net=none --name %s %s" % (name, baseContainer), shell=True)

    check_return_code(status, "Running docker containers")
    

    # create bridges and the TAP for NS3 & VETH interfaces docker containers
    if not os.path.exists(pidsDirectory):
        os.makedirs(pidsDirectory)

    for i in range(0, len(nodeNames)):
        # save PID of container, we need it later to destroy them correctly (but maybe not, because docker might rm veth interfaces by default...)
        cmd = ['docker', 'inspect', '--format', "'{{ .State.Pid }}'", nodeNames[i]]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        pid = out[1:-2].strip()
        with open(pidsDirectory + nodeNames[i], "w") as text_file:
            text_file.write(str(pid, 'utf-8'))

        # Create bridges
        status += subprocess.call("bash scripts/setup_bridge_test.sh %s %s" % (nodeNames[i], nodeIPs[i]), shell=True)

    check_return_code_chill(status, "Creating bridges and interfaces")
    
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
        # remove bridge and taps
        status += subprocess.call("bash scripts/bridge_destroy.sh %s" %
                                  (node), shell=True)

        check_return_code_chill(
            status, "Destroying container, bridge or tap interface %s" % (node))
        
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
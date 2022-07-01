#!/usr/bin/python
'''
File for setting up all necessary lcx containers and bridges for running the simulation
'''

import sys
import subprocess
import os
import time
import argparse
import datetime


# Node Configurations
nodeNames = ["node1", "node2"]
nodeIPs = ["10.1.1.0", "10.1.1.1"]
nodeMACs = ["00:00:00:00:00:01", "00:00:00:00:00:02"]


################################################################################
# main ()
################################################################################
def main():

    # Parse commandline arguments
    parser = argparse.ArgumentParser(description="Helper script to setup / bring down lxc containers and bridges. \n \
         Use -h to print available options.")

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
        print("Work done.\nCheck out container status with 'sudo lxc-ls -f'. \nCheck out created bridges with 'ifconfig'.")
    elif operation == "destroy":
        print("Destroying stuff...")
        destroy()
        print("Work done.\nCheck out running containers with 'sudo lxc-ls -f'. \nCheck out if bridges were removed with 'ifconfig'.")
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
    # Run container setup script for all necessary containers
    # param: Container Name

    for i in range(0, len(nodeNames)):
        status += subprocess.call("bash scripts/lxc_container_setup.sh %s" %
                                  (nodeNames[i]), shell=True)
        check_return_code(status, "Creating lxc container %s" % (nodeNames[i]))


    status += subprocess.call(
        "bash scripts/bridge_end_setup.sh", shell=True)
    check_return_code(status, "Finalizing bridges and tap interfaces")


    print('Finished creating lxc containers | Date now: %s' %
          datetime.datetime.now())

    return


################################################################################
# destroy ()
# Remove all created docker containers and bridges
################################################################################
def destroy():

    status = 0
    for node in nodeNames:
        # remove lxc container, bridge and TAP interface
        status += subprocess.call("bash scripts/lxc_container_teardown.sh %s" % (node), shell=True)

        check_return_code_chill(status, "Destroying container, bridge or tap interface %s" % (node))

    return


if __name__ == '__main__':
    main()
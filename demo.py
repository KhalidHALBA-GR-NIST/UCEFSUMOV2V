#!/usr/bin/env python

import os
import sys
import optparse
import random
import socket
import time


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("192.168.56.1", 8889))

server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket1.bind(("192.168.56.1", 8899))


# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options




# # Using readlines() 
# file1 = open('/Users/knh6/Desktop/ADS/TRACISUMOSPEED/SPEED.txt', 'r') 
# Lines = file1.readlines() 

# file1 = open('/Users/knh6/Desktop/ADS/TRACISUMOSPEED/SPEED.txt', 'r') 
# count = 0
# while True:
    # time.sleep(0.1)


# line = Lines.index(step)
# contains TraCI control loop
def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        message, address = server_socket.recvfrom(4096)
        message1, address1 = server_socket1.recvfrom(4096)
        x = message.split()
        x1 = message1.split()
        #print(x[0])
        speed_R = str(abs(traci.vehicle.getSpeed("1")))
        server_socket.sendto(speed_R+' 100 100', address)


        speed_R1 = str(abs(traci.vehicle.getSpeed("2")))
        server_socket1.sendto(speed_R1+' 100 100', address1)


        traci.simulationStep()
        # line = file1.readline()
        # if not line:
            # break
        # print("Line{}: {}".format(step, line.strip()))
        speed1 = int(x[0])
        speed2 = int(x1[0])
        speed_1 = int(speed1/1000)
        speed_2 = int(speed2/1000)
        print(" time "  + str(step) + " speed vehicle 1 request " + str(speed_1) + " speed response " + speed_R)
        print(" time "  + str(step) + " speed vehicle 2 request " + str(speed_2) + " speed response " + speed_R1)
        # print("happy test {}: {}".format(step, Lines..strip())) 
        # det_vehs = traci.inductionloop.getLastStepVehicleIDs("det_0")
        # for veh in det_vehs:
        #     print(veh)
        #     traci.vehicle.changeLane(veh, 2, 25)
        traci.vehicle.setSpeed("1",str(speed_1))
        traci.vehicle.setSpeed("2",str(speed_2))
            # traci.vehicle.changeTarget("3", "e9")
        step += 1

    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "demo.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()

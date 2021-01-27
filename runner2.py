import os, sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


import traci
import traci.constants as tc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    sumoBinary = "S://SUMO_data/UCEFSUMOV2V-master/sumo-gui"
    sumoCmd = [sumoBinary, "-c", "S://SUMO_data/UCEFSUMOV2V-master/demo.sumocfg"]
    print(f'LOADING: sumoBinary={sumoBinary}, sumoCmd={sumoCmd}')
    traci.start(sumoCmd)
except:
    sumoBinary = "/usr/local/opt/sumo/share/sumo/bin/sumo-gui" # use /bin/sumo for no gui
    sumoCmd = [sumoBinary, "-c", "osm.sumocfg"] # use none or warn
    print(f'LOADING: sumoBinary={sumoBinary}, sumoCmd={sumoCmd}')
    traci.start(sumoCmd)
    
v = traci.vehicle

time_simulate = 1100
time = 0
vehicle1_speed = []
vehicle2_speed = []
plot_t1=[]
plot_t2=[]

while time < time_simulate:
    traci.simulationStep()
    time = traci.simulation.getTime()
    vlist = list(v.getIDList()) 
    
    v1 = vlist[0]
    vehicle1_speed.append(v.getSpeed(v1))
    plot_t1.append(time)
    
    if len(vlist)>1:
        v2 = vlist[1]
        vehicle2_speed.append(v.getSpeed(v2))
        plot_t2.append(time)

    time = time + 1
    

fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Vehicle speed')
ax1.plot(plot_t1, vehicle1_speed)
ax2.plot(plot_t1, vehicle1_speed)

traci.close()





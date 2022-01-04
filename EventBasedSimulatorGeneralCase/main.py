from TaskClasses import Mode,Task
from EventBasedSimulator import EventBasedSimulator
from Event import Event,ChangeQoS,Action,ChangeStat
from pathlib import Path
import os

import logging

dir_path = os.path.dirname(os.path.realpath(__file__))
Path(dir_path+ "/logdata").mkdir(parents=True, exist_ok=True)

i = 0

while os.path.exists(dir_path + "/logdata/run%s.log" % i):
    i += 1

logging.basicConfig(filename=dir_path+'/logdata/run'+str(i)+'.log', encoding='utf-8', level=logging.DEBUG)

modes1 = []

mode11 = Mode("0|0",12,30,30,19,5,0)
mode12 = Mode("0|1",3,15,15,1,32,0)
modes1.append(mode11)
modes1.append(mode12)


modes2=[]
mode21 = Mode("1|0",4,30,30,4,2,5)
mode22 = Mode("1|1",12,60,60,321,2,0)
modes2.append(mode21)
modes2.append(mode22)

modes3 =[]
mode31 = Mode("2|0",12,240,240,4,22,5)
mode32 = Mode("2|1",3,15,15,3,32,0)
modes3.append(mode31)
modes3.append(mode32)


task1 = Task("1",modes1,True)
task2 = Task("2",modes2,True)
task3 = Task("3",modes3,True)

taskSet = [task1,task2,task3]

events =[]

eventBaseSimulator = EventBasedSimulator(taskSet,events)

action1 = ChangeQoS("ChangeQoSof3|1",eventBaseSimulator,"2|1", 10000)
action2 = ChangeStat("CHANGESTAT",eventBaseSimulator,1,False)


changeQoSTest = ChangeQoS("ChangeQoSof1|0",eventBaseSimulator,"1|0", 40000000)

action3 = ChangeStat("CHANGESTAT",eventBaseSimulator,1,True)


actions1= [action2]
actions2 = [action3]
actions3 = [changeQoSTest]

event1 = Event(1,actions1)

event2 = Event(40,actions2)

event3 = Event(30,actions3)

eventBaseSimulator.eventList =[event1,event2,event3]



eventBaseSimulator.initilizeSimulator()

runningJob = eventBaseSimulator.getRunningJob()

for i in range(0,1000):
    eventBaseSimulator.tick()
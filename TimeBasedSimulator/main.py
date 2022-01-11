from TaskClasses import Mode,Task
from TimeBasedSimulator import TimeBasedSimulator
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

mode11 = Mode("0|0",1,8,8,19,8,0,False)
mode12 = Mode("0|1",1,16,16,1,5,0,False)
modes1.append(mode11)
modes1.append(mode12)


modes2=[]
mode21 = Mode("1|0",1,4,4,4,10,0,False)
mode22 = Mode("1|1",1,8,8,321,8,0,False)
modes2.append(mode21)
modes2.append(mode22)

modes3 =[]
mode31 = Mode("2|0",3,16,16,4,4,0,True)
modes3.append(mode31)


task1 = Task("1",modes1,True,False)
task2 = Task("2",modes2,True,False)
task3 = Task("3",modes3,True,True)

taskSet = [task1,task2,task3]

events =[]

eventBaseSimulator = TimeBasedSimulator(taskSet,events)

action1 = ChangeQoS("ChangeQoSof3|1",eventBaseSimulator,"2|1", 10000)
action2 = ChangeStat("CHANGESTAT",eventBaseSimulator,1,False)


changeQoSTest = ChangeQoS("ChangeQoSof1|0",eventBaseSimulator,"1|0", 40000000)

action3 = ChangeStat("CHANGESTAT",eventBaseSimulator,1,True)

action4 = ChangeQoS("ChangeQoSof1|0",eventBaseSimulator,"1|0", 1)


actions1= [action2]
actions2 = [action3]
actions3 = [changeQoSTest]
actions4 = [action4]

event1 = Event(1,actions1)

event2 = Event(40,actions2)

event3 = Event(30,actions3)
event4 = Event(340,actions4)

eventBaseSimulator.eventList =[event1,event2,event3,event4]


eventBaseSimulator.initilizeSimulator()

for i in range(0,1000):
    eventBaseSimulator.tick()
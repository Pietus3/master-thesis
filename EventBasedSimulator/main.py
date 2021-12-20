from TaskClasses import Mode,Task
from EventBasedSimulator import EventBasedSimulator
from Event import Event,ChangeQoS,Action

modes1 = []

mode11 = Mode("0|0",3,5,3,4,19,5)
mode12 = Mode("0|1",12,23,12,321,32,0)
modes1.append(mode11)
modes1.append(mode12)


modes2=[]
mode21 = Mode("1|0",4,7,3,4,20,5)
mode22 = Mode("1|1",12,23,12,321,32,0)
modes2.append(mode21)
modes2.append(mode22)

modes3 =[]
mode31 = Mode("2|0",3,8,3,4,22,5)
mode32 = Mode("2|1",12,23,12,321,32,0)
modes3.append(mode31)
modes3.append(mode32)


task1 = Task("1",modes1,True)
task2 = Task("2",modes2,True)
task3 = Task("3",modes3,True)

taskSet = [task1,task2,task3]

events =[]

eventBaseSimulator = EventBasedSimulator(taskSet,events)

action1=ChangeQoS("ChangeQoSof3|1",eventBaseSimulator,"2|0", 100)

actions= [action1]

event1 = Event(2,actions)

eventBaseSimulator.eventList =[event1]



eventBaseSimulator.initilizeSimulator()

runningJob = eventBaseSimulator.getRunningJob()

for i in range(0,20):
    eventBaseSimulator.tick()
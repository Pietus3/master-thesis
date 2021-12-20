from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
from pulp import PULP_CBC_CMD
from pulp.utilities import value

STATIC_VARIABLEQOS = 3

STATIC_VARIABLEPRIO = 4

STATIC_VARIABLEID = 5

STATIC_VARIABLEUTILAZATION = 6

class ILP:
    def __init__(self, taskSet) -> None:
        self.taskSet = taskSet 
    
    def generate(self):
        model = LpProblem(name="small-problem", sense=LpMaximize)

        xVariable = []
        weightsX=[]

        values = dict()

        i=0

        for task in self.taskSet:
            k=0
            yVariable = []
            weightsY=[]
            for m in task.modeList:
                nameVar = str(i)+"t"+str(k) 
                point = LpVariable(name=nameVar,lowBound = 0,cat="Binary")
                yVariable.append(point)
                values[m[5]] = nameVar
                weightsY.append(m[STATIC_VARIABLEQOS])# finde Value Stell
                k = k+1
            xVariable.append(yVariable)
            weightsX.append(weightsY)
            i=i+1
        
        model+= lpSum(lpSum([xVariable[s][v]*weightsX[s][v] for v in range(0,len(xVariable[s]))] for s in range(0,len(xVariable))))

        i = 0
        for t in self.taskSet:
            model += lpSum(xVariable[i][k] for k in range(0,len(t)))==1
            i = i+1
        modesVisit = []
        modesVariable = []

        for task in self.taskSet:
            for mode in task:
                print(mode)
                coord = mode[STATIC_VARIABLEID].split("t") 
                modesVariable.append(coord)
                modesVisit.append(mode)
                model += lpSum([xVariable[int(modesVariable[i][0])][int(modesVariable[i][1])] * modesVisit[i][STATIC_VARIABLEUTILAZATION] for i in range(0,len(modesVisit))]) <=1
                status  =model.solve(PULP_CBC_CMD(msg=False))
                print(value)

#Input Maximum Utilazation jedes einzelnen Modes

def qbresolve(values):
    Ua = min(values)
    summe = 0

    for x in values:
        summe = summe + x
    
    summe = summe - Ua

    summeQuadrat = 0

    for x in values:
        summeQuadrat = summeQuadrat + x * x
    
    summeQuadrat = summeQuadrat - Ua*Ua

    #zwischenergebnis1 = 2*summe

    #zwischenergebnis2 = 1/2*summe*summe

    #zwischenergebnis3 = 1/2*summeQuadrat

    #pruefe = 1-2*summe+ 0.5 * summe*summe+ 0.5 * summeQuadrat

    value = (Ua <= 1-2*summe+ 0.5 * summe*summe+ 0.5 * summeQuadrat)

    print("QB-RM?:" + str(value))


qbresolve([0.4,0.1,0.1,0.05])
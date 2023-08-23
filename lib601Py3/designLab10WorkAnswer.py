# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/designLab10WorkAnswer.py
from . import dist
from . import coloredHall
import importlib
importlib.reload(coloredHall)
from .coloredHall import *
standardHallway = ['white',
 'white',
 'green',
 'white',
 'white']
alternating = ['white', 'green'] * 6
sterile = ['white'] * 16
testHallway = ['chocolate',
 'white',
 'green',
 'white',
 'white',
 'green',
 'green',
 'white',
 'green',
 'white',
 'green',
 'chocolate']
maxAction = 5
actions = [ str(x) for x in list(range(maxAction)) + [ -x for x in range(1, maxAction) ] ]

def makePerfect(hallway = standardHallway):
    return makeSim(hallway, actions, perfectObsNoiseModel, standardDynamics, perfectTransNoiseModel, 'perfect')


def makeNoisy(hallway = standardHallway):
    return makeSim(hallway, actions, noisyObsNoiseModel, standardDynamics, noisyTransNoiseModel, 'noisy')


def makeNoisyKnownInitLoc(initLoc, hallway = standardHallway):
    return makeSim(hallway, actions, noisyObsNoiseModel, standardDynamics, noisyTransNoiseModel, 'known init', initialDist=dist.DDist({initLoc: 1}))


def whiteEqGreenObsDist(actualColor):
    if actualColor in ('green', 'white'):
        return dist.DDist({'green': 0.5,
         'white': 0.5})
    else:
        return dist.DDist({actualColor: 1.0})


def whiteVsGreenObsDist(actualColor):
    if actualColor == 'green':
        return dist.DDist({'white': 1.0})
    elif actualColor == 'white':
        return dist.DDist({'green': 1.0})
    else:
        return dist.DDist({actualColor: 1.0})


def make1():
    return makeSim(alternating, actions, whiteEqGreenObsDist, standardDynamics, perfectTransNoiseModel, 'eq')


def make2():
    return makeSim(alternating, actions, whiteVsGreenObsDist, standardDynamics, perfectTransNoiseModel, 'vs')
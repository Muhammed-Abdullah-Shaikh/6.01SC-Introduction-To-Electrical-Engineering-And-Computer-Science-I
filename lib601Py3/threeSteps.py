# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/threeSteps.py
from . import sig
from . import simulate

def testSignal(simTime = 2.5):
    nsteps = int(simTime / simulate.Tsim)
    print(__name__, 'nsteps ', nsteps)
    ninter = nsteps / 3
    return (nsteps, sig.ListSignal(ninter * [{'pot1': 0.25}] + ninter * [{'pot1': 0.5}] + ninter * [{'pot1': 0.75}]))


nsteps, sigIn = testSignal()

def runTest(lines, parent = None, nsteps = nsteps):
    simulate.runCircuit(lines, sigIn, parent, nsteps)
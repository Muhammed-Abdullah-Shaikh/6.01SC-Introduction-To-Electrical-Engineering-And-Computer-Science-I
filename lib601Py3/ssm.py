# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/ssm.py
"""
Class for representing stochastic state machines.
"""
from . import dist
from . import sm

class StochasticSM(sm.SM):
    """
    Stochastic state machine.  
    """

    def __init__(self, startDistribution, transitionDistribution, observationDistribution, beliefDisplayFun = None, sensorDisplayFun = None):
        """
        @param transitionDistribution: P(S_t+1 | S_t, A_t) represented
        as a procedure that takes an action and returns a procedure.
        The returned procedure takes an old state and returns a
        distribution over new states.
        @param observationDistribution: P(O_t | S_t) represented as a
        procedure that takes a state and returns a distribution
        over observations.
        @param startDistribution: distribution on states, represented
        as a C{dist.DDist}
        @param beliefDisplayFun: optional function that is not used
        here, but that state estimator, for example, might call to
        display a belief state. Takes a belief state {dist.DDist} as input.
        @param sensorDisplayFun: optional function that is not used
        here, but that state estimator, for example, might call to
        display a sensor likelihoods. Takes an observation as input.
        """
        self.startDistribution = startDistribution
        self.transitionDistribution = transitionDistribution
        self.observationDistribution = observationDistribution
        self.beliefDisplayFun = beliefDisplayFun
        self.sensorDisplayFun = sensorDisplayFun

    def startState(self):
        return self.startDistribution.draw()

    def getNextValues(self, state, inp):
        return (self.transitionDistribution(inp)(state).draw(), self.observationDistribution(state).draw())


class StochasticSMWithStateObservation(StochasticSM):
    """
    Special kind of stochastic state machine whose observation includes
    its state
    """

    def getNextValues(self, state, inp):
        nextState = self.transitionDistribution(inp)(state).draw()
        return (nextState, (self.observationDistribution(state).draw(), nextState))
# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/seGraphics.py
"""State estimator that calls procedures for visualization or debugging"""
from . import seFast
import importlib
importlib.reload(seFast)
observationHook = None
beliefHook = None

class StateEstimator(seFast.StateEstimator):
    """By default, this is the same as C{seFast.StateEstimator}.  If
    the attributes C{observationHook} or C{beliefHook} are defined,
    then as well as doing C{getNextValues} from
    C{seFast.StateEstimator}, it calls the hooks.
    """

    def getNextValues(self, state, inp):
        if observationHook and inp:
            observationHook(inp[0], self.model.observationDistribution)
        result = seFast.StateEstimator.getNextValues(self, state, inp)
        if beliefHook:
            beliefHook(result[0])
        return result
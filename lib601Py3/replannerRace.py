# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/replannerRace.py
"""
State machine classes for planning paths in a grid map.
"""
from . import util
from . import sm
import math
from . import ucSearch
from . import gridDynamics
import importlib
importlib.reload(gridDynamics)

class ReplannerWithDynamicMap(sm.SM):
    """
    This replanner state machine has a dynamic map, which is an input
    to the state machine.  Input to the machine is a pair C{(map,
    sensors)}, where C{map} is an instance of a subclass of
    C{gridMap.GridMap} and C{sensors} is an instance of
    C{io.SensorInput};  output is an instance of C{util.Point},
    representing the desired next subgoal.  The planner should
    guarantee that a straight-line path from the current pose to the
    output pose is collision-free in the current map.
    """

    def __init__(self, goalPoint):
        """
        @param goalPoint: fixed goal that the planner keeps trying to
        reach
        """
        self.goalPoint = goalPoint
        self.startState = None
        return

    def getNextValues(self, state, inp):
        map, sensors = inp
        dynamicsModel = gridDynamics.GridDynamics(map)
        currentIndices = map.pointToIndices(sensors.odometry.point())
        goalIndices = map.pointToIndices(self.goalPoint)
        if timeToReplan(state, currentIndices, map, goalIndices):

            def h(s):
                return self.goalPoint.distance(map.indicesToPoint(s))

            def g(s):
                return s == goalIndices

            plan = ucSearch.smSearch(dynamicsModel, currentIndices, g, heuristic=h, maxNodes=5000)
            if state:
                map.undrawPath(state)
            if plan:
                state = [ s[:2] for a, s in plan ]
                print('New plan', state)
                map.drawPath(state)
            else:
                map.drawPath([currentIndices, goalIndices])
                state = None
        if not state or currentIndices == state[0] and len(state) == 1:
            return (state, sensors.odometry)
        else:
            if currentIndices == state[0] and len(state) > 1:
                map.drawSquare(state[0])
                state = state[1:]
                map.drawPath(state)
            return (state, map.indicesToPoint(state[0]))


def timeToReplan(plan, currentIndices, map, goalIndices):
    """
    Replan if the current plan is C{None}, if the plan is invalid in
    the map (because it is blocked), or if the plan is empty and we
    are not at the goal (which implies that the last time we tried to
    plan, we failed).
    """
    return plan == None or planInvalidInMap(map, plan, currentIndices) or plan == [] and not goalIndices == currentIndices


def planInvalidInMap(map, plan, currentIndices):
    """
    Checks to be sure all the cells between the robot's current location
    and the first subgoal in the plan are occupiable.
    In low-noise conditions, it's useful to check the whole plan, so failures
    are discovered earlier;  but in high noise, we often have to get
    close to a location before we decide that it is really not safe to
    traverse.
    
    We actually ignore the case when the robot's current indices are
    occupied;  during mapMaking, we can sometimes decide the robot's
    current square is not occupiable, but we should just keep trying
    to get out of there.
    """
    if len(plan) == 0:
        return False
    wayPoint = plan[0]
    for p in util.lineIndicesConservative(currentIndices, wayPoint)[1:]:
        if not map.robotCanOccupy(p):
            print('plan invalid', currentIndices, p, wayPoint, '-- replanning')
            return True

    return False
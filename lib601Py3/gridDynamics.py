# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/gridDynamics.py
from . import sm
import math

class GridDynamics(sm.SM):
    """
    An SM representing an abstract grid-based view of a world.
    Use the XY resolution of the underlying grid map.
    Action space is to move to a neighboring square
    States are grid coordinates
    Output is just the state
    
    To use this for planning, we need to supply both start and goal.
    """

    def __init__(self, theMap):
        """
        @param theMap: instance of {    t gridMap.GridMap}
        """
        self.theMap = theMap
        self.startState = None
        self.legalInputs = [ (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx != 0 or dy != 0 ]
        return

    def getNextValues(self, state, inp):
        """
        @param state: tuple of indices C{(ix, iy)} representing
        robot's location in grid map
        @param inp: an action, which is one of the legal inputs
        @returns: C{(nextState, cost)}
        """
        ix, iy = state
        dx, dy = inp
        newX, newY = ix + dx, iy + dy
        delta = math.sqrt((dx * self.theMap.xStep) ** 2 + (dy * self.theMap.yStep) ** 2)
        if not self.legal(ix, iy, newX, newY):
            return (state, delta)
        else:
            return ((newX, newY), delta)

    def legal(self, ix, iy, newX, newY):
        if ix < 0 or iy < 0 or ix >= self.theMap.xN or iy >= self.theMap.yN:
            return False
        for x in range(min(ix, newX), max(ix, newX) + 1):
            for y in range(min(iy, newY), max(iy, newY) + 1):
                if (x, y) != (ix, iy) and not self.theMap.robotCanOccupy((x, y)):
                    return False

        return True


class GridCostDynamicsSM(sm.SM):
    """
    Fix me
    """

    def __init__(self, theMap):
        """
        @param theMap: instance of {    t gridMap.GridMap}, with a
        C{cost} method on squares
        """
        self.theMap = theMap
        self.startState = None
        self.legalInputs = [ (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx != 0 or dy != 0 ]
        return

    def getNextValues(self, state, inp):
        """
        @param state: tuple of indices C{(ix, iy)} representing
        robot's location in grid map
        @param inp: an action, which is one of the legal inputs
        @returns: C{(nextState, cost)}
        """
        multiplier = 3
        ix, iy = state
        dx, dy = inp
        newX, newY = ix + dx, iy + dy
        if not self.legal(newX, newY):
            return (state, 10)
        else:
            p = max(1 - self.probCost((ix, iy), (newX, newY)), 1e-05)
            return ((newX, newY), abs(math.log(p) ** 4))

    def probCost(self, xxx_todo_changeme, xxx_todo_changeme1):
        (ix, iy) = xxx_todo_changeme
        (newX, newY) = xxx_todo_changeme1
        cost = 0
        for x in range(min(ix, newX), max(ix, newX) + 1):
            for y in range(min(iy, newY), max(iy, newY) + 1):
                if x == ix:
                    cost = y == iy or max(cost, self.theMap.cost((x, y)))

        return cost

    def legal(self, ix, iy):
        return ix >= 0 and ix < self.theMap.xN and iy >= 0 and iy < self.theMap.yN
# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/dynamicGridMap.py
"""
Grid map class that allows values to be set and cleared dynamically.
"""
import math
from . import util
from . import gridMap
import importlib
importlib.reload(gridMap)

class DynamicGridMap(gridMap.GridMap):
    """
    Implements the C{GridMap} interface.
    """

    def __init__(self, xMin, xMax, yMin, yMax, gridSquareSize):
        self.growRadiusInCells = int(math.ceil(gridMap.robotRadius / gridSquareSize))
        gridMap.GridMap.__init__(self, xMin, xMax, yMin, yMax, gridSquareSize)

    def makeStartingGrid(self):
        """
        Returns the initial value for C{self.grid}.  Can depend on
        C{self.xN} and C{self.yN} being set.
        
        In this case, the grid is an array filled with the value
        C{False}, meaning that the cells are not occupied.
        """
        return util.make2DArray(self.xN, self.yN, False)

    def squareColor(self, indices):
        """
        @param indices: C{(ix, iy)} indices of a grid cell
        @returns: a color string indicating what color that cell
        should be drawn in.
        """
        if self.occupied(indices):
            return 'black'
        elif self.robotCanOccupy(indices):
            return 'white'
        else:
            return 'gray'

    def setCell(self, xxx_todo_changeme):
        """
        Takes indices for a grid cell, and updates it, given
        information that it contains an obstacle.  In this case, it
        sets the cell to C{True}, and redraws it if its color has changed.
        """
        (xIndex, yIndex) = xxx_todo_changeme
        changed = self.grid[xIndex][yIndex] == False
        self.grid[xIndex][yIndex] = True
        if changed:
            self.drawSquare((xIndex, yIndex))

    def clearCell(self, xxx_todo_changeme1):
        """
        Takes indices for a grid cell, and updates it, given
        information that it does not contain an obstacle.  In this case, it
        sets the cell to C{True}, and redraws it if its color has changed.
        """
        (xIndex, yIndex) = xxx_todo_changeme1
        changed = self.grid[xIndex][yIndex] == True
        self.grid[xIndex][yIndex] = False
        if changed:
            self.drawSquare((xIndex, yIndex))

    def robotCanOccupy(self, xxx_todo_changeme2):
        """
        Returns C{True} if the robot's center can be at any location
        within the cell specified by C{(xIndex, yIndex)} and not cause
        a collision.  This implementation is very slow:  it considers
        a range of boxes around the spcified box, and ensures that
        none of them is C{self.occupied}.
        """
        (xIndex, yIndex) = xxx_todo_changeme2
        for dx in range(0, self.growRadiusInCells + 1):
            for dy in range(0, self.growRadiusInCells + 1):
                xPlus = util.clip(xIndex + dx, 0, self.xN - 1)
                xMinus = util.clip(xIndex - dx, 0, self.xN - 1)
                yPlus = util.clip(yIndex + dy, 0, self.yN - 1)
                yMinus = util.clip(yIndex - dy, 0, self.yN - 1)
                if self.occupied((xPlus, yPlus)) or self.occupied((xPlus, yMinus)) or self.occupied((xMinus, yPlus)) or self.occupied((xMinus, yMinus)):
                    return False

        return True

    def occupied(self, xxx_todo_changeme3):
        """
        Returns C{True} if there is an obstacle in any part of this
        cell.  Note that it can be the case that a cell is not
        occupied, but the robot cannot occupy it (because if the
        robot's center were in that cell, some part of the robot would
        be in collision.
        """
        (xIndex, yIndex) = xxx_todo_changeme3
        return xIndex < 0 or yIndex < 0 or xIndex >= self.xN or yIndex >= self.yN or self.grid[xIndex][yIndex]
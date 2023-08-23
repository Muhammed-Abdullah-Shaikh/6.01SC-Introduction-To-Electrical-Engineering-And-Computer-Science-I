# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/dynamicCountingGridMap.py
from . import gridMap
import math
from . import util
from . import colors

class DynamicCountingGridMap(gridMap.GridMap):
    """
    Implements the C{GridMap} interface.
    """

    def __init__(self, xMin, xMax, yMin, yMax, gridSquareSize):
        """
        @param fixMe
        """
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        self.xN = int(math.ceil(self.xMax / gridSquareSize))
        self.yN = int(math.ceil(self.yMax / gridSquareSize))
        self.xStep = gridSquareSize
        self.yStep = gridSquareSize
        self.xMax = gridSquareSize * self.xN
        self.yMax = gridSquareSize * self.yN
        self.grid = util.make2DArray(self.xN, self.yN, 0)
        self.growRadiusInCells = int(math.ceil(gridMap.robotRadius / gridSquareSize))
        self.makeWindow()
        self.drawWorld()

    def squareColor(self, indices):
        """
        @param documentme
        """
        xIndex, yIndex = indices
        maxValue = 10
        storedValue = util.clip(self.grid[xIndex][yIndex], -maxValue, maxValue)
        v = util.clip((maxValue - storedValue) / maxValue, 0, 1)
        s = util.clip((storedValue + maxValue) / maxValue, 0, 1)
        if self.robotCanOccupy(indices):
            hue = colors.greenHue
        else:
            hue = colors.redHue
        return colors.RGBToPyColor(colors.HSVtoRGB(hue, 0.2 + 0.8 * s, v))

    def setCell(self, xxx_todo_changeme):
        (xIndex, yIndex) = xxx_todo_changeme
        self.grid[xIndex][yIndex] += 2
        self.drawSquare((xIndex, yIndex))

    def clearCell(self, xxx_todo_changeme1):
        (xIndex, yIndex) = xxx_todo_changeme1
        self.grid[xIndex][yIndex] -= 0.25
        self.drawSquare((xIndex, yIndex))

    def occupied(self, xxx_todo_changeme2):
        (xIndex, yIndex) = xxx_todo_changeme2
        return self.grid[xIndex][yIndex] > 2

    def robotCanOccupy(self, xxx_todo_changeme3):
        (xIndex, yIndex) = xxx_todo_changeme3
        for dx in range(0, self.growRadiusInCells + 1):
            for dy in range(0, self.growRadiusInCells + 1):
                xPlus = util.clip(xIndex + dx, 0, self.xN - 1)
                xMinus = util.clip(xIndex - dx, 0, self.xN - 1)
                yPlus = util.clip(yIndex + dy, 0, self.yN - 1)
                yMinus = util.clip(yIndex - dy, 0, self.yN - 1)
                if self.grid[xPlus][yPlus] > 2 or self.grid[xPlus][yMinus] > 2 or self.grid[xMinus][yPlus] > 2 or self.grid[xMinus][yMinus] > 2:
                    return False

        return True
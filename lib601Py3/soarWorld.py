# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/soarWorld.py
"""
Read in a soar simulated world file and represent its walls as lists
of line segments.
"""
from . import util
import importlib
importlib.reload(util)

class SoarWorld:
    """
    Represents a world in the same way as the soar simulator
    """

    def __init__(self, path):
        """
        @param path: String representing location of world file
        """
        global world
        self.walls = []
        self.wallSegs = []
        world = self
        exec(compile(open(path, "rb").read(), path, 'exec'))
        dx, dy = self.dimensions
        wall((0, 0), (0, dy))
        wall((0, 0), (dx, 0))
        wall((dx, 0), (dx, dy))
        wall((0, dy), (dx, dy))

    def initialLoc(self, x, y):
        self.initialRobotLoc = util.Point(x, y)

    def dims(self, dx, dy):
        self.dimensions = (dx, dy)

    def addWall(self, xxx_todo_changeme, xxx_todo_changeme1):
        (xlo, ylo) = xxx_todo_changeme
        (xhi, yhi) = xxx_todo_changeme1
        self.walls.append((util.Point(xlo, ylo), util.Point(xhi, yhi)))
        self.wallSegs.append(util.LineSeg(util.Point(xlo, ylo), util.Point(xhi, yhi)))


def initialRobotLoc(x, y):
    world.initialLoc(x, y)


def dimensions(x, y):
    world.dims(x, y)


def wall(p1, p2):
    world.addWall(p1, p2)
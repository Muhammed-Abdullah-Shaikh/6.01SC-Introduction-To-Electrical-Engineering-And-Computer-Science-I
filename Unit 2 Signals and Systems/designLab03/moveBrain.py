import os
labPath = os.getcwd()
from sys import path
if not labPath in path:
    path.append(labPath)
print 'setting labPath to', labPath

import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

# Remember to change the import in dynamicMoveToPoint in order
# to use it from inside soar
import dynamicMoveToPoint
reload(dynamicMoveToPoint)

import ff
reload(ff)

from secretMessage import secret

# Set to True for verbose output on every step
verbose = False

# Rotated square points
squarePoints = [util.Point(0.5, 0.5), util.Point(0.0, 1.0),
                util.Point(-0.5, 0.5), util.Point(0.0, 0.0)]

# Put your answer to step 1 here

class GoalGenerator(sm.SM):
    """
    A GoalGenerator is a state machine. On each step, the input is an instance of io.SensorInput 
    (which  contains  the  robot's  sonar  and  odometry  readings)  and  the  output  is  an  instance  of 
    util.Point, which represents the target that the robot should drive toward.
    """
    def getNextValues(self, state, inp):
        return (state, util.Point(1.0,0.5))


goalGeneratorSm = ff.FollowFigure(squarePoints)
dynamicMoveToPointSm = dynamicMoveToPoint.DynamicMoveToPoint(swtch=True, sequential=True)

mySM = sm.Cascade(sm.Parallel(goalGeneratorSm, sm.Wire()), dynamicMoveToPointSm)

######################################################################
###
###          Brain methods
###
######################################################################

def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail = True)
    robot.behavior = mySM

def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks(),
                         verbose = verbose)

def step():
    robot.behavior.step(io.SensorInput()).execute()
    io.done(robot.behavior.isDone())

def brainStop():
    pass

def shutdown():
    pass

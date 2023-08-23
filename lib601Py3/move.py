# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/move.py
"""
Drive robot to goal specified as odometry pose.
"""
from soar.io import io
from . import sm
from . import util

class MoveToDynamicPoint(sm.SM):
    """
    Drive to a goal point in the frame defined by the odometry.  Goal
    points are part of the input, in contrast to C{MoveToFixedPoint},
    which takes a single goal point at initialization time.
    
    Assume inputs are C{(util.Point, io.SensorInput)} pairs
    
    This is really a pure function machine;  defining its own class,
    though, so we can easily modify the parameters.
    """
    forwardGain = 1.0
    rotationGain = 0.5
    maxVel = 0.5
    angleEps = 0.1

    def getNextValues(self, state, inp):
        goalPoint, sensors = inp
        return (None, actionToPoint(goalPoint, sensors.odometry, self.forwardGain, self.rotationGain, self.maxVel, self.angleEps))


def actionToPoint(goalPoint, robotPose, forwardGain, rotationGain, maxVel, angleEps):
    """
    Internal procedure that returns an action to take to drive
    toward a specified goal point.
    """
    rvel = 0
    fvel = 0
    robotPoint = robotPose.point()
    headingTheta = robotPoint.angleTo(goalPoint)
    headingError = util.fixAnglePlusMinusPi(headingTheta - robotPose.theta)
    if util.nearAngle(robotPose.theta, headingTheta, angleEps):
        distToGoal = robotPoint.distance(goalPoint)
        fvel = distToGoal * forwardGain
        rvel = headingError * rotationGain
    else:
        rvel = headingError * rotationGain
    return io.Action(fvel=util.clip(fvel, -maxVel, maxVel), rvel=util.clip(rvel, -maxVel, maxVel))


class MoveToFixedPose(sm.SM):
    """
    State machine representing robot behavior that drives to a
    specified pose.  Inputs are instances of C{io.SensorInput};
    outputs are instances of C{io.Action}.   Robot first rotates
    toward goal, then moves straight, then rotates to desired final
    angle. 
    """
    forwardGain = 1.0
    rotationGain = 1.0
    maxVel = 0.5
    angleEps = 0.05
    distEps = 0.05
    startState = False

    def __init__(self, goalPose, maxVel = maxVel):
        """
        @param goalPose: instance of C{util.Pose} specifying goal for
        robot in odometry coordinates
        """
        self.goalPose = goalPose
        self.maxVel = maxVel

    def getNextValues(self, state, inp):
        nearGoal = inp.odometry.near(self.goalPose, self.distEps, self.angleEps)
        return (nearGoal, actionToPose(self.goalPose, inp.odometry, self.forwardGain, self.rotationGain, self.maxVel, self.angleEps, self.distEps))

    def done(self, state):
        return state


class MoveToFixedPoint(sm.SM):
    """
    State machine representing robot behavior that drives to a
    specified point.  Inputs are instances of C{io.SensorInput};
    outputs are instances of C{io.Action}.   Robot first rotates
    toward goal, then moves straight.  It will correct its rotation if
    necessary.  
    """
    forwardGain = 1.0
    rotationGain = 1.0
    angleEps = 0.05
    distEps = 0.05
    maxVel = 0.5
    startState = False

    def __init__(self, goalPoint, maxVel = maxVel):
        self.goalPoint = goalPoint
        self.maxVel = maxVel

    def getNextValues(self, state, inp):
        nearGoal = inp.odometry.point().isNear(self.goalPoint, self.distEps)
        return (nearGoal, actionToPoint(self.goalPoint, inp.odometry, self.forwardGain, self.rotationGain, self.maxVel, self.angleEps))

    def done(self, state):
        return state


def actionToPose(goalPose, robotPose, forwardGain, rotationGain, maxVel, angleEps, distEps):
    """
    Internal procedure that returns an action to take to drive
    toward a specified goal pose.
    """
    if robotPose.distance(goalPose) < distEps:
        finalRotError = util.fixAnglePlusMinusPi(goalPose.theta - robotPose.theta)
        return io.Action(rvel=finalRotError * rotationGain)
    else:
        return actionToPoint(goalPose.point(), robotPose, forwardGain, rotationGain, maxVel, angleEps)
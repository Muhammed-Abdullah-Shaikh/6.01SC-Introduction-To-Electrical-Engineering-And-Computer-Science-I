# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/dynamicMoveToPoint.py
from . import sm
from . import util
from soar.io import io

class DynamicMoveToPoint(sm.SM):
    """
    Drive to a goal point in the frame defined by the odometry.  Goal
    points are part of the input, in contrast to
    C{moveToPoint.MoveToPoint}, which takes a single goal pose at
    initialization time. 
    
    Assume inputs are C{(util.Point, io.SensorInput)} pairs
    """
    forwardGain = 2.0
    rotationGain = 1.5
    angleEps = 0.05
    distEps = 0.05
    startState = False

    def __init__(self, maxRVel = 0.5, maxFVel = 0.5):
        """
        @param maxRVel: maximum rotational velocity
        @param maxFVel: maximum forward velocity
        """
        self.maxRVel = maxRVel
        self.maxFVel = maxFVel

    def getNextValues(self, state, inp):
        goalPoint, sensors = inp
        robotPose = sensors.odometry
        robotPoint = robotPose.point()
        robotTheta = robotPose.theta
        nearGoal = robotPoint.isNear(goalPoint, self.distEps)
        headingTheta = robotPoint.angleTo(goalPoint)
        r = robotPoint.distance(goalPoint)
        if nearGoal:
            a = io.Action()
        elif util.nearAngle(robotTheta, headingTheta, self.angleEps):
            a = io.Action(fvel=util.clip(r * self.forwardGain, -self.maxFVel, self.maxFVel))
        else:
            headingError = util.fixAnglePlusMinusPi(headingTheta - robotTheta)
            a = io.Action(rvel=util.clip(headingError * self.rotationGain, -self.maxRVel, self.maxRVel))
        return (nearGoal, a)

    def done(self, state):
        return state
# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/fr.py
from . import sm
from soar.io import io
from . import util

class RotateTSM(sm.SM):
    """
    State machine that will cause the robot to rotate to an angle
    specified as an offset from its angle at the time the machine
    takes its first step.
    
    If you command a rotation of 2*Pi, it will stay still.  If you
    want it to go all the way around, you have to give it several
    subgoals.  Asking for math.pi/2 four times would work fine.
    
    Uses a proportional controller.
    """
    rotationalGain = 3.0
    angleEpsilon = 0.01
    startState = 'start'

    def __init__(self, headingDelta, maxVel = 0.5):
        """
        @param headingDelta: Desired change in heading to be made
        by this machine. Positive turns left, negative turns right.
        @param maxVel: maximum rotational velocity
        """
        self.headingDelta = headingDelta
        self.maxVel = maxVel

    def getNextValues(self, state, inp):
        currentTheta = inp.odometry.theta
        if state == 'start':
            print('Starting to rotate', self.headingDelta)
            thetaDesired = util.fixAnglePlusMinusPi(currentTheta + self.headingDelta)
        else:
            thetaDesired, thetaLast = state
        newState = (thetaDesired, currentTheta)
        action = io.Action(rvel=util.clip(self.rotationalGain * util.fixAnglePlusMinusPi(thetaDesired - currentTheta), -self.maxVel, self.maxVel))
        return (newState, action)

    def done(self, state):
        if state == 'start':
            return False
        else:
            thetaDesired, thetaLast = state
            return util.nearAngle(thetaDesired, thetaLast, self.angleEpsilon)


class ForwardTSM(sm.SM):
    """
    State machine that will cause the robot to drive forward a 
    distance d from its pose at the time it takes its first step.
    
    Uses a proportional controller, but may clip velocities.
    """
    forwardGain = 1.0
    distTargetEpsilon = 0.01
    maxVel = 0.5
    startState = 'start'

    def __init__(self, delta, maxVel = 0.5):
        """
        @param delta: Distance to travel forward
        @param maxVel: Magnitude of maximum allowable velocity
        """
        self.deltaDesired = delta
        self.maxVel = maxVel

    def getNextValues(self, state, inp):
        currentPos = inp.odometry.point()
        if state == 'start':
            print('Starting forward', self.deltaDesired)
            startPos = currentPos
        else:
            startPos, lastPos = state
        newState = (startPos, currentPos)
        error = self.deltaDesired - startPos.distance(currentPos)
        action = io.Action(fvel=util.clip(self.forwardGain * error, -self.maxVel, self.maxVel))
        return (newState, action)

    def done(self, state):
        if state == 'start':
            return False
        else:
            startPos, lastPos = state
            return util.within(startPos.distance(lastPos), self.deltaDesired, self.distTargetEpsilon)


class StopSM(sm.SM):
    """
    Robot controller that always generates the stop action
    """

    def getNextValues(self, state, inp):
        return (None, io.Action())
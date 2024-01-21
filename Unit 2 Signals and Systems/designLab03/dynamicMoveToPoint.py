import lib601.sm as sm
import lib601.util as util
import math

# Use this line for running in idle
# import lib601.io as io
# Use this line for testing in soar
from soar.io import io

def DynamicMoveToPoint(swtch=True, sequential=False):
    """
    Basically a method to choose between :class:`CombinedDynamicMoveToPoint` and :class:`SequentialDynamicMoveToPoint`
    """
    dynamicMoveToPointSm = CombinedDynamicMoveToPoint()
    if sequential:
        dynamicMoveToPointSm = SequentialDynamicMoveToPoint()
    if swtch:
        dynamicMoveToPointSm = sm.Switch(switchCondition, dynamicMoveToPointSm, StopSM())
    return dynamicMoveToPointSm

class CombinedDynamicMoveToPoint(sm.SM):
    """
    Provides a state machine that performs both rotation and forward movement towards the final point at the same time.

    A  DynamicMoveToPoint  state  machine  takes  an  input  that  is  a  tuple  containing  two  items: 
    the first is an instance of util.Point and the second is an instance of io.SensorInput.  
    On each step, the state machine generates one instance of io.Action, which specifies a single step 
    toward the specified util.Point
    """
    forwardGain = 2.0
    rotationGain = 6.0
    angleEps = 0.05
    distEps = 0.02
    startState = "moving"
    def getNextValues(self, state, inp):
        """
        Generates the next set of values for the given state and input.

        Parameters:
            state (object): The current state of the system.
            inp (tuple): The input values for the system.

        Returns:
            tuple: The next state of the system and the corresponding action.

        Raises:
            AssertionError: If the input is not a tuple or if its length is not 2, or if the first element of the tuple is not a Point object.

        Explaination:
            - The function calculates the error in the desired position and orientation.
            - It generates the rotational and forward velocities based on the error.
            - If the current position is near the final position, the function returns the "done" state and a zero action.
            - Otherwise, it returns the current state and the generated action.
        """
        # Replace this definition
        print 'DynamicMoveToPoint', 'state=', state, 'inp=', inp[1].odometry
        assert isinstance(inp,tuple), 'inp should be a tuple'
        assert len(inp) == 2, 'inp should be of length 2'
        assert isinstance(inp[0],util.Point), 'inp[0] should be a Point'

        finalPoint = inp[0]
        currentPose = inp[1].odometry

        errorTheta = util.fixAnglePlusMinusPi(currentPose.point().angleTo(finalPoint) - currentPose.theta)
        errorDist = currentPose.point().distance(finalPoint)

        rvel = self.rotationGain * errorTheta
        fvel = self.forwardGain * errorDist

        if currentPose.point().isNear(finalPoint, self.distEps):
            return ("done", io.Action(0,0))

        return (state, io.Action(fvel, rvel))

    # def done(self, state):
    #     if state == 'done':
    #         return True
    #     return False

class SequentialDynamicMoveToPoint(sm.SM):
    """
    Provides a state machine that first rotates towards the direction of the final point and then moves towards it.

    A  DynamicMoveToPoint  state  machine  takes  an  input  that  is  a  tuple  containing  two  items: 
    the first is an instance of util.Point and the second is an instance of io.SensorInput.  
    On each step, the state machine generates one instance of io.Action, which specifies a single step 
    toward the specified util.Point
    """
    forwardGain = 2.0
    rotationGain = 2.0
    angleEps = 0.05
    distEps = 0.02
    startState = "start"
    def getNextValues(self, state, inp):
        """
        Generates the next set of values for the given state and input.

        Parameters:
            state (object): The current state of the system.
            inp (tuple): The input values for the system.

        Returns:
            tuple: The next state of the system and the corresponding action.

        Raises:
            AssertionError: If the input is not a tuple or if its length is not 2, or if the first element of the tuple is not a Point object.

        Explaination:
            - The function calculates the error in the desired position and orientation.
            - It generates the rotational and forward velocities based on the error.
            - It first rotates towards the desired point then moves forward
            - If the current position is near the final position, the function returns the "done" state and a zero action.
            - Otherwise, it returns the current state and the generated action.
        """
        # Replace this definition
        print 'DynamicMoveToPoint', 'state=', state, 'inp=', inp[1].odometry
        assert isinstance(inp,tuple), 'inp should be a tuple'
        assert len(inp) == 2, 'inp should be of length 2'
        assert isinstance(inp[0],util.Point), 'inp[0] should be a Point'

        finalPoint = inp[0]
        currentPose = inp[1].odometry

        errorTheta = util.fixAnglePlusMinusPi(currentPose.point().angleTo(finalPoint) - currentPose.theta)
        errorDist = currentPose.point().distance(finalPoint)

        rvel = self.rotationGain * errorTheta
        fvel = self.forwardGain * errorDist

        if currentPose.point().isNear(finalPoint, self.distEps):
            return ("done", io.Action(0,0))

        # if not util.nearAngle(currentPose.point().angleTo(finalPoint), currentPose.theta, self.angleEps):
        if not abs(errorTheta) < self.angleEps:
            return ("rotating", io.Action(0, rvel))

        return ("forward", io.Action(fvel, 0))

    # def done(self, state):
    #     if state == 'done':
    #         return True
    #     return False


class StopSM(sm.SM):
    def getNextValues(self, state, inp):
        return ("stop", io.Action())

def switchCondition(inp):
    """
    Use the sm.Switch state-machine combinator in :func:`DynamicMoveToPoint` to make a robot that stops for pedestrians. 

    The robot stops if front sonar distance is less that 0.3m.
    """
    move = True
    frontSonarDist = min(inp[1].sonars[3:5])
    if frontSonarDist < 0.3:
        return not move
    return move
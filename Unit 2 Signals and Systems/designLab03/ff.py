import lib601.sm as sm

class FollowFigure(sm.SM):
    """
    we initialize the FollowFigure by giving it list of way points, which are 
    points that define a sequence of linear segments that the robot should traverse.

    The job of FollowFigure is to take instances of io.SensorInput as input and generate 
    instances of util.Point as output
    """
    def __init__(self, points):
        self.points = points
        self.finalState = len(points) - 1
        self.startState = 0
        self.distEps = 0.02
    
    def getNextValues(self, state, inp):
        """
        Calculates the next state and point based on the current state and input.

        Start out by generating the first point in the input sequence as output, and does that 
        until the robot's actual pose (found as sensorInput.odometry) is near that point; 
        Once the robot has  gotten  near  the  target  point,  the  machine switches  to  generating  
        the  next  target  point as output, etc.  Even after the robot gets near the final point, 
        the machine just continues to generate that point as output.
        
        Parameters:
            state (int): The current state.
            inp (Input): The input object.
        
        Returns:
            tuple: A tuple containing the next state and the next point.
        """
        if state == self.finalState:
            #Done
            return (state, self.points[state])

        currentPoint = inp.odometry.point()
        desiredPoint = self.points[state]

        if currentPoint.isNear(desiredPoint, self.distEps):
            return (state+1, self.points[state+1])
        return (state, self.points[state])
        
            


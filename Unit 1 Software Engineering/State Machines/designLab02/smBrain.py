import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io


# Eight sonars in front
#  threrefore 180 degrees divided in 8 angles
# each angle is 180/8 = 22.5 
# a, b and sonar values, c is 3rd side of triangle formed
# refer https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Triangle_with_notations_2.svg/220px-Triangle_with_notations_2.svg.png
# for diagram
Gamma = math.radians(22.5)
def get_height(a, b, gamma=Gamma):
    c =  math.sqrt(a**2 + b**2 - 2*a*b*math.cos(gamma)) # Cosine rule
    return (a*b/c)*math.sin(gamma) # sine rule


# Be within 0.5 distance from an obstacle
class MySMClass(sm.SM):
    def getNextValues(self, state, inp):
        a,b = inp.sonars[3:5]
        distance = get_height(a,b)
        eps = 0.05
        if distance < 0.5 - eps:
            return (state, io.Action(fvel = -0.5, rvel = 0.0))
        elif distance > 0.5 + eps:
            return (state, io.Action(fvel = 0.5, rvel = 0.0))
        else:
            return (state, io.Action(fvel = 0.0, rvel = 0.0))


mySM = MySMClass()
mySM.name = 'brainSM'

######################################################################
###
###          Brain methods
###
######################################################################

def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
                                        lambda: 
                                        io.SensorInput().sonars[sonarNum]))

# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=False, # slime trails
                                  sonarMonitor=False) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks(), verbose = True, compact=False)

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    print inp.sonars[3]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass

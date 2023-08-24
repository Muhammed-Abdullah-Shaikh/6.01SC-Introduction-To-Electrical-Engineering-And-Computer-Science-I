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
def get_median(a, b, gamma=Gamma):
    c =  math.sqrt(a**2 + b**2 - 2*a*b*math.cos(gamma)) # Cosine rule
    return(1 / 2)*math.sqrt(2*(a**2) + 2*(b**2) - c**2) # Apollonius’s Theorem

# Wall Follower
class MySMClass(sm.SM):
    def getNextValues(self, state, inp):
        sonars = inp.sonars
        front_distance = get_median(sonars[3], sonars[4]) if sonars[3] < 3 and sonars[4] < 3 else min(sonars[3], sonars[4])
        right_distance = get_median(sonars[6], sonars[7]) if sonars[6] < 3 and sonars[7] < 3 else min(sonars[6], sonars[7])
        if sonars[7] < 0.5 and sonars[7] > 0.3:
            right_distance = sonars[7]
        elif sonars[6] < 0.5 and sonars[6] > 0.3:
            right_distance = sonars[6]
        # right_distance = min(get_median(sonars[6], sonars[7]), sonars[7])
        print "Front Distance: ", front_distance
        print "Right Hand Side Distance: ", right_distance
        if front_distance > 0.5:
            if right_distance > 0.5: # Too far from boundry on the right, turn towards right
                return (state, io.Action(fvel = 0.5, rvel = -0.5))
            if right_distance < 0.3: # Too close to boundry on the right, move left
                return (state, io.Action(fvel = 0.2, rvel = 0.5))
            # Else move straight
            return (state, io.Action(fvel = 0.4, rvel = 0.0))
        else:
            # stop and turn left
            return (state, io.Action(fvel = 0.0, rvel = 1.0))

        
        


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
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
                                  sonarMonitor=False) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks(), verbose = True, compact=True)

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

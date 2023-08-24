import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io


class State:
    forward = 1
    left = 2
    right = 3

# Wall Follower
class MySMClass(sm.SM):

    startState = State.forward

    def getNextValues(self, state, inp):
        front_dist = min(inp.sonars[3], inp.sonars[4])
        right_dist = min(inp.sonars[6], inp.sonars[7])
        left_dist = min(inp.sonars[0], inp.sonars[1])

        print "Front Distance: ", front_dist
        print "Right Hand Side Distance: ", right_dist
        print "Left Hand Side Distance: ", left_dist
        print "State: ", state

        # no walls in 3m range Just keep going forwards
        if min(front_dist, right_dist, left_dist) > 3:
            return (State.forward, io.Action(fvel = 0.4, rvel = 0.0))

        # check front distance as we can get close to front while taking turn
        # We stop and rotate
        if front_dist < 0.5:
            return (State.right if min(inp.sonars[0:3]) < 0.3 else State.left, io.Action(fvel = 0.1, rvel = -1.0 if min(inp.sonars[0:3]) < 0.3 else 1.0))
        # if wall on the right side farther than 0.5, move right
        if right_dist > 0.5:
            return (State.right, io.Action(fvel = 0.2, rvel = -0.5))
        # if wall on the right side within 0.5 and 0.3, move forward
        if right_dist <=0.5 and right_dist >= 0.3:
            return (State.forward, io.Action(fvel = 0.4, rvel = 0.0))
        # Final case
        # if wall on right side less than 0.3 away, move left
        return (State.left, io.Action(fvel = 0.2, rvel = 0.5))


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
    robot.behavior.start(traceTasks = robot.gfx.tasks(), verbose = False, compact=True)

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

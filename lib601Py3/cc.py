# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/cc.py
from .leNumpy import *
from .util import *
print('Loading', __name__)

class Circuit:

    def __init__(self, components):
        self.components = components
        self.nodeDict = {}
        for c in components:
            for name in c.nodeNames:
                if name not in self.nodeDict:
                    self.nodeDict[name] = CircuitNode()

    def makeEquationSet(self, groundVoltage):
        ckt = EquationSet()
        self.addComponentEquations(ckt)
        self.addKCLEquations(ckt, groundVoltage)
        ckt.addEquation(setGround(groundVoltage))
        return ckt

    def addComponentEquations(self, equationSet):
        for c in self.components:
            equationSet.addEquation(c.componentEquation())

    def addKCLEquations(self, equationSet, groundVoltage):
        for c in self.components:
            c.addKCLToNodes(self.nodeDict)

        for name in list(self.nodeDict.keys()):
            if name != groundVoltage:
                node = self.nodeDict[name]
                nodeEq = node.kclEquation()
                if nodeEq.coeffs is []:
                    raise Exception('Error: Empty kcl equation - unconnected node?')
                equationSet.addEquation(nodeEq)

    def displaySolution(self, groundNode):
        ckt = self.makeEquationSet(groundNode)
        print('Solving the following equations:')
        for e in ckt.equations:
            print(e)

        print('The solution is:')
        print(ckt.solve())


class CircuitNode:

    def __init__(self):
        self.posCurrents = []
        self.negCurrents = []

    def addConnection(self, sign, currentName):
        if sign > 0:
            self.posCurrents.append(currentName)
        else:
            self.negCurrents.append(currentName)

    def kclEquation(self):
        return kcl(self.posCurrents, self.negCurrents)


class Component2Leads:

    def __init__(self, value, v1, v2):
        self.value = value
        self.v1Name = v1
        self.v2Name = v2
        self.currentName = gensym('i_' + v1 + '_' + v2)
        self.nodeNames = [v1, v2]

    def addKCLToNodes(self, nodeDict):
        node1 = nodeDict[self.v1Name]
        node2 = nodeDict[self.v2Name]
        node1.addConnection(-1, self.currentName)
        node2.addConnection(1, self.currentName)

    def __str__(self):
        return str([self.__class__.__name__] + self.nodeNames)

    __repr__ = __str__


class Resistor(Component2Leads):

    def componentEquation(self):
        return resistor(self.value, self.v1Name, self.v2Name, self.currentName)


class VSrc(Component2Leads):

    def componentEquation(self):
        return vsrc(self.value, self.v1Name, self.v2Name)


class ISrc(Component2Leads):

    def componentEquation(self):
        return isrc(self.value, self.currentName)


class Wire(Component2Leads):

    def __init__(self, v1, v2):
        Component2Leads.__init__(self, 0, v1, v2)

    def componentEquation(self):
        return wire(self.v1Name, self.v2Name)


class OpAmp:

    def __init__(self, v1, v2, v3, K = 10000):
        self.K = K
        self.v1Name = v1
        self.v2Name = v2
        self.voutName = v3
        self.currentName = gensym('i_' + v3)
        self.nodeNames = [v1, v2, v3]

    def addKCLToNodes(self, nodeDict):
        node3 = nodeDict[self.voutName]
        node3.addConnection(-1, self.currentName)

    def componentEquation(self):
        return opamp(self.K, self.v1Name, self.v2Name, self.voutName)

    def __str__(self):
        return str([self.__class__.__name__] + self.nodeNames)

    __repr__ = __str__


def resistor(R, vn1, vn2, i12):
    return Equation([1.0, -1.0, -float(R)], [vn1, vn2, i12], 0)


def vsrc(Vs, vn1, vn2):
    return Equation([1.0, -1.0], [vn1, vn2], float(Vs))


def kcl(pos, neg):
    return Equation([ 1 for x in pos ] + [ -1 for x in neg ], pos + neg, 0.0)


def setGround(vn1):
    return Equation([1], [vn1], 0.0)


def wire(vn1, vn2):
    return Equation([1.0, -1.0], [vn1, vn2], 0.0)


def opamp(K, vPlus, vMinus, voutPlus):
    return Equation([1.0, -K, K], [voutPlus, vPlus, vMinus], 0.0)


def isrc(Is, i):
    return Equation([1.0], [i], float(Is))


def thevenin(VR, vn1, vn2, i12):
    Vth, Rth = VR
    return Equation([1.0, -1.0, -Rth], [vn1, vn2, i12], Vth)
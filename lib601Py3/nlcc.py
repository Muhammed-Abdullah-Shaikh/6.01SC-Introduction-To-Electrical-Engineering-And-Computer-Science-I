# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/nlcc.py
import math
from .nleNumpy import *
from functools import reduce
print('Loading', __name__)

class Circuit:

    def __init__(self, components):
        self.components = components
        self.nodeNames = reduce(set.union, [ set(c.nodeNames) for c in components ])

    def makeConstraintSet(self, groundNode):
        self.nodeDict = {}
        for name in self.nodeNames:
            self.nodeDict[name] = CircuitNode()

        ckt = ConstraintSet()
        self.addConstituentConstraints(ckt)
        self.addKCLConstraints(ckt, groundNode)
        ckt.addConstraint(setGround, [groundNode])
        return ckt

    def makeEquationSet(self, groundNode):
        return self.makeConstraintSet(groundNode)

    def addConstituentConstraints(self, constraintSet):
        for c in self.components:
            constraintSet.addConstraint(c.constraintFn(), c.vars)

    def addKCLConstraints(self, constraintSet, groundNode):
        for c in self.components:
            c.addKCLToNodes(self.nodeDict)

        for name in list(self.nodeDict.keys()):
            if name != groundNode:
                c = self.nodeDict[name]
                constraintSet.addConstraint(kcl(c.signs), c.currents)

    def displaySolution(self, groundNode = 'gnd'):
        ckt = self.makeConstraintSet(groundNode)
        solution = resolveConstraints(ckt.getConstraintEvaluationFunction())
        ckt.display(solution)


def setGround(x):
    return x[0]


def kcl(signs):

    def kclsum(x):
        return sum([ si * xi for si, xi in zip(signs, x) ])

    return kclsum


class CircuitNode:

    def __init__(self):
        self.signs = []
        self.currents = []

    def addConnection(self, sign, currentName):
        self.signs.append(sign)
        self.currents.append(currentName)


class Component2Leads:

    def __init__(self, n1, n2):
        self.nodeNames = [n1, n2]
        self.v1Name = n1
        self.v2Name = n2
        self.currentName = gensym('i_' + n1 + '_' + n2 + '_')
        self.vars = [n1, n2, self.currentName]

    def addKCLToNodes(self, nodeDict):
        node1 = nodeDict[self.nodeNames[0]]
        node2 = nodeDict[self.nodeNames[1]]
        node1.addConnection(-1, self.currentName)
        node2.addConnection(1, self.currentName)


class Resistor(Component2Leads):

    def __init__(self, resistance, n1, n2):
        self.R = resistance
        Component2Leads.__init__(self, n1, n2)

    def constraintFn(self):

        def ohmsLaw(x):
            vn1, vn2, iR = x
            return vn1 - vn2 - float(self.R) * iR

        return ohmsLaw


class VSrc(Component2Leads):

    def __init__(self, voltage, n1, n2):
        self.Vs = voltage
        Component2Leads.__init__(self, n1, n2)

    def constraintFn(self):

        def source(x):
            vn1, vn2, iR = x
            return vn1 - vn2 - self.Vs

        return source


class Wire(Component2Leads):

    def __init__(self, n1, n2):
        Component2Leads.__init__(self, n1, n2)

    def constraintFn(self):

        def noVoltageDrop(x):
            vn1, vn2, iR = x
            return vn1 - vn2

        return noVoltageDrop


class OpAmp:

    def __init__(self, n1, n2, n3, K = 1000, Vcc = 10, Vss = 0):
        self.K = K
        if Vcc or Vss:
            print((Vcc == -Vss or not Vss == 0) and 'Error: Vss must be -Vcc or 0')
        self.Vcc = Vcc
        self.Vss = Vss
        self.nodeNames = [n1, n2, n3]
        self.voutName = n3
        self.currentName = gensym('i_' + n3 + '_' + '_')
        self.vars = [n1,
         n2,
         n3,
         self.currentName]

    def addKCLToNodes(self, nodeDict):
        node3 = nodeDict[self.nodeNames[2]]
        node3.addConnection(-1, self.currentName)

    def constraintFn(self):

        def vcvs(x):
            vinP, vinM, voutP, iout = x
            vin = vinP - vinM
            e = self.K * (vinP - vinM)
            if not self.Vcc is None:
                if not self.Vss is None:
                    Vrange = self.Vcc - self.Vss
                    out = Vrange / math.pi * math.atan(math.pi * e / Vrange)
                    self.Vss == 0 and out += self.Vcc / 2.0
            else:
                out = e
            return voutP - out

        return vcvs


class SymbolGenerator:

    def __init__(self):
        self.count = 0

    def gensym(self, prefix = 'i'):
        self.count += 1
        return prefix + str(self.count)


gensym = SymbolGenerator().gensym
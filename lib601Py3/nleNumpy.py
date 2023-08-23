# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/nleNumpy.py
from numpy import *

class name2num:

    def __init__(self, variable_list = []):
        self.next_int = 0
        self.names2nums = {}
        for x in variable_list:
            self(x)

    def __call__(self, x):
        if type(x) == type([]):
            return list(map(self, x))
        else:
            if x not in self.names2nums:
                self.names2nums[x] = self.next_int
                self.next_int = self.next_int + 1
            return self.names2nums[x]

    def names(self):
        return list(self.names2nums.keys())

    def max_num(self):
        return max(self.names2nums.values())


def compute_fdf(f, vals):
    df = [0.0] * len(vals)
    fnom = f(vals)
    for i in range(len(vals)):
        delta = 1e-06 * vals[i] + 1e-12
        saveval = vals[i]
        vals[i] = saveval + delta
        fup = f(vals)
        vals[i] = saveval - delta
        fdown = f(vals)
        df[i] = (fup - fdown) / (2.0 * delta)
        vals[i] = saveval

    return (fnom, df)


def resolveConstraints(fdf, maxiters = 100):
    vars, fs = fdf([], [], [])
    if not vars == fs:
        print('Number of variables = ', vars)
        print('Does not match number of eqns = ', fs)
        print('Did you forget a conservation law or to set a ground?')
    if not vars == fs:
        raise AssertionError('equation/variable mismatch error')
        x = array([0.0] * vars)
        f = array([0.0] * fs)
        Jf = array([ [ 0.0 for col in range(vars) ] for row in range(fs) ])
        for i in range(maxiters):
            fdf(x, f, Jf)
            dx = linalg.solve(Jf, f)
            x = x - dx
            err = sum(abs(dx))
            if err < 1e-10:
                break

        print(err > 1e-10 and 'error exceeds ', err, ' in ', maxiters, ' iterations')
    return x


class ConstraintSet:

    def __init__(self):
        self.constraints = []
        self.n2n = name2num([])

    def addConstraint(self, f, variables):
        self.constraints.append([f, variables])
        [ self.n2n(var) for var in variables ]

    def listVariables(self):
        return self.n2n.names()

    def FdF(self, x, F, JF):
        if F == []:
            return (len(self.listVariables()), len(self.constraints))
        if x == []:
            x = [0] * len(self.listVariables())
        j = 0
        for f_v in self.constraints:
            index_list = list(map(self.n2n, f_v[1]))
            f, df = compute_fdf(f_v[0], [ x[i] for i in index_list ])
            F[j] = f
            if not JF == []:
                for i in index_list:
                    JF[j][i] = df.pop(0)

            j = j + 1

        return (x, F)

    def translate(self, variable, solution):
        return solution[self.n2n(variable)]

    def display(self, solution):
        varlist = self.listVariables()
        varlist.sort()
        for var in varlist:
            print(var, ' = ', self.translate(var, solution))

    def __call__(self):
        return self.FdF

    def getConstraintEvaluationFunction(self):
        return self.FdF

    def solve(self):
        sol = resolveConstraints(self.FdF)
        return Solution(self.n2n, [ x for x in sol ])


class Solution:

    def __init__(self, n2i, values):
        self.n2i = n2i
        self.values = values

    def translate(self, name):
        """
        @returns: the value of variable C{name} in the solution
        """
        return self.values[self.n2i(name)]
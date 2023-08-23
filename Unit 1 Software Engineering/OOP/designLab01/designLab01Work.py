#
# File:   designLab01Work.py
# Author: 6.01 Staff
# Date:   02-Sep-11
#
# Below are templates for your answers to three parts of Design Lab 1

#-----------------------------------------------------------------------------

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

#-----------------------------------------------------------------------------

class V2:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
    
    def __str__(self):
        return f"V2({self.X}, {self.Y})"

    def getX(self):
        return self.X
    def getY(self):
        return self.Y

    def __add__(self, other):
        return V2(self.X + other.X, self.Y + other.Y)

    def __mul__(self, other):
        if isinstance(other, V2):
            return self.X * other.X + self.Y * other.Y
        else:
            return V2(self.X * other, self.Y * other)
#-----------------------------------------------------------------------------

class Polynomial:
    def __init__(self, coefficients):
        self.coeffs = coefficients
        self.order = len(self.coeffs)-1

    def coeff(self, i):
        if i < 0:
            return 0
        if i >= len(self.coeffs):
            return 0
        return self.coeffs[i]
    
    def add(self, other):
        if self.order < 0:
            return other
        if other.order < 0:
            return self
        if self.order < other.order:
            diff = other.order - self.order
            return Polynomial(other.coeffs[:diff]+[a + b for a, b in zip(self.coeffs, other.coeffs[diff:])])
        if self.order > other.order:
            diff = self.order - other.order
            return Polynomial(self.coeffs[:diff]+[a + b for a, b in zip(other.coeffs, self.coeffs[diff:])])

        return Polynomial([a + b for a, b in zip(self.coeffs, other.coeffs)])

    def mul(self, other):
        temp_poly = Polynomial([])
        order = self.order
        for coeff in self.coeffs:
            temp_poly += Polynomial([coeff*c1 for c1 in other.coeffs] + [0]*order)
            order -= 1
        return temp_poly

    def val(self, x):
        result = 0
        for i, coeff in enumerate(reversed(self.coeffs)):
            result += coeff * x**i
        return result
    
    def roots(self):
        if self.order < 0:
            return None
        if self.order == 0:
            return self.coeffs[0]
        if self.order == 1:
            return - self.coeffs[1] / self.coeffs[0]
        if self.order == 2:
            a, b, c = self.coeffs
            D2 = b**2 - 4*a*c
            D = None
            if D2 < 0:
                D = complex(D2**0.5)
            else:
                D = D2**0.5
            return (-b + D) / (2*a), (-b - D) / (2*a)
        return "Order too high to solve for roots."

    def __str__(self):
        if self.order < 0:
            return "0"

        out = "+" + str(self.coeffs[-1])
        for i, coeff in enumerate(reversed(self.coeffs[:-1]), start=1):
            if coeff != 0:
                if coeff < 0:
                    out = f"-{coeff}x**{i} " + out
                else:
                    out = f"+{coeff}x**{i} " + out
        return out

    def __add__(self, other):
        return self.add(other)

    def __mul__(self, other):
        return self.mul(other)

    def __call__(self, x):
        return self.val(x)

    def __repr__(self):
        return str(self)




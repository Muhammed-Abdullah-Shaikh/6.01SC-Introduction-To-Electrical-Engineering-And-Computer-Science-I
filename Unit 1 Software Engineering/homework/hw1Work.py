import pdb
import lib601.sm as sm
import string
import operator

LAZY=False

class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.opStr + '(' + \
               str(self.left) + ', ' +\
               str(self.right) + ')'
    __repr__ = __str__

    def lazy_eval(self, env):
        left_val = self.left.eval(env)
        right_val = self.right.eval(env)
        if not isNum(left_val) or not isNum(right_val):
            return eval(self.opStr)(left_val, right_val)
        return self.op(left_val, right_val)

    def eval(self, env, lazy=LAZY):
        if lazy:
            return self.lazy_eval(env)
        else:
            return self.op(self.left.eval(env), self.right.eval(env))


class Sum(BinaryOp):
    opStr = 'Sum'
    op = operator.add

class Prod(BinaryOp):
    opStr = 'Prod'
    op = operator.mul

class Quot(BinaryOp):
    opStr = 'Quot'
    op = operator.truediv

class Diff(BinaryOp):
    opStr = 'Diff'
    op = operator.sub

class Assign(BinaryOp):
    opStr = 'Assign'

    def eval(self,env, lazy=LAZY):
        if lazy:
            self.lazy_eval(env)
        else:
            env[self.left.name] = self.right.eval(env)
    
    def lazy_eval(self, env):
        env[self.left.name] = self.right
        
class Number:
    def __init__(self, val):
        self.value = val
    def __str__(self):
        return 'Num('+str(self.value)+')'
    __repr__ = __str__

    def eval(self, env):
        return self.value

class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Var('+self.name+')'
    __repr__ = __str__

    def eval(self, env, lazy=LAZY):
        if lazy:
            return self.lazy_eval(env)
        return env[self.name]

    def lazy_eval(self, env):
        if self.name not in env:
            return Variable(self.name)
        if isNum(env[self.name]):
            return env[self.name]
        return env[self.name].eval(env)

# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']

# Convert strings into a list of tokens (strings)
def tokenizeLegacy(string):
    tokens = [string.replace(" ", "")]
    for sep in seps:
        ## maps a list of strings to fuction slit by sep, 
        ## returns a list of lists
        ## sum with empty list flattens it out
        ## However this approach also removes delimeters
	    tokens = sum(map(lambda x: [l for l in x.split(sep) if l], tokens), [])
    return tokens

# Convert strings into a list of tokens (strings)
def tokenize(string):
    tokens = []
    start = 0
    end = 0
    for char in string:
        if char in seps or char == " ":
            # Check for space for cases like 'hi 33 777' 
            tokens.append(string[start:end].strip())
            tokens.append(char.strip())
            start = end+1
        end += 1
    if start != end:
        tokens.append(string[start:end])
    return [l for l in tokens if l]

# tokens is a list of tokens
# returns a syntax tree:  an instance of {\tt Number}, {\tt Variable},
# or one of the subclasses of {\tt BinaryOp} 
def parse(tokens):
    def parseExp(index):
        if numberTok(tokens[index]):
            return Number(float(tokens[index])), index + 1
        if variableTok(tokens[index]):
            return Variable(tokens[index]), index + 1
        
        if tokens[index] == '(':
            left, index = parseExp(index + 1)
            
            token = tokens[index]
            if token == '+':
                op = Sum
            elif token == '-':
                op = Diff
            elif token == '*':
                op = Prod
            elif token == '/':
                op = Quot
            elif token == '=':
                op = Assign

            right, index = parseExp(index + 1)

            if tokens[index] == ')':
                return op(left, right), index + 1
        
    (parsedExp, nextIndex) = parseExp(0)
    return parsedExp

# token is a string
# returns True if contains only digits
def numberTok(token):
    for char in token:
        if not char in string.digits: return False
    return True

# token is a string
# returns True its first character is a letter
def variableTok(token):
    for char in token:
        if char in string.letters: return True
    return False

# thing is any Python entity
# returns True if it is a number
def isNum(thing):
    return type(thing) == int or type(thing) == float

# Run calculator interactively
def calc():
    env = {}
    while True:
        e = raw_input('%')            # prints %, returns user input
        print '%', parse(tokenize(e)).eval(env)
        print '   env =', env

# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    env = {}
    for e in exprs:
        print '%', e                    # e is the experession 
        print '%', parse(tokenize(e)).eval(env)
        print '   env =', env

# Simple tokenizer tests
'''Answers are:
['fred']
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''
def testTokenize():
    print tokenize('fred ')
    print tokenize('777 ')
    print tokenize('777 hi 33 ')
    print tokenize('**-)(')
    print tokenize('( hi * ho )')
    print tokenize('(fred + george)')
    print tokenize('(hi*ho)')
    print tokenize('( fred+george )')


# Simple parsing tests from the handout
'''Answers are:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''
def testParse():
    print parse(['a'])
    print parse(['888'])
    print parse(['(', 'fred', '+', 'george', ')'])
    print parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')' ,')'])
    print parse(tokenize('((a * b) / (cee - doh))'))
    print parse(tokenize('(a = (3 * 5))'))

####################################################################
# Test cases for EAGER evaluator
####################################################################

def testEval():
    env = {}
    Assign(Variable('a'), Number(5.0)).eval(env)
    print Variable('a').eval(env)
    env['b'] = 2.0
    print Variable('b').eval(env)
    env['c'] = 4.0
    print Variable('c').eval(env)
    print Sum(Variable('a'), Variable('b')).eval(env)
    print Sum(Diff(Variable('a'), Variable('c')), Variable('b')).eval(env)
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).eval(env)
    print Variable('a').eval(env)
    print env

# Basic calculator test cases (see handout)
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]
# calcTest(testExprs)

####################################################################
# Test cases for LAZY evaluator
####################################################################

# Simple lazy eval test cases from handout
'''Answers are:
Sum(Var(b), Var(c))
Sum(2.0, Var(c))
6.0
'''
def testLazyEval():
    env = {}
    Assign(Variable('a'), Sum(Variable('b'), Variable('c'))).eval(env)
    print Variable('a').eval(env)
    env['b'] = Number(2.0)
    print Variable('a').eval(env)
    env['c'] = Number(4.0)
    print Variable('a').eval(env)

# Lazy partial eval test cases (see handout)
lazyTestExprs = ['(a = (b + c))',
                  '(b = ((d * e) / 2))',
                  'a',
                  '(d = 6)',
                  '(e = 5)',
                  'a',
                  '(c = 9)',
                  'a',
                  '(d = 2)',
                  'a']
# calcTest(lazyTestExprs)

## More test cases (see handout)
partialTestExprs = ['(z = (y + w))',
                    'z',
                    '(y = 2)',
                    'z',
                    '(w = 4)',
                    'z',
                    '(w = 100)',
                    'z']

# calcTest(partialTestExprs)

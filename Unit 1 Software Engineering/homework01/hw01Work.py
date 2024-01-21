import pdb
import lib601.sm as sm
import string
import operator

LAZY=True

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
        """
        Evaluate the lazy expression in the given environment.
        if any of right or left doesn't evaluate into a Number
        then it's simply still Binary Operation
        `eval(self.opStr)(left_val, right_val)` is equivalent to `Sum(left_val, right_val)` if opStr is 'Sum'

        Parameters:
            env (dict): The environment in which to evaluate the expression.

        Returns:
            int or float or str: The result of evaluating the lazy expression.
        """
        left_val = self.left.eval(env)
        right_val = self.right.eval(env)
        # if any of right or left doesn't evaluate into a Number
        # then it's simple still Binary Operation
        # 
        if not isNum(left_val) or not isNum(right_val):
            return eval(self.opStr)(left_val, right_val)
        return self.op(left_val, right_val)

    def eval(self, env, lazy=LAZY):
        """
        Evaluate the expression in the given environment.

        Args:
            env (dict): The environment in which to evaluate the expression.
            lazy (bool, optional): Whether to lazily evaluate the expression. Defaults to LAZY.

        Returns:
            The result of evaluating the expression.
        """
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
        """
        Evaluate the expression.

        Args:
            env (dict): The environment in which the expression is evaluated.
            lazy (bool, optional): If lazy evaluation should be performed. Defaults to LAZY.

        Returns:
            None
        """
        if lazy:
            self.lazy_eval(env)
        else:
            env[self.left.name] = self.right.eval(env)
    
    def lazy_eval(self, env):
        """
        Assigns the value of `self.right` to the variable `self.left.name` in the given environment `env`.
        Does not evaluate the right hand side; simply assign the value of the variable in the environment (`self.left.name`) to be the unevaluated syntax tree (`self.right`).

        Parameters:
            env (dict): The environment in which the assignment will be made.

        Returns:
            None
        """
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
        """
        Evaluates the expression in the given environment.

        Parameters:
            env (dict): The environment in which the expression is evaluated.
            lazy (bool, optional): Whether to lazily evaluate the expression. Defaults to LAZY.

        Returns:
            The evaluated value of the expression.
        """
        if lazy:
            return self.lazy_eval(env)
        return env[self.name]

    def lazy_eval(self, env):
        """
        Evaluates a lazy expression based on the given environment.
        1. If there is no variable in the environment already, simply returns an instance of Variable
        with the name of the variable
        2. Otherwise, returns the value of the variable from the environment if the variable is a number
        3. Otherwise, returns the syntax tree for the expression

        Parameters:
            env (dict): The environment containing variable-value mappings.

        Returns:
            Variable or Num: The evaluated expression.
        """
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
        tokens = sum([[l for l in x.split(sep) if l] for x in tokens], [])
    return tokens

# Convert strings into a list of tokens (strings)
def tokenize(string):
    """
    Tokenizes a given string into a list of tokens.
    For each charecter in the string, it checks if it is a space or sperator (`(`, `)`, `+`, `-`, `*`, `/`, `=`)
    Need to check for spaces for cases like 'hi 33 777'
        
    If the character is a separator or space, the function adds the substring that starts from
    the `start` index and ends just before the current index (`end`) to the `tokens` list.
    This extracted substring is stripped of any leading or trailing spaces to ensure clean tokens.
    Additionally, the current character is added as a separate token to the `tokens` list.
    
    The `start` index is then updated to the position after the last separator or space.

    At the end of the loop, if the `start` index is not equal to the `end` index, it means there
    is a final token to be added to the `tokens` list. Only happnes when the last token
    is not followed by a separator.
    Eg. tokenize('fred+george')

    Parameters:
        string (str): The string to be tokenized.

    Returns:
        list: A list of tokens extracted from the input string.
    """
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
    """
    Parses a list of tokens and returns the parsed expression.

    Parameters:
    - tokens (list): A list of tokens representing an arithmetic expression.

    Returns:
    - parsedExp: The parsed expression.

    Example:
    parse(['(', '+', '2', '3', ')']) returns Sum(Number(2), Number(3))
    """
    def parseExp(index):
        """
        Parses an expression from a given index in the tokens list.

        1. If token represents a number, then make it into a Number instance and return that, paired with index+1.
        2. If token represents a variable name, then make it into a Variable instance and return that paired with index+1. 
        3. Otherwise, the sequence of tokens starting at index must be of the form: (  expression  op  expression  )
            Therefore, token must be `(` 
            - Using recursive call to parseExp, gives a  syntax tree for left side and 
            the index for the token beyond the end of the expression. 
            - The token beyond leftTree is a single-character operator token called op. 
            This op determines the Binary Operation to be performed.
            - Again using a recursive call to parseExp, gives a syntax tree for right side and
            the index for the token beyond the end of the expression.

        Parameters:
            index (int): The index in the tokens list from where to start parsing the expression.

        Returns:
            tuple: A tuple containing the parsed expression and the updated index.

        Raises:
            None
        """
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
        e = input('%')            # prints %, returns user input
        print('%', parse(tokenize(e)).eval(env))
        print('   env =', env)

# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    env = {}
    for e in exprs:
        print('%', e)                    # e is the experession 
        print('%', parse(tokenize(e)).eval(env))
        print('   env =', env)

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
    print(tokenize('fred '))
    print(tokenize('777 '))
    print(tokenize('777 hi 33 '))
    print(tokenize('**-)('))
    print(tokenize('( hi * ho )'))
    print(tokenize('(fred + george)'))
    print(tokenize('(hi*ho)'))
    print(tokenize('( fred+george )'))


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
    print(parse(['a']))
    print(parse(['888']))
    print(parse(['(', 'fred', '+', 'george', ')']))
    print(parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')' ,')']))
    print(parse(tokenize('((a * b) / (cee - doh))')))
    print(parse(tokenize('(a = (3 * 5))')))

####################################################################
# Test cases for EAGER evaluator
####################################################################

def testEval():
    env = {}
    Assign(Variable('a'), Number(5.0)).eval(env)
    print(Variable('a').eval(env))
    env['b'] = 2.0
    print(Variable('b').eval(env))
    env['c'] = 4.0
    print(Variable('c').eval(env))
    print(Sum(Variable('a'), Variable('b')).eval(env))
    print(Sum(Diff(Variable('a'), Variable('c')), Variable('b')).eval(env))
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).eval(env)
    print(Variable('a').eval(env))
    print(env)

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
    print(Variable('a').eval(env))
    env['b'] = Number(2.0)
    print(Variable('a').eval(env))
    env['c'] = Number(4.0)
    print(Variable('a').eval(env))

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

import itertools

class Exp:
    def __init__(self):
        pass
    def eval(self, env):
        pass
    def __add__(self, exp1, exp2):
        return Or(exp1, exp2)
    def __mul__(self, exp1, exp2):
        return And(exp1, exp2)

    def tautology(self, vars):
        permutations = map(list, itertools.product([False, True], repeat=len(vars)))
        if len(vars) == 0:
            return self.eval({})
        for permutation in permutations:
            env = {}
            for i in range(len(vars)):
                env[vars[i]] = permutation[i]
            if not self.eval(env):
                return False
        return True

    def symplify(self):
        if isinstance(self, Not):
            return Not(self.exp.symplify())
        elif isinstance(self, Or) or isinstance(self, And):
            if isinstance(self.left, Cons) and self.left.val == False:
                return self.right.symplify()
            elif isinstance(self.right, Cons) and self.right.val == False:
                return self.left.symplify()
            else:
                if isinstance(self, Or):
                    return self.__add__(self.left.symplify(), self.right.symplify())
                else:
                    return self.__mul__(self.left.symplify(), self.right.symplify())
        return self #cons or var

class Or(Exp):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return'(' + self.left.__str__() + ' ∨ ' + self.right.__str__() + ')'
    def eval(self, env):
        return self.left.eval(env) or self.right.eval(env)

class And(Exp):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return '(' + self.left.__str__() + ' ∧ ' + self.right.__str__() + ')'
    def eval(self, env):
        return self.left.eval(env) and self.right.eval(env)

class Var(Exp):
    def __init__(self, var):
        self.var = var
    def __str__(self):
        return self.var
    def eval(self, env):
        if self.var not in env.keys():
            raise noValException("No value for vareiable " + self.var)
        return env[self.var]
class Cons(Exp):
    def __init__(self, val):
        if type(val) != bool:
            raise typeException("Value must be boolean")
        self.val = val
    def __str__(self):
        return str(self.val)
    def eval(self, env):
        return self.val

class Not(Exp):
    def __init__(self, exp):
        self.exp = exp
    def __str__(self):
        return '¬' + str(self.exp)
    def eval(self, env):
        return not self.exp.eval(env)

class typeException(Exception):
    pass

class noValException(Exception):
    pass

exp = Or(Cons(False), And(Cons(True), Not(Var('x'))))
val = exp.eval({'x' : True})
print(exp.__str__())
print('for: ' + str({'x' : True}) +', in: ' + exp.__str__() + ', val: ' + str(val))

taut = Or(Var('p'), Not(Var('p')))
if taut.tautology(['p']):
    print('Exp: ' + taut.__str__() + ' is tautology.')
else:
    print('Exp: ' + taut.__str__() + ' is not tautology.')

print('for: ' + exp.__str__() + ', symplify(): ' + exp.symplify().__str__())

#exp.eval({'y' : True})
#Cons('True')
import numpy as np
from collections import defaultdict, Counter
import itertools

from IPython.display import Math, display, HTML

import exh.utils         as utils
import exh.model.options as options
import exh.model.vars    as var

from .simplify import IteratorType
from .display  import Display
from .evaluate import Evaluate


class Formula(IteratorType, Display, Evaluate): # Using sub-classing to spread code over multiple files
    """
    Base class for fomulas

    Class attributes:
        no_parenthesis (bool) -- whether to display the formula with parenthesis around it in conjunctions, coordinations, etc.
        substitutable  (bool) -- Whether sub-formulas of this formulas count as alternatives to it

    Attributes:
        children (list(Formula)) -- sub-formulas
        vm (VariableManager)     -- organizes mapping from predicate and variables name to concrete bit position
    """

    no_parenthesis = False
    substitutable = True

    def __init__(self, *children):
        self.subst = self.__class__.substitutable
        self.children = children
        self.vars()

        # Free vars are lexically ordered
        self.free_vars = list(set(var for child in self.children for var in child.free_vars))
        self.free_vars.sort()

    def reinitialize(self): #only used for Exh, which performs computation at initialization
        pass

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)

    def __str__(self):
        return self.display()

    def __repr__(self):
        return self.display()

    def copy(self):
        """Creates copy of the object (overridden by children's classes"""
        return Formula(*self.children)

    def __eq__(self, other):
        """Returns true if two formulas are syntactically the same, up to constituent reordering (overridden by children classes)"""
        return self.__class__ is other.__class__

    def __hash__(self):
        return hash(self.__class__)



    ### FORMULA MANIPULATION METHODS ###
    def flatten(self):
        """
        Turns embedded "or" and "and" in to generalized "or" and "and"
        Ex: a or ((b or c) or d) becomes a or b or c or d
        """
        raise Exception("Not implemented yet!")

        if self.type in ["and", "or"]:
            new_children = list(self.iterator_type())
        else:
            new_children = self.children

        return Formula(self.type, *map(lambda c: c.flatten(), new_children))


    def simplify(self):
        """Turns a formula into a quantifier-first, disjunctions of conjunctions formula"""
        raise Exception("Not implemented yet!")

        # Returns all indexes of variables in a conjunctive formula
        def idx_vars(f):
            return [child.idx if "idx" in dir(child) else -1 for child in f.iterator_type("and")]

        if self.type == "or" or self.type == "and":
            simplified_children = [child.simplify() for child in self.iterator_type()]

            if self.type == "or":
                all_children = [grandchild for child in simplified_children for grandchild in child.iterator_type("or")]
                all_children.sort(key = idx_vars)

                return Formula("or", *all_children)

            else:
                all_children = [list(child.iterator_type("or")) for child in simplified_children]
                individual_conjuncts = TODO

                return self
        elif self.type == "neg":
            child = self.children[0]

            if child.type == "or":
                pass
        else:
            return self

    def vars(self):
        """Returns a VariableManager object for all the variables that occur in the formula"""

        self.vm = var.VarManager.merge(*[c.vars() for c in self.children])
        self.vm.linearize()
        return self.vm

    @classmethod
    def alternative_to(cls, other):
        """
        Returns an formulat which is an alternative to other with the same children  ; meant to be overriden by subclasses
        Example: Or.alternative_to(a & b) -> a | b
        """
        raise Exception("alternative_to is not been implemented for class {}".format(cls.__name__))



############### OPERATORS ##############

class Operator(Formula):
    """
    Base class for associative operators

    Class attributes:
        plain_symbol (str) -- symbol to display in plain text mode (to be overridden by children classes)
        latex_symbol (str) -- symbol to display in LateX mode (to be overridden by children classes)

    Attributes:
        fun (function) -- function to call on subformulas' result to get parent result
    """


    plain_symbol = "op"
    latex_symbol = "\text{op}"

    def __init__(self, fun, is_commutative, *children):
        super(Operator, self).__init__(*children)
        self.is_commutative = is_commutative
        self.fun = fun

    def evaluate_aux(self, assignment, vm, variables = dict(), free_vars = list()):
        """Stacks subformulas' results and applies fun to it"""
        return self.fun(np.stack([child.evaluate_aux(assignment, vm, variables, free_vars) for child in self.children]))


    def display_aux(self, latex):

        if latex:
            symbol = self.__class__.latex_symbol
        else:
            symbol = self.__class__.plain_symbol

        def paren(child):
            if (self.__class__ is child.__class__) or child.__class__.no_parenthesis:
                return child.display_aux(latex)
            else:
                return "({})".format(child.display_aux(latex))

        if len(self.children) == 1:
            return "{}[{}]".format(symbol, self.children[0].display_aux(latex))
        else:
            return " {type} ".format(type = symbol).join([paren(child) for child in self.children])

    @classmethod
    def alternative_to(cls, other):
        return cls(*other.children)

    def __members(self):
        return self.children

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False

        if self.is_commutative:
            return Counter(self.__members()) == Counter(other.__members())
        else:
            return self.__members() == other.__members()

    def __hash__(self):
        str_memebrs = sorted([str(m) for m in self.__members()])  # TODO: Why str
        return hash((self.__class__, tuple(str_memebrs)))


class And(Operator):
    plain_symbol = "and"
    latex_symbol = r"\land"

    fun_ = lambda array: np.min(array, axis = 0)
    is_commutative = True

    """docstring for And"""
    def __init__(self, *children):
        super(And, self).__init__(And.fun_, And.is_commutative, *children)


class Or(Operator):
    plain_symbol = "or"
    latex_symbol = r"\lor"

    fun_ = lambda array: np.max(array, axis = 0)
    is_commutative = True

    """docstring for Or"""
    def __init__(self, *children):
        super(Or, self).__init__(Or.fun_, Or.is_commutative, *children)

class Not(Operator):
    no_parenthesis = True

    plain_symbol = "not"
    latex_symbol = r"\neg"

    fun_ = lambda x: np.squeeze(np.logical_not(x), axis = 0)
    is_commutative = False

    """docstring for Not"""
    def __init__(self, child):
        super(Not, self).__init__(Not.fun_, Not.is_commutative, child)


class Nand(Operator):
    plain_symbol = "nand"
    latex_symbol = r"\nand"

    fun_ = lambda array: ~np.min(array, axis=0)
    is_commutative = True

    def __init__(self, *children):
        super(Nand, self).__init__(Nand.fun_, Nand.is_commutative, *children)


class Nor(Operator):
    plain_symbol = "nor"
    latex_symbol = r"\nor"

    fun_ = lambda array: ~np.max(array, axis=0)
    is_commutative = True

    def __init__(self, *children):
        super(Nor, self).__init__(Nor.fun_, Nor.is_commutative, *children)


class Xor(Operator):
    plain_symbol = "xor"
    latex_symbol = r"\xor"

    fun_ = lambda array: np.max(array, axis=0) & ~np.min(array, axis=0)
    is_commutative = True

    def __init__(self, *children):
        super(Xor, self).__init__(Xor.fun_, Xor.is_commutative, *children)


class Iff(Operator):
    plain_symbol = "iff"
    latex_symbol = r"\iff"

    fun_ = lambda array: np.min(array, axis=0) | ~np.max(array, axis=0)
    is_commutative = True

    def __init__(self, *children):
        super(Iff, self).__init__(Iff.fun_, Iff.is_commutative, *children)

class OnlyL(Operator):
    plain_symbol = "onlyl"
    latex_symbol = r"\onlyl"

    fun_ = lambda array: array[0] & np.all(~array[1:], axis = 0)
    is_commutative = False

    def __init__(self, *children):
        super(OnlyL, self).__init__(OnlyL.fun_, OnlyL.is_commutative, *children)


class OnlyR(Operator):
    plain_symbol = "onlyr"
    latex_symbol = r"\onlyr"

    fun_ = lambda array: array[-1] & np.all(~array[:-1], axis = 0)
    is_commutative = False

    def __init__(self, *children):
        super(OnlyR, self).__init__(OnlyR.fun_, OnlyR.is_commutative, *children)



############### TAUTOLOGIES AND ANTILOGIES ########

class Truth(Formula):
    """docstring for Truth"""
    def __init__(self):
        super(Truth, self).__init__()

    def evaluate_aux(self, assignment, vm, variables = dict(), free_vars = list()):
        return np.ones(assignment.shape[0], dtype = "bool")

    def display_aux(self, latex):
        if latex:
            return r"\textsf{true}"
        else:
            return "true"


class Falsity(Formula):
    """docstring for Falsity"""
    def __init__(self):
        super(Falsity, self).__init__()

    def evaluate_aux(self, assignment, vm, variables = dict(), free_vars = list()):
        return np.zeros(assignment.shape[0], dtype = "bool")

    def display_aux(self, latex):
        if latex:
            return r"\textsf{true}"
        else:
            return "true"

class Named(Formula):
    def __init__(self, name, child, latex_name = None):
        super(Named, self).__init__(child)
        self.name       = name
        self.latex_name = latex_name if latex_name is not None else self.name

    def evaluate_aux(self, *args, **kwargs):
        return self.children[0].evaluate_aux(*args, **kwargs)

    def display_aux(self, latex):
        if latex:
            return self.latex_name
        else:
            return self.name

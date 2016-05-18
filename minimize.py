#!/usr/bin/env python

from pyeda.inter import *

class RB:
    def __init__(self, n):
        self.n = n
        self.var = exprvar(str(id(self)))
        self.expr = self.var
    def __xor__(self, other):
        result = RB(self.n)
        result.expr = Xor(self.expr, other.expr)
        return result

u = RB(8)
v = RB(8)
w = u ^ u

fill = Or(w.expr, exprvar('dummy'))
f1m = espresso_exprs(fill.to_dnf())
print(f1m[0])

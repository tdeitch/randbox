# RandBytes
# RandBytes(n): generate n random bytes
# len(RandBytes): length, in bytes
# .entropy(): entropy of the number, in bits
# .unwrap(): returns the raw bits
# &, |, ^, ~: bitwise AND, OR, XOR, and NOT 

import os
import math
from bitarray import bitarray

class RandBytes:
    def __init__(self, n):
        self._wrapped = True
        self._i = bitarray(endian='big')
        self._i.frombytes(os.urandom(n))
        self._n = n
        self._pr_one = [.5] * (n * 8)
    def __len__(self):
        if not self._wrapped:
            raise RuntimeError
        return self._n
    def entropy(self):
        return sum([min_entropy(i) for i in self._pr_one])
    def unwrap(self):
        self._wrapped = False
        return self._i
    def __and__(self ,other):
        if not self._wrapped:
            raise RuntimeError
        if isinstance(other, bitarray):
            if len(self._i) != len(other):
                raise ValueError
            newRB = RandBytes(len(self))
            newRB._i = self._i & other
            newRB._pr_one = self._pr_one[:]
            for i in range(len(self)*8):
                if not other[i]:
                    newRB._pr_one[i] = 0
            self._wrapped = False
            return newRB
        elif isinstance(other, RandBytes):
            if len(self) != len(other):
                raise ValueError
            newRB = RandBytes(len(self))
            newRB._i = self._i & other._i
            newRB._pr_one = self._pr_one[:]
            if id(self) != id(other):
                for i in range(len(self)*8):
                    newRB._pr_one[i] = self._pr_one[i] * other._pr_one[i]
            self._wrapped = False
            other._wrapped = False
            return newRB
        else:
            raise TypeError
    def __or__(self ,other):
        if not self._wrapped:
            raise RuntimeError
        if isinstance(other, bitarray):
            if len(self._i) != len(other):
                raise ValueError
            newRB = RandBytes(len(self))
            newRB._i = self._i | other
            newRB._pr_one = self._pr_one[:]
            for i in range(len(self)*8):
                if other[i]:
                    newRB._pr_one[i] = 1
            self._wrapped = False
            return newRB
        elif isinstance(other, RandBytes):
            if len(self) != len(other):
                raise ValueError
            newRB = RandBytes(len(self))
            newRB._i = self._i | other._i
            newRB._pr_one = self._pr_one[:]
            if id(self) != id(other):
                for i in range(len(self)*8):
                    newRB._pr_one[i] = 1 - ((1 - self._pr_one[i]) * (1 - other._pr_one[i]))
            self._wrapped = False
            other._wrapped = False
            return newRB
        else:
            raise TypeError
    def __xor__(self ,other):
        if not self._wrapped:
            raise RuntimeError
        if isinstance(other, bitarray):
            if len(self._i) != len(other):
                raise ValueError
            newRB = RandBytes(len(self))
            newRB._i = self._i ^ other
            newRB._pr_one = self._pr_one[:]
            for i in range(len(self)*8):
                if other[i]:
                    newRB._pr_one[i] = 1 - newRB._pr_one[i]
            self._wrapped = False
            return newRB
        elif isinstance(other, RandBytes):
            if len(self) != len(other):
                raise ValueError
            newRB = RandBytes(len(self))
            newRB._i = self._i ^ other._i
            newRB._pr_one = self._pr_one[:]
            if id(self) == id(other):
                newRB._pr_one = [0] * len(self._i)
            else:
                for i in range(len(self)*8):
                    newRB._pr_one[i] = self._pr_one[i] * (1 - other._pr_one[i]) + other._pr_one[i] * (1 - self._pr_one[i])
            self._wrapped = False
            other._wrapped = False
            return newRB
        else:
            raise TypeError
    def __invert__(self):
        if not self._wrapped:
            raise RuntimeError
        newRB = RandBytes(len(self))
        newRB._i = ~ self._i
        newRB._pr_one =  [1 - i for i in self._pr_one]
        self._wrapped = False
        return newRB

def shannon_entropy(pr):
    if pr == 0 or (1-pr) == 0:
        return 0
    return -1 * (pr * math.log(pr,2) + (1-pr) * math.log(1-pr,2))

def min_entropy(pr):
    if pr == 0 or (1-pr) == 0:
        return 0
    if pr > .5:
        return -1 * math.log(pr, 2)
    return -1 * math.log(1-pr, 2)

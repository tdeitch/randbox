#!/usr/bin/env python3

from pyrand import RandBytes
from bitarray import bitarray

def otp(msg):
    m = bitarray(endian='big')
    m.frombytes(msg.encode('utf-8'))
    key = RandBytes(len(msg.encode('utf-8')))
    assert(key.entropy() == len(m))
    c = (key ^ m)
    assert(c.entropy() == len(m))
    rc = c.unwrap()
    rkey = key.unwrap()
    print('Encrypted message:', rc)
    print('Bytes:', len(m))
    print('Decrypted message:', bxor(rc, rkey).decode('utf-8'))

def selfXor():
    i = RandBytes(4)
    j = i ^ i
    assert(j.entropy() == 0)

def newAnd():
    i = RandBytes(8)
    j = RandBytes(8)
    k = i & j
    assert(k.entropy() > 24 and k.entropy() < 28)

def main():
    otp('this is interesting')
    otp('☃')
    selfXor()
    newAnd()

def bxor(a, b):
    result = bytearray(a)
    for i, bt in enumerate(b):
        result[i] ^= bt
    return bytes(result)

if __name__ == "__main__":
    main()

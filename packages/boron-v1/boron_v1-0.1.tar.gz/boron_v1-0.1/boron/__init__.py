import ctypes
import os
c_lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), "c_lib.dll"))

def mul(*args):
    return c_lib.mul(*args)

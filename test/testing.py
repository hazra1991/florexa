
# __all__ = ["var1","var1","normal" ,"__privet"]
var1 = 1
var2 = 2

class _privet:
    def __init__(self):
        print("private class")

import functools
print("testing ")
class Errors:

    class SchemaError(Exception):
        pass

    class DuplicateKeyErr(Exception):
        pass

class myclass:
    def dis(self):
        if True:
            raise Errors.SchemaError ("dsnkjdnakjdanjk")
        

class A(object):
    def __init__(self):
        for i in range(10):
            if not hasattr(self, "__foo"):
                self.__foo = True
                print "__foo"

print dir(A())
from Py3dsMax import mxs

class Box(object):
    def __init__(self, position, **kwargs):
        self.max_object = mxs.box(length=0.08,
                                  width=0.08,
                                  height=0.08,
                                  pos=position.to_point3())
        for key, value in kwargs.items():
            setattr(self.max_object, key, value)
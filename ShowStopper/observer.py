__author__ = 'Jason Orendorff'

# Taken from StackOverflow:
# http://stackoverflow.com/questions/1904351/python-observer-pattern-examples-tips
# use self.fire(type="progress", percent=50) for example

class Event(object):
    pass

class Observable(object):
    def __init__(self):
        self.callbacks = []
    def subscribe(self, callback):
        self.callbacks.append(callback)
    def fire(self, **attrs):
        e = Event()
        e.source = self
        for k, v in attrs.iteritems():
            setattr(e, k, v)
        for fn in self.callbacks:
            fn(e)
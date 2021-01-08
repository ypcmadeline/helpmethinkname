from PySide2.QtCore import QObject, Property, Signal


class property(QObject):


    def __init__(self, initr=None, inits=None):
        QObject.__init__(self)
        if initr is None:
            initr = ["0,0,0"]
        self.range = initr
        if inits is None:
            inits = [False]
        self.sweep = inits
        self.observers = []



    def setname(self, val):
        self.name = val

    def readname(self):
        return self.name

    def readrlist(self):
        return self.range

    def setrlist(self, val):
        self.range = val
        for callback in self.observers:
            callback()

    def readslist(self):
        return self.sweep

    def setslist(self, val):
        self.sweep = val
        for callback in self.observers:
            callback()

    def bind_to(self, callback):
        self.observers.append(callback)

    saverange = Property(list, readrlist, setrlist)
    savesweep = Property(list, readslist, setslist)
    savename = Property(str, readname, setname)




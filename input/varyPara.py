class VaryPara:

    def __init__(self, name, range, sweep):
        self.name = name
        self.range = range
        # self.range.append(range)
        self.sweep = sweep
        # self.sweep.append(sweep)

    def getName(self):
        return self.name

    def getRange(self):
        return self.range

    def getSweep(self):
        return self.sweep

    def setName(self, name):
        self.name = name

    def addRange(self, range):
        self.range.append(range)

    def addSweep(self, sweep):
        self.sweep.append(sweep)
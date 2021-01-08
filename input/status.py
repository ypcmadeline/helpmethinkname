class Status:

    def __init__(self, name):
        self.name = name
        self.range = []
        self.sweep = []

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
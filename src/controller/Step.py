class Step:
    def __init__(self, initStep, max):
        self._step = initStep
        self.MAX = max

    def increase(self):
        self._step = int(self._step + 1)

    def decrease(self):
        self._step = int(self._step - 1)

    def setStep(self, step):
        self._step = step

    def getStep(self):
        return self._step

    def isMAX(self):
        return self._step == self.MAX

    def reset(self):
        self._step = 0

    def setMax(self, max):
        self.MAX = max

    def setToMax(self):
        self._step = self.MAX

    def printStep(self):
        print("Step: " + str(self._step))

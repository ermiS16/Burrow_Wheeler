class Speed:
    def __init__(self):
        self._speedFactor = 1

    def update(self, factor):
        self._speedFactor = factor

    def getFactor(self):
        return self._speedFactor

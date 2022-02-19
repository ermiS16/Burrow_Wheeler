class Speed:
    def __init__(self):
        self._speed_factor = 1

    def update(self, factor):
        self._speed_factor = factor

    def getFactor(self):
        return self._speed_factor

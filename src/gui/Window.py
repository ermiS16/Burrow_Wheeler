class Window:
    def __init__(self, screen):

        self._windowWidth = 0
        self._windowHeight = 0

        self.screen_resolution = screen.geometry()
        self._screenWidth, self._screenHeight = self.screen_resolution.width(), self.screen_resolution.height()
        self._windowWidth, self._windowHeight = self.screen_resolution.width(), self.screen_resolution.height()
        print(str(self._screenWidth) + ", " + str(self._screenHeight))

    def getWindowWidth(self):
        return self._windowWidth

    def getWindowHeight(self):
        return self._windowHeight

    def getScreenWidth(self):
        return self._screenWidth

    def getScreenHeight(self):
        return self._screenHeight

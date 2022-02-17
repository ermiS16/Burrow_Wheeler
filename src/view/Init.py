from model.Description import DESC
from view.Content import Content


class Init(Content):
    def __init__(self, arg1):
        super(Init, self).__init__(self)

    def initContent(self):
        self.initDescription(DESC.init)

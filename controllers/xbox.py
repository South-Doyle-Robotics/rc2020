from .controller import Controller
from traits import implements
from wpilib import Joystick

@implements(Controller)
class Xbox:
    def __init__(self, port):
        self.controller = Joystick(port)

    def forward(self):
        # return self.controller.getAxis(1)
        return 0

    def turn(self):
        # return self.controller.getAxis(4)
        return 0
from traits import implements, Controller

@implements(Controller)
class ShooterController:
    def __init__(self, port): self.joystick = Joystick(port)
    def get_joystick(self): return self.joystick
    axis = Controller.axis
    button = Controller.button

    shoot = button(1)
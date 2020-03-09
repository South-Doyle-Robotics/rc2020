from traits import implements, Controller
from wpilib import Joystick


@implements(Controller)
class DriverController:
    def __init__(self, port): self.joystick = Joystick(port)
    def get_joystick(self): return self.joystick
    axis = Controller.axis
    button = Controller.button

    # Chassis
    forward = axis(1)
    turn = axis(2)
    hood = axis(3)
    shift = button(1)

    # Turret and Singulator
    shoot = button(2)
    intake = button(3)

    # Turret and Singulator
    clear_jam = button(4)
    deploy_climb = button(9)
    lower_climb = button(10)
    retract_climb = button(11)
    extend_climb = button(12)

from traits import implements, Controller
from wpilib import Joystick


@implements(Controller)
class JoystickController:
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


@implements(Controller)
class XBoxController:
    def __init__(self, port): self.joystick = Joystick(port)
    def get_joystick(self): return self.joystick
    axis = Controller.axis
    button = Controller.button

    # Chassis
    forward = axis(1)
    turn = axis(4)
    shift = button(10)

    # Turret and Singulator
    shoot = button(1) # A button
    intake = button(6)
    clear_jam = button(5)
    hood_increase = button(3) # X button
    hood_decrease = button(4) # Y button
    turret_increase = button(7) # Back button
    turret_decrease = button(8) # Start button

    # Climber
    # lower_climb = button(7) # Back button
    # deploy_climb = button(8) # Start button
    # retract_climb = button(3) # X button
    # extend_climb = button(4) # Y button

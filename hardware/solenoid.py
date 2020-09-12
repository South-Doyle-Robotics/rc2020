from constants import PCM_ID
from wpilib import DoubleSolenoid as WPI_DoubleSolenoid, Compressor
from tools import Timed

Compressor(PCM_ID)


class DoubleSolenoid(WPI_DoubleSolenoid, Timed):
    def __init__(self, forward_channel, reverse_channel):
        super().__init__(PCM_ID, forward_channel, reverse_channel)

    def forward(self):
        self.set(self.Value.kForward)

    def reverse(self):
        self.set(self.Value.kReverse)

    def delayed_forward(self, seconds):
        self.do(self.forward, seconds)

    def delayed_reverse(self, seconds):
        self.do(self.reverse, seconds)

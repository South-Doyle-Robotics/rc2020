from constants import PCM_ID
from wpilib import DoubleSolenoid as WPI_DoubleSolenoid, Compressor

Compressor(PCM_ID)

class DoubleSolenoid(WPI_DoubleSolenoid):
    def __init__(self, forward_channel, reverse_channel):
        super().__init__(PCM_ID, forward_channel, reverse_channel)
    
    def forward(self):
        self.set(self.Value.kForward)
    
    def reverse(self):
        self.set(self.Value.kReverse)
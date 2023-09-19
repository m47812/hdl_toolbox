from enum import IntEnum


class SignalDirection:
    In = 0
    Out = 1
    InOut = 2

class Signal:
    def __init__(self, name, signal_type, direction : SignalDirection = None):
        self.name = name
        self.signal_type = signal_type
        self.direction : SignalDirection = direction

    @property
    def EntityString(self):
        raise NotImplemented("EntityString is not defined for the base class")

    @property
    def InstanceString(self):
        raise NotImplemented("InstanceString is not defined for the base class")

class VHDLSignal(Signal):
    def __init__(self, name, signal_type, direction : SignalDirection = None):
        super.__init__(name, signal_type, direction)

    @property
    def EntityString(self):
        if self.direction is None:
            return self.name + " : " + self.direction.String
        else:
            return self.name + " : " + str(self.direction) + " " + self.direction.String
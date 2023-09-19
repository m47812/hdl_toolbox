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
    def entity_string(self):
        raise NotImplemented("EntityString is not defined for the base class")

    def instance_string(self):
        raise NotImplemented("InstanceString is not defined for the base class")
    def instance_string(self, connected_signal):
        raise NotImplemented("InstanceString is not defined for the base class")

    @property
    def declaration_string(self):
        raise NotImplemented("declaration_string is not defined for the base class")

class VHDLSignal(Signal):
    def __init__(self, name, signal_type, direction : SignalDirection = None):
        super.__init__(name, signal_type, direction)

    @property
    def entity_string(self):
        if self.direction is None:
            return self.name + " : " + self.signal_type.string
        else:
            return self.name + " : " + str(self.direction) + " " + self.signal_type.string

    def instance_string(self):
        return self.name + " => #X"

    def instance_string(self, connected_signal:Signal):
        return self.name + " => " + connected_signal.name

    @property
    def declaration_string(self):
        return "signal " + self.name + " : " + self.signal_type.string

class VerilogSignal(Signal):
    def __init__(self, name, signal_type, direction : SignalDirection = None):
        super.__init__(name, signal_type, direction)

    @property
    def entity_string(self):
        direction_str = ""
        if self.direction == SignalDirection.In:
            direction_str = "input "
        elif self.direction == SignalDirection.Out:
            direction_str = "output "
        elif self.direction == SignalDirection.InOut:
            direction_str = "inout "
        return direction_str + self.signal_type.string + self.name

    def instance_string(self):
        return "." + self.name + "(#X)"

    def instance_string(self, connected_signal:Signal):
        return "." + self.name + "(" + connected_signal.name + ")"

    @property
    def declaration_string(self):
        return "wire " + self.signal_type.string + self.name
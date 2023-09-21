class SignalRange:
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def __str__(self):
        raise NotImplementedError("SignalRange.__str__ is not defined for the base class")

class VHDLSignalRange(SignalRange):
    def __init__(self, lower, upper, to_type):
        super().__init__(lower, upper)
        self.to_type = to_type

    def __str__(self):
        if self.to_type == "downto":
            return self.upper + " downto " + self.lower
        elif self.to_type == "to":
            return self.lower + " to " + self.upper
        else:
            raise ValueError(f"to_type was not of valid value it was: {self.to_type}")

class VerilogSignalRange(SignalRange):
    def __init__(self, lower, upper):
        super().__init__(lower, upper)

    def __str__(self):
        return self.upper + ":" + self.lower
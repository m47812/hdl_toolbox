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

class SignalType:
    def __init__(self, type_name, range:SignalRange=None):
        self.name = type_name
        self.range = range

    @property
    def string(self):
        raise NotImplementedError("SignalType.string is not defined for the base class")

class VHDLSignalType(SignalType):
    def __init__(self, type_name, range:SignalRange=None):
        super().__init__(type_name, range)

    def __int__(self, verilog_type):
        raise NotImplementedError("Type Cast of signal types is not currently implemented")

    @property
    def string(self):
        if self.range is None:
            return self.name
        else:
            raise NotImplementedError("VHDL Uses different variants of range spec thefore needs to be defined in inherenting class")

class VHDLVectorSignalType(VHDLSignalType):
    def __init__(self, type_name, range:SignalRange=None):
        super().__init__(type_name, range)

    def __int__(self, verilog_type):
        super().__int__(verilog_type)

    @property
    def string(self):
        return self.name + "(" + str(self.range) + ")"

class VHDLRangeSignalType(VHDLSignalType):
    def __init__(self, type_name, range:SignalRange=None):
        super().__init__(type_name, range)

    def __int__(self, verilog_type):
        super().__int__(verilog_type)

    @property
    def string(self):
        return self.name + " range " + str(self.range)

class VerilogSignalType(SignalType):
    def __init__(self, type_name, range:SignalRange=None):
        super().__init__(type_name, range)

    def __int__(self, vhdl_type):
        raise NotImplementedError("Type Cast of signal types is not currently implemented")

    @property
    def string(self):
        if self.range is None:
            return ""
        else:
            return "[" + str(self.range) + "] "
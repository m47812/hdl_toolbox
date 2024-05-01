from .signal_range import SignalRange

class SignalType:
    def __init__(self, type_name, range:SignalRange=None):
        self.name = type_name
        self.range = range

    @property
    def string(self):
        raise NotImplementedError("SignalType.string is not defined for the base class")
    def to_verilog(self):
        raise NotImplementedError("Can not be executed in the base class")
    def to_vhdl(self):
        raise NotImplementedError("Can not be executed in the base class")

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
    def to_verilog(self):
        return VerilogSignalType(is_signed=False, range=None)
    def to_vhdl(self):
        return self

class VHDLVectorSignalType(VHDLSignalType):
    def __init__(self, type_name, range:SignalRange=None):
        super().__init__(type_name, range)

    @property
    def string(self):
        return self.name + "(" + str(self.range) + ")"
    def to_verilog(self):
        if self.name.lower() == "signed":
            return VerilogSignalType(is_signed=True, range=self.range.to_verilog())
        else:
            return VerilogSignalType(is_signed=False, range=self.range.to_verilog())

class VHDLRangeSignalType(VHDLSignalType):
    def __init__(self, type_name, range:SignalRange=None):
        super().__init__(type_name, range)

    @property
    def string(self):
        return self.name + " range " + str(self.range)
    def to_verilog(self):
        raise ValueError(f"Range types are not supported for conversion to Verilog: {self.name}")

class VerilogSignalType(SignalType):
    def __init__(self, is_signed, range:SignalRange=None):
        super().__init__(type_name=None, range=range)
        self.is_signed = is_signed

    @property
    def string(self):
        type_str = ""
        if self.is_signed:
            type_str += "signed "
        if not self.range is None:
            type_str += "[" + str(self.range) + "] "
        return type_str
    def to_verilog(self):
        return self
    def to_vhdl(self, is_parameter=False):
        if self.is_signed and not self.range is None:
            return VHDLVectorSignalType("signed", self.range.to_vhdl())
        elif not self.range is None:
            return VHDLVectorSignalType("std_logic_vector", self.range.to_vhdl())
        elif is_parameter:
            return VHDLSignalType("integer")
        else:
            return VHDLSignalType("std_logic")
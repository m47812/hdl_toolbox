import re

class SignalRange:
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def __str__(self):
        raise NotImplementedError("SignalRange.__str__ is not defined for the base class")
    def to_verilog(self):
        raise NotImplementedError("Can not be executed in the base class")
    def to_vhdl(self):
        raise NotImplementedError("Can not be executed in the base class")

class VHDLSignalRange(SignalRange):
    def __init__(self, signal_str=None, lower=None, upper=None, to_type=None):
        if signal_str is None:
            super().__init__(lower, upper)
            self.to_type = to_type
        else:
            if "downto" in signal_str:
                upper = re.findall(r'(?<=\().+?(?=downto)', signal_str, re.IGNORECASE)[0].strip()
                lower = re.findall(r'(?<=downto).+(?=\))', signal_str, re.IGNORECASE)[0].strip()
                range_type = "downto"
            elif "to" in signal_str:
                lower = re.findall(r'.+?(?=to)', signal_str, re.IGNORECASE)[0].strip()
                upper = re.findall(r'(?<=to).+', signal_str, re.IGNORECASE)[0].strip()
                range_type = "to"
            else:
                raise ValueError("Invalid range expression")
            super().__init__(lower, upper)
            self.to_type = range_type  
        
    def __str__(self):
        if self.to_type == "downto":
            return self.upper + " downto " + self.lower
        elif self.to_type == "to":
            return self.lower + " to " + self.upper
        else:
            raise ValueError(f"to_type was not of valid value it was: {self.to_type}")
        
    def to_verilog(self):
        if self.to_type == "downto":
            return VerilogSignalRange(self.lower, self.upper)
        else:
            raise ValueError(f"Signal range with expression \"to\" are not currently supported for conversion to Verilog (use downto instead)")
    def to_vhdl(self):
        return self

class VerilogSignalRange(SignalRange):
    def __init__(self, lower, upper):
        super().__init__(lower, upper)

    def __str__(self):
        return self.upper + ":" + self.lower
    def to_verilog(self):
        return self
    def to_vhdl(self):
        return VHDLSignalRange(lower=self.lower, upper=self.upper, to_type="downto")
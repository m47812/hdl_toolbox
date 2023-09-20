class HDL_Module:
    def __init__(self):
        self.signals = []

    def from_source_code(self, source):
        raise NotImplementedError("from_source_code can not be executed in the base class")

    def _extract_signal_strings(self, source):
        raise NotImplementedError("from_source_code can not be executed in the base class")

    def _separate_signal_into_subcomponents(self, signal_str):
        raise NotImplementedError("_separate_signal_into_subcomponents can not be executed in the base class")
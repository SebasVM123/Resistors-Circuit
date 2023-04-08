class Block:
    def __init__(self):
        self.resistors = []
        self.RE = 0
        self.VE = 0

    def addResistor(self, resistor):
        self.resistors.append(resistor)

    def getRE(self):
        REInv = 0
        for R in self.resistors:
            REInv = REInv + (1 / R.ohm)

        self.RE = 1 / REInv
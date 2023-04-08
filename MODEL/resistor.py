class Resistor:
    def __init__(self, ohm=0, V=0, I=0):
        self.ohm = ohm
        self.V = V
        self.I = I

    def getVoltage(self):
        self.V = self.ohm * self.I

    def getCurrent(self):
        self.I = self.V / self.ohm
from MODEL.block import *
from MODEL.resistor import *
import schemdraw as schem
import schemdraw.elements as e
from PIL import Image


class Circuit:
    def __init__(self, VT=0):
        self.blocks = []
        self.VT = VT
        self.IT = 0
        self.RE = 0

    def addBlock(self, block):
        self.blocks.append(block)

    def solve(self):
        for B in self.blocks:
            B.getRE()
            self.RE = self.RE + B.RE

        self.IT = round((self.VT / self.RE), 4)
        for B in self.blocks:
            B.VE = round((B.RE * self.IT), 4)
            for R in B.resistors:
                R.V = round(B.VE, 4)
                R.I = round(R.V / R.ohm, 4)

    def drawBlock(self, pos):
        numRes = len(self.blocks[pos].resistors)
        n = 2 * (numRes + 1)
        HLines = []
        d = schem.Drawing()

        LV1 = d.add(e.LINE, d='up', l=4)

        for i in range(1, n + 1):
            if i != ((n / 2) + 1):
                l = d.add(e.LINE, d='right', l=2)
            elif i == ((n / 2) + 1):
                l = d.add(e.LINE, d='right', xy=LV1.start, l=2)
            HLines.append(l)

        LV2 = d.add(e.LINE, d='up', l=4)

        i = 0
        for R in self.blocks[pos].resistors:
            txt = '$R_' + str(i + 1) + '$'
            I = str(R.I) + 'A'
            res = d.add(e.Resistor(d='down', xy=HLines[i].end).length(4).label(txt, loc='top'))
            current = d.add(e.CurrentLabel().at(res).label(I, rotate=True, loc='bottom', fontsize=10).scale(0.7))
            i += 1

        d.save('temp/block.png', dpi=100)

    def drawSchem(self):
        graph = schem.Drawing()

        l1 = graph.add(e.LINE, d='right', l=6)

        i = 1
        for B in self.blocks:
            V = str(B.VE) + 'V'
            txt = 'B' + str(i)
            block = graph.add(e.SourceControlled(d='down').label(V, rotate=True, loc='bot').label(txt, loc='top'))
            current = graph.add(e.CurrentLabelInline(direction='in').at(block))
            i += 1

        #l = graph.add(e.LINE, d='down', l=8)

        l2 = graph.add(e.LINE, d='left', l=6)
        V = graph.add(e.Battery(d='up', toy=l1.start).label(str(self.VT) + 'V', rotate=True, loc='bot'))
        IT = graph.add(e.CurrentLabel().at(V).label(str(self.IT) + 'A', rotate=True, loc='top').scale(0.7))

        graph.save('temp/schem.png', dpi=130)

        img = Image.open(r'temp/schem.png')
        width, height = img.size
        imgCrop = img.crop((0, 16, width, height - 17))
        imgCrop.save('temp/schemCrop.png')


'''R11 = Resistor(500)
R12 = Resistor(100)
R13 = Resistor(200)

B1 = Block()
B1.addResistor(R11)
B1.addResistor(R12)
B1.addResistor(R13)

R21 = Resistor(1000)
R22 = Resistor(1200)
R23 = Resistor(1700)
R24 = Resistor(2000)

B2 = Block()
B2.addResistor(R21)
B2.addResistor(R22)
B2.addResistor(R23)
B2.addResistor(R24)

circuit = Circuit(10)
circuit.addBlock(B1)
circuit.addBlock(B2)
circuit.solve()
circuit.download()'''

'''i = 1
for B in circuit.blocks:
    print('Bloque ', i)

    j = 1
    for R in B.resistors:
        print('Resistencia ', j, ': ', R.V, 'V, ', R.I, 'A.', sep='')
        j += 1

    i += 1'''

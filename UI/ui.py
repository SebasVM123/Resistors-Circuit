import sys
from MODEL.circuit import *
from PyQt5 import uic, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        with open("styles.qss") as f:
            self.setStyleSheet(f.read())

        self.move(0, 30)

        self.circuit = Circuit()
        self.aux = 1

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.widgetButtons = QWidget()
        self.widgetButtons.setLayout(self.mainLayout)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widgetButtons)

        self.lineEditRes.hide()
        self.pushButtonRes.hide()
        self.pushButtonFinish.hide()

        self.pushButtonCalcular.setEnabled(False)
        self.pushButtonCrear.clicked.connect(self.createBlock)
        self.pushButtonRes.clicked.connect(self.createResistor)
        self.pushButtonFinish.clicked.connect(self.reset)
        self.pushButtonCalcular.clicked.connect(self.solve)
        self.pushButtonVol.clicked.connect(self.start)
        self.pushButtonCrear.setEnabled(False)

    def start(self):
        self.circuit.VT = int(self.lineEditVol.text())
        self.pushButtonCrear.setEnabled(True)
        self.lineEditVol.hide()
        self.labelVol.hide()
        self.pushButtonVol.hide()

    def createBlock(self):
        block = Block()
        self.circuit.addBlock(block)

        self.pushButtonCrear.setEnabled(False)
        self.labelRes.setText('Ingrese la resistencia de R' + str(self.aux) + ':')
        self.lineEditRes.show()
        self.pushButtonRes.show()
        self.pushButtonFinish.show()

    def createResistor(self):
        ohm = float(self.lineEditRes.text())
        self.lineEditRes.clear()
        r = Resistor(ohm)
        self.circuit.blocks[-1].addResistor(r)

        self.aux += 1
        self.labelRes.setText('Ingrese la resistencia de R' + str(self.aux) + ':')

    def reset(self):
        self.aux = 1
        self.pushButtonCrear.setEnabled(True)
        self.labelRes.setText('')
        self.lineEditRes.hide()
        self.pushButtonRes.hide()
        self.pushButtonFinish.hide()

        self.pushButtonCalcular.setEnabled(True)

    def solve(self):
        self.pushButtonCrear.hide()
        self.pushButtonCalcular.setEnabled(False)
        self.circuit.solve()
        self.circuit.drawSchem()

        if len(self.circuit.blocks) == 1:
            height = 2 * int(Image.open('temp/schemCrop.png').height)
        else:
            height = int((Image.open('temp/schemCrop.png').height)/len(self.circuit.blocks))

        self.widgetButtons.setStyleSheet('.QWidget{background-image: url(temp/schemCrop.png); '
                                         'background-repeat: no-repeat; background-position: left}')

        for i in range(len(self.circuit.blocks)):
            buttonGrBx = QGroupBox()
            buttonGrBx.setFixedHeight(height)

            buttonLayout = QHBoxLayout()
            buttonLayout.setAlignment(Qt.AlignRight)

            button = QPushButton()
            button.setStyleSheet('QPushButton{image: url(lupa.png); border-radius: 15px; '
                                 'background-color: rgb(91, 75, 61);}')
            button.setCursor(Qt.PointingHandCursor)
            button.setObjectName(str(i))
            button.setFixedSize(30, 30)
            button.clicked.connect(self.zoom)

            spacer = QLabel('')
            if len(self.circuit.blocks) > 2: spacer.setFixedWidth(80)
            else: spacer.setFixedWidth(95)
            spacer.setStyleSheet('QLabel{background: transparent;}')

            buttonLayout.addWidget(button)
            buttonLayout.addWidget(spacer)
            buttonGrBx.setLayout(buttonLayout)

            buttonGrBx.setStyleSheet('.QGroupBox{background: transparent; border: 0;}')

            self.mainLayout.addWidget(buttonGrBx)

    def zoom(self):
        button = self.sender()
        self.circuit.drawBlock(int(button.objectName()))

        img = Image.open('temp/block.png')
        width, height = img.size


        zoom = PopUp([width, height])
        zoom.setWindowTitle('Bloque ' + str(int(button.objectName()) + 1))
        zoom.show()
        zoom.exec_()

class PopUp(QDialog):
    def __init__(self, size):
        super().__init__()

        with open("styles.qss") as f:
            self.setStyleSheet(f.read())

        self.move(571, 300)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)


        self.setFixedSize(size[0] + 30, size[1] + 30)
        self.VLayout = QVBoxLayout()
        self.VLayout.setAlignment(Qt.AlignTop)

        self.groupBox = QGroupBox()
        self.groupBox.setFixedSize(size[0], size[1])
        self.groupBox.setContentsMargins(0, 0, 0, 0)
        self.groupBox.setStyleSheet('QGroupBox{background-image: url(temp/block.png); border: 0;}')
        self.VLayout.addWidget(self.groupBox)

        self.setLayout(self.VLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = MainWindow()
    GUI.show()
    sys.exit(app.exec_())
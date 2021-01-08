import os
import re

from PyQt5 import QtCore, QtWidgets
import library.motor as motor
import input.ErrorPane as ErrorPane

class guimotor(object):

    def __init__(self):
        # self.motor = motor.motor()
        self.reset_num = 0


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 30, 50, 16))
        self.label.setText("Motor")
        self.label.adjustSize()
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 30, 500, 300))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.anglelabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.anglelabel.setText("Current angle: " )
        self.gridLayout.addWidget(self.anglelabel, 0, 0, 1, 1)

        self.resetbtn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.resetbtn.setText("Reset Angle")
        self.resetbtn.clicked.connect(lambda: self.reset())
        self.gridLayout.addWidget(self.resetbtn, 1, 0, 1, 1)

        self.rotatelabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.rotatelabel.setText("Rotate to: ")
        self.gridLayout.addWidget(self.rotatelabel, 3, 0, 1, 1)

        self.rotate = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.rotate, 3, 1, 1, 1)

        self.speedlabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.speedlabel.setText("Speed: ")
        self.gridLayout.addWidget(self.speedlabel, 2, 0, 1, 1)

        self.speed = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.speed.addItem("1")
        self.speed.addItem("1/2")
        self.speed.addItem("1/4")
        self.speed.addItem("1/8")
        self.speed.addItem("1/16")
        self.speed.currentTextChanged.connect(lambda: self.changespeed())
        self.gridLayout.addWidget(self.speed, 2, 1, 1, 1)

        self.setbtn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.setbtn.setText("Apply")
        self.setbtn.clicked.connect(lambda: self.set())
        self.gridLayout.addWidget(self.setbtn, 4, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 422, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def update(self):
        self.anglelabel.setText("Current angle: " + str(self.motor.angle))

    def reset(self):
        self.motor.return_zero()
        self.update()

    def changespeed(self):
        self.motor.speed_mode(self.speed.currentText())
        # print("self.speed.currentText()")

    def set(self):
        # self.motor.rotation(int(self.rotate.text()))
        angle = self.rotate.text()
        try:
            a = float(angle)
        except:
            self.popErrorWindow("Angle should be numeric")
        self.checkboundary(float(angle), "Angle")
        try:
            print("set angle")
            # self.motor.rotation(a)
        except:
            self.popErrorWindow("Seems something wrong with rotation angle. Please check again.")

    def popErrorWindow(self, msg):
        self.window = QtWidgets.QMainWindow()
        self.ui = ErrorPane.error(msg)
        self.ui.setupUi(self.window)
        self.window.show()

    def checkboundary(self, num, name):
        try:
            cur_path = os.path.dirname(__file__)
            new_path = os.path.join(cur_path, '..','input', 'boundary.txt')
            file1 = open(new_path, "r+")
            text = file1.readlines()
            for i in range(len(text)):
                text[i] = text[i].replace('\n', '')
                x = re.split("<=|>=|<|>", text[i])
                y = re.findall("<=|>=|<|>", text[i])
                y = y[0]
                if name == x[0]:
                    if y == ">":
                        if not float(num) > float(x[1]):
                            file1.close()
                            self.popErrorWindow(
                                "Warning: Value of " + name + " should > " + str(x[1]))
                            return False
                    if y == "<":
                        if not float(num) < float(x[1]):
                            file1.close()
                            self.popErrorWindow(
                                "Warning: Value of " + name + " should < " + str(x[1]))
                            return False
                    if y == ">=":
                        if not float(num) >= float(x[1]):
                            file1.close()
                            self.popErrorWindow(
                                "Warning: Value of " + name + " should >= " + str(x[1]))
                            return False
                    if y == "<=":
                        if not float(num) <= float(x[1]):
                            file1.close()
                            self.popErrorWindow(
                                "Warning: Value of " + name + " should <= " + str(x[1]))
                            return False
            file1.close()
            return True
        except:
            self.popErrorWindow("Fail to read boundary.txt")
            return False






if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    setParameter = QtWidgets.QMainWindow()
    ui = guimotor()
    ui.setupUi(setParameter)
    setParameter.show()
    sys.exit(app.exec_())

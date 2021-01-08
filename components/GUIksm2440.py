import os
import re

from PyQt5 import QtCore, QtWidgets
import library.keithley_2440 as keithley_2440
import input.ErrorPane as ErrorPane
class ksm2440(object):

    def __init__(self):
        # self.ksm2440 = keithley_2440.keithley_2440()
        self.reset_num = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 30, 171, 16))
        self.label.setText("Keithley Source Meter 2440")
        self.label.adjustSize()
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 30, 500, 500))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.curlabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.curlabel.setText("Current(A)")
        self.gridLayout.addWidget(self.curlabel, 1, 0, 1, 1)

        self.current = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.current, 1, 1, 1, 1)

        self.comlabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.comlabel.setText("Compliance(V)")
        self.gridLayout.addWidget(self.comlabel, 2, 0, 1, 1)

        self.compliance = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.compliance, 2, 1, 1, 1)

        self.setbtn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.setbtn.setText("Apply")
        self.setbtn.clicked.connect(lambda: self.set())
        self.gridLayout.addWidget(self.setbtn, 3, 1, 1, 1)

        self.outputbtn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.outputbtn.setText("Output: OFF")
        self.outputbtn.clicked.connect(lambda: self.output())
        self.gridLayout.addWidget(self.outputbtn, 4, 1, 1, 1)

        self.resetbtn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.resetbtn.setText("Reset")
        self.resetbtn.clicked.connect(lambda: self.reset())
        self.gridLayout.addWidget(self.resetbtn, 0, 0, 1, 1)

        self.resetlabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.resetlabel.setText("")
        self.gridLayout.addWidget(self.resetlabel, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 422, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def output(self):
        if self.outputbtn.text() == "Output: ON":
            # self.ksm2440.output(False)
            self.outputbtn.setText("Output: OFF")
        else:
            # self.ksm2440.output(True)
            self.outputbtn.setText("Output: ON")

    def reset(self):
        # self.ksm2440.reset()
        if self.reset_num != 0:
            self.resetlabel.setText("Reset("+str(self.reset_num)+")")
        else:
            self.resetlabel.setText("Reset")
        self.reset_num = self.reset_num + 1

    def set(self):
        current = self.current.text()
        compliance = self.compliance.text()
        if current != "":
            try:
                c = float(current)
            except:
                self.popErrorWindow("Current should be numeric")
                return
            if not self.checkboundary(float(current), "Keithley 2440 cur (A)"):
                return
            try:
                print("set current")
                # self.ksm2440.set_current(float(current))
            except:
                self.popErrorWindow("Seems something wrong with current. Please check again.")
                return
        if compliance != "":
            try:
                v = float(compliance)
            except:
                self.popErrorWindow("Compliance should be numeric")
                return
            if not self.checkboundary(float(compliance), "Keithley 2440 com (V)"):
                return
            try:
                print("set compliance")
                # self.ksm2440.set_compliance(v)
            except:
                self.popErrorWindow("Seems something wrong with compliance. Please check again.")
                return

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
                                "Warning: Value of " + name + "should > " + str(x[1]))
                            return False
                    if y == "<":
                        if not float(num) < float(x[1]):
                            file1.close()
                            self.popErrorWindow(
                                "Warning: Value of " + name + "should < " + str(x[1]))
                            return False
                    if y == ">=":
                        if not float(num) >= float(x[1]):
                            file1.close()
                            self.popErrorWindow(
                                "Warning: Value of " + name + "should >= " + str(x[1]))
                            return False
                    if y == "<=":
                        if not float(num) <= float(x[1]):
                            file1.close()
                            self.popErrorWindow(
                                "Warning: Value of " + name + "should <= " + str(x[1]))
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
    ui = ksm2440()
    ui.setupUi(setParameter)
    setParameter.show()
    sys.exit(app.exec_())

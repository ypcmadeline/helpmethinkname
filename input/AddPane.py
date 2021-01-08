from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

import input.status as status
import re
import input.ErrorPane as ErrorPane


class add(object):
    signal = pyqtSignal(int)

    def __init__(self, prop):
        self.pp = prop

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(831, 591)

        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 120, 571, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 47, 12))
        self.label.setText(self.pp.savename)
        self.label.adjustSize()

        self.index = []
        self.rfield = []
        self.cbox = []

        for i in range(len(self.pp.saverange)):
            self.index.append(QtWidgets.QLabel(self.gridLayoutWidget))
            self.index[i].setText(str(i + 1) + ". ")
            self.gridLayout.addWidget(self.index[i], i, 0, 1, 1)

            self.rlabel = QtWidgets.QLabel(self.gridLayoutWidget)
            self.rlabel.setText("Range: ")
            self.gridLayout.addWidget(self.rlabel, i, 1, 1, 1)

            self.rfield.append(QtWidgets.QLineEdit(self.gridLayoutWidget))
            self.rfield[i].setText(self.pp.saverange[i])
            self.gridLayout.addWidget(self.rfield[i], i, 2, 1, 1)

            self.cbox.append(QtWidgets.QCheckBox(self.gridLayoutWidget))
            self.cbox[i].setText("sweep")
            self.cbox[i].setChecked(self.pp.savesweep[i])
            self.gridLayout.addWidget(self.cbox[i], i, 3, 1, 1)

        self.addrow()

        self.addBtn = QtWidgets.QPushButton(Dialog)
        self.addBtn.setGeometry(QtCore.QRect(680, 160, 51, 31))
        self.addBtn.setText("Save")
        self.addBtn.clicked.connect(lambda: self.addHandler())

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def addrow(self):
        length = len(self.pp.saverange)
        self.index.append(QtWidgets.QLabel(self.gridLayoutWidget))
        self.index[length].setText(str(length + 1) + ". ")
        self.gridLayout.addWidget(self.index[length], length, 0, 1, 1)

        self.rlabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.rlabel.setText("Range: ")
        self.gridLayout.addWidget(self.rlabel, length, 1, 1, 1)

        self.rfield.append(QtWidgets.QLineEdit(self.gridLayoutWidget))
        self.gridLayout.addWidget(self.rfield[length], length, 2, 1, 1)

        self.cbox.append(QtWidgets.QCheckBox(self.gridLayoutWidget))
        self.cbox[length].setText("sweep")
        self.gridLayout.addWidget(self.cbox[length], length, 3, 1, 1)


    def addHandler(self):
        rangelist = []
        sweeplist = []
        for i in range(len(self.pp.saverange) + 1):
            # check range format
            getrange = self.rfield[i].text()
            check = self.checkrange(getrange,i)
            if not check:
                return
            # if no wrong format -> continue
            rangelist.append(getrange)
            sweeplist.append(self.cbox[i].isChecked())
        self.pp.saverange = rangelist
        self.pp.savesweep = sweeplist
        self.addrow()

    def checkrange(self, text, i):
        try:
            numbers = text.split(",")
            num1 = numbers[0]
            num2 = numbers[1]
            check1 = self.checknum(num1, i)
            check2 = self.checknum(num2, i)
            check3 = numbers[2].isdigit()
            checkbound1 = self.checkboundary(num1, i)
            checkbound2 = self.checkboundary(num2, i)
            if not (check1 and check2 and check3):
                self.popErrorWindow("Wrong input range format at " + str(i + 1) + "th item.")
            return check1 and check2 and check3 and checkbound1 and checkbound2
        except:
            self.popErrorWindow("Wrong input range format at " + str(i + 1) + "th item.")
            return False

    def checknum(self, text, i):
        y = re.fullmatch("[0-9]*[.][0-9]*|[-][0-9]*[.][0-9]*", text)
        x = re.fullmatch("[0-9]*|[-][0-9]*", text)
        if (y is None) and (x is None):
            self.popErrorWindow("Range must be integers/float at " + str(i + 1) + "th vary item.")
            return False
        return True


    def checkboundary(self, num, index):
        try:
            file1 = open("boundary.txt", "r+")
            text = file1.readlines()
            for i in range(len(text)):
                text[i] = text[i].replace('\n', '')
                x = re.split("<=|>=|<|>", text[i])
                y = re.findall("<=|>=|<|>", text[i])
                y = y[0]
                if self.label.text() == x[0]:
                    if y == ">":
                        if not float(num) > float(x[1]):
                            file1.close()
                            self.popErrorWindow(
                                "Warning: Value at " + str(index + 1) + "th item should > " + str(x[1]))
                            return False
                    if y == "<":
                        if not float(num) < float(x[1]):
                            file1.close()
                            self.popErrorWindow(
                                "Warning: Value at " + str(index + 1) + "th item should < " + str(x[1]))
                            return False
                    if y == ">=":
                        if not float(num) >= float(x[1]):
                            file1.close()
                            self.popErrorWindow(
                                "Warning: Value at " + str(index + 1) + "th item should >= " + str(x[1]))
                            return False
                    if y == "<=":
                        if not float(num) <= float(x[1]):
                            file1.close()
                            self.popErrorWindow(
                                "Warning: Value at " + str(index + 1) + "th item should <= " + str(x[1]))
                            return False
            file1.close()
            return True
        except:
            self.popErrorWindow("Fail to read boundary.txt")
            return False

    def popErrorWindow(self, msg):
        self.window = QtWidgets.QMainWindow()
        self.ui = ErrorPane.error(msg)
        self.ui.setupUi(self.window)
        self.window.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    setParameter = QtWidgets.QMainWindow()
    test = status.Status("testing")
    test.addRange(["1,5,5"])
    test.addSweep(True)
    ui = add(test)
    ui.setupUi(setParameter)
    setParameter.show()
    sys.exit(app.exec_())

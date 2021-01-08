import os
import re

from PyQt5 import QtCore, QtWidgets
import library.keithley_6221 as keithley_6221
import input.ErrorPane as ErrorPane

class ksm6221(object):

    def __init__(self):
        # self.ksm6221 = keithley_6221.keithley_6221()
        self.reset_num = 0
        self.init_num = 0
        self.arm_num = 0
        self.abort_num = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 30, 171, 16))
        self.label.setText("Keithley Source Meter 6221")
        self.label.adjustSize()

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 40, 900, 800))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.dcLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.dcLayoutWidget.setGeometry(QtCore.QRect(40, 80, 100, 300))
        self.dcLayoutWidget.setObjectName("dcLayoutWidget")
        self.dcLayout = QtWidgets.QGridLayout(self.dcLayoutWidget)
        self.dcLayout.setContentsMargins(0, 0, 0, 0)
        self.dcLayout.setObjectName("dcLayout")
        self.gridLayout.addWidget(self.dcLayoutWidget, 0, 0, 1, 1)

        self.dclabel = QtWidgets.QLabel(self.dcLayoutWidget)
        self.dclabel.setText("DC Setting:")
        self.dcLayout.addWidget(self.dclabel, 0, 0, 1, 1)
        self.dclabel.adjustSize()

        self.curlabel = QtWidgets.QLabel(self.dcLayoutWidget)
        self.curlabel.setText("Current(A)")
        self.dcLayout.addWidget(self.curlabel, 3, 0, 1, 1)

        self.current = QtWidgets.QLineEdit(self.dcLayoutWidget)
        self.dcLayout.addWidget(self.current, 3, 1, 1, 1)

        self.comlabel = QtWidgets.QLabel(self.dcLayoutWidget)
        self.comlabel.setText("Compliance(V)")
        self.dcLayout.addWidget(self.comlabel, 4, 0, 1, 1)

        self.compliance = QtWidgets.QLineEdit(self.dcLayoutWidget)
        self.dcLayout.addWidget(self.compliance, 4, 1, 1, 1)

        self.dc_setbtn = QtWidgets.QPushButton(self.dcLayoutWidget)
        self.dc_setbtn.setText("Apply")
        self.dc_setbtn.clicked.connect(lambda: self.dcset())
        self.dcLayout.addWidget(self.dc_setbtn, 5, 3, 1, 1)

        self.resetbtn = QtWidgets.QPushButton(self.dcLayoutWidget)
        self.resetbtn.setText("Reset")
        self.resetbtn.clicked.connect(lambda: self.reset())
        self.dcLayout.addWidget(self.resetbtn, 1, 0, 1, 1)

        self.resetlabel = QtWidgets.QLabel(self.dcLayoutWidget)
        self.resetlabel.setText("")
        self.dcLayout.addWidget(self.resetlabel, 1, 1, 1, 1)

        self.autorangebtn = QtWidgets.QPushButton(self.dcLayoutWidget)
        self.autorangebtn.setText("AutoRange: OFF")
        self.autorangebtn.clicked.connect(lambda: self.autorange())
        self.dcLayout.addWidget(self.autorangebtn, 2, 0, 1, 1)

        self.acLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.acLayoutWidget.setGeometry(QtCore.QRect(40, 80, 100, 300))
        self.acLayoutWidget.setObjectName("acLayoutWidget")
        self.acLayout = QtWidgets.QGridLayout(self.acLayoutWidget)
        self.acLayout.setContentsMargins(0, 0, 0, 0)
        self.acLayout.setObjectName("acLayout")
        self.gridLayout.addWidget(self.acLayoutWidget, 1,0,1,1)

        self.aclabel = QtWidgets.QLabel(self.dcLayoutWidget)
        self.aclabel.setText("AC Setting:")
        self.acLayout.addWidget(self.aclabel, 0, 0, 1, 1)
        self.aclabel.adjustSize()

        self.initbtn = QtWidgets.QPushButton(self.acLayoutWidget)
        self.initbtn.setText("Initialize")
        self.initbtn.clicked.connect(lambda: self.init())
        self.acLayout.addWidget(self.initbtn, 1, 0, 1, 1)

        self.initlabel = QtWidgets.QLabel(self.dcLayoutWidget)
        self.initlabel.setText("")
        self.acLayout.addWidget(self.initlabel, 1, 1, 1, 1)
        self.initlabel.adjustSize()

        self.armbtn = QtWidgets.QPushButton(self.acLayoutWidget)
        self.armbtn.setText("Arm")
        self.armbtn.clicked.connect(lambda: self.arm())
        self.acLayout.addWidget(self.armbtn, 2, 0, 1, 1)

        self.armlabel = QtWidgets.QLabel(self.acLayoutWidget)
        self.armlabel.setText("")
        self.acLayout.addWidget(self.armlabel, 2, 1, 1, 1)
        self.armlabel.adjustSize()

        self.abortbtn = QtWidgets.QPushButton(self.acLayoutWidget)
        self.abortbtn.setText("Abort")
        self.abortbtn.clicked.connect(lambda: self.abort())
        self.acLayout.addWidget(self.abortbtn, 3, 0, 1, 1)

        self.abortlabel = QtWidgets.QLabel(self.acLayoutWidget)
        self.abortlabel.setText("")
        self.acLayout.addWidget(self.abortlabel, 3, 1, 1, 1)
        self.abortlabel.adjustSize()

        self.phasebtn = QtWidgets.QPushButton(self.acLayoutWidget)
        self.phasebtn.setText("Phase Marker: OFF")
        self.phasebtn.clicked.connect(lambda: self.phasemarker())
        self.acLayout.addWidget(self.phasebtn, 4, 0, 1, 1)

        self.rangelabel = QtWidgets.QLabel(self.acLayoutWidget)
        self.rangelabel.setText("Range: ")
        self.acLayout.addWidget(self.rangelabel, 5, 0, 1, 1)

        self.range = QtWidgets.QComboBox(self.acLayoutWidget)
        self.range.addItem("")
        self.range.addItem("fix")
        self.range.addItem("best")
        self.acLayout.addWidget(self.range, 5, 1, 1, 1)
        self.range.currentTextChanged.connect(lambda: self.wave_range())

        self.amplabel = QtWidgets.QLabel(self.acLayoutWidget)
        self.amplabel.setText("Amplitude(A)")
        self.acLayout.addWidget(self.amplabel, 6, 0, 1, 1)

        self.amplitude = QtWidgets.QLineEdit(self.acLayoutWidget)
        self.acLayout.addWidget(self.amplitude, 6, 1, 1, 1)

        self.frelabel = QtWidgets.QLabel(self.acLayoutWidget)
        self.frelabel.setText("Frequency(Hz)")
        self.acLayout.addWidget(self.frelabel, 7, 0, 1, 1)

        self.frequency = QtWidgets.QLineEdit(self.acLayoutWidget)
        self.acLayout.addWidget(self.frequency, 7, 1, 1, 1)

        self.offsetlabel = QtWidgets.QLabel(self.acLayoutWidget)
        self.offsetlabel.setText("Offset")
        self.acLayout.addWidget(self.offsetlabel, 8, 0, 1, 1)

        self.offset = QtWidgets.QLineEdit(self.acLayoutWidget)
        self.acLayout.addWidget(self.offset, 8, 1, 1, 1)

        self.durlabel = QtWidgets.QLabel(self.acLayoutWidget)
        self.durlabel.setText("Duration")
        self.acLayout.addWidget(self.durlabel, 9, 0, 1, 1)

        self.duration = QtWidgets.QLineEdit(self.acLayoutWidget)
        self.acLayout.addWidget(self.duration, 9, 1, 1, 1)

        self.deglabel = QtWidgets.QLabel(self.acLayoutWidget)
        self.deglabel.setText("Phase marker degree")
        self.acLayout.addWidget(self.deglabel, 10, 0, 1, 1)

        self.degree = QtWidgets.QLineEdit(self.acLayoutWidget)
        self.acLayout.addWidget(self.degree, 10, 1, 1, 1)

        self.ac_setbtn = QtWidgets.QPushButton(self.acLayoutWidget)
        self.ac_setbtn.setText("Apply")
        self.ac_setbtn.clicked.connect(lambda: self.acset())
        self.acLayout.addWidget(self.ac_setbtn, 11, 2, 1, 1)

        self.outputbtn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.outputbtn.setText("Output: OFF")
        self.outputbtn.clicked.connect(lambda: self.output())
        self.gridLayout.addWidget(self.outputbtn, 2, 0, 1, 1)

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
        # self.ksm6221.reset()
        if self.reset_num != 0:
            self.resetlabel.setText("Reset("+str(self.reset_num)+")")
        else:
            self.resetlabel.setText("Reset")
        self.reset_num = self.reset_num + 1

    def dcset(self):
        current = self.current.text()
        compliance = self.compliance.text()
        if current != "":
            try:
                c = float(current)
            except:
                self.popErrorWindow("Current should be numeric")
                return
            if not self.checkboundary(float(current), "Keithley 6221 cur (A)"):
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
            if not self.checkboundary(float(compliance), "Keithley 6221 com (V)"):
                return
            try:
                print("set compliance")
                # self.ksm2440.set_compliance(v)
            except:
                self.popErrorWindow("Seems something wrong with compliance. Please check again.")
                return

    def autorange(self):
        if self.autorangebtn.text() == "AutoRange: ON":
            # self.ksm6221.auto_range(False)
            self.autorangebtn.setText("AutoRange: OFF")
        else:
            # self.ksm6221.auto_range(True)
            self.autorangebtn.setText("AutoRange: ON")

    def wave_range(self):
        print("wave")
        # self.ksm6221.wave_range(self.range.currentText())

    def acset(self):
        amplitude = self.amplitude.text()
        frequency = self.frequency.text()
        degree = self.degree.text()
        offset = self.offset.text()
        duration = self.duration.text()
        if amplitude != "":
            try:
                a = float(amplitude)
            except:
                self.popErrorWindow("Amplitude should be numeric")
                return
            if not self.checkboundary(float(amplitude), "Keithley 6221 amp (A)"):
                return
            try:
                print("set amp")
                # self.ksm6221.set_wave_amp(float(amplitude))
            except:
                self.popErrorWindow("Seems something wrong with amplitude. Please check again.")
                return
        if frequency != "":
            try:
                f = float(frequency)
            except:
                self.popErrorWindow("frequency should be numeric")
                return
            if not self.checkboundary(float(frequency), "Keithley 6221 fre (Hz)"):
                return
            try:
                print("set amp")
                # self.ksm6221.set_wave_fre(float(frequency))
            except:
                self.popErrorWindow("Seems something wrong with frequency. Please check again.")
                return
        if degree != "":
            try:
                d = float(degree)
            except:
                self.popErrorWindow("degree should be numeric")
                return
            if not self.checkboundary(float(degree), "Keithley 6221 Phase marker degree"):
                return
            try:
                print("set degree")
                # self.ksm6221.set_phase_maker(float(degree))
            except:
                self.popErrorWindow("Seems something wrong with degree. Please check again.")
                return
        if offset != "":
            try:
                o = float(offset)
            except:
                self.popErrorWindow("offset should be numeric")
                return
            if not self.checkboundary(float(offset), "Keithley 6221 offset"):
                return
            try:
                print("set offset")
                # self.ksm6221.set_offset(float(offset))
            except:
                self.popErrorWindow("Seems something wrong with offset. Please check again.")
                return
        if duration != "":
            try:
                d = float(duration)
            except:
                self.popErrorWindow("duration should be numeric")
                return
            if not self.checkboundary(float(duration), "Keithley 6221 duration"):
                return
            try:
                print("set duration")
                # self.ksm6221.set_wave_duration(float(duration))
            except:
                self.popErrorWindow("Seems something wrong with duration. Please check again.")
                return


    def arm(self):
        # self.ksm6221.arm_wave()
        if self.arm_num != 0:
            self.armlabel.setText("Set to ARM WAVE("+str(self.arm_num)+")")
        else:
            self.armlabel.setText("Set to ARM WAVE")
        self.arm_num = self.arm_num + 1

    def abort(self):
        # self.ksm6221.wave_abort()
        if self.abort_num != 0:
            self.abortlabel.setText("Aborted("+str(self.abort_num)+")")
        else:
            self.abortlabel.setText("Aborted")
        self.abort_num = self.abort_num + 1

    def init(self):
        # self.ksm6221.wave_init()
        if self.init_num != 0:
            self.initlabel.setText("Initialized("+str(self.init_num)+")")
        else:
            self.initlabel.setText("Initialized")
        self.init_num = self.init_num + 1

    def phasemarker(self):
        if self.phasebtn.text() == "Phase Marker: ON":
            # self.ksm6221.phase_maker(False)
            self.phasebtn.setText("Phase Marker: OFF")
        else:
            # self.ksm6221.phase_maker(True)
            self.phasebtn.setText("Phase Marker: ON")

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
    ui = ksm6221()
    ui.setupUi(setParameter)
    setParameter.show()
    sys.exit(app.exec_())

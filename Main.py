from PyQt5 import QtCore, QtWidgets
import components.GUImotor
import components.GUIksm2440
import components.GUIksm6221
import input.MainPane
import output.first_gui


class gui(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 30, 50, 16))
        self.label.setText("No Name")
        self.label.adjustSize()
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 80, 500, 300))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.indelabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.indelabel.setText("Independent control:")
        self.gridLayout.addWidget(self.indelabel, 0, 0, 1, 1)

        self.ksm2440 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.ksm2440.setText("Keithley 2440 Source Meter")
        self.ksm2440.clicked.connect(lambda: self.pop2440())
        self.gridLayout.addWidget(self.ksm2440, 1, 0, 1, 1)

        self.ksm6221 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.ksm6221.setText("Keithley 6221 Source Meter")
        self.ksm6221.clicked.connect(lambda: self.pop6221())
        self.gridLayout.addWidget(self.ksm6221, 2, 0, 1, 1)

        self.motor = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.motor.setText("Motor")
        self.motor.clicked.connect(lambda: self.popmotor())
        self.gridLayout.addWidget(self.motor, 3, 0, 1, 1)

        self.intelabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.intelabel.setText("Integrated control:")
        self.gridLayout.addWidget(self.intelabel, 4, 0, 1, 1)

        self.input = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.input.setText("Input Setting")
        self.input.clicked.connect(lambda: self.popinput())
        self.gridLayout.addWidget(self.input, 5, 0, 1, 1)

        self.output = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.output.setText("Output Setting")
        self.output.clicked.connect(lambda: self.popoutput())
        self.gridLayout.addWidget(self.output, 6, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 422, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def pop2440(self):
        self.window2440 = QtWidgets.QMainWindow()
        self.ui = components.GUIksm2440.ksm2440()
        self.ui.setupUi(self.window2440)
        self.window2440.show()

    def pop6221(self):
        self.window6221 = QtWidgets.QMainWindow()
        self.ui = components.GUIksm6221.ksm6221()
        self.ui.setupUi(self.window6221)
        self.window6221.show()

    def popmotor(self):
        self.windowmotor = QtWidgets.QMainWindow()
        self.ui = components.GUImotor.guimotor()
        self.ui.setupUi(self.windowmotor)
        self.windowmotor.show()

    def popinput(self):
        self.windowinput = QtWidgets.QMainWindow()
        self.ui = input.MainPane.Setting(self.windowinput)
        self.windowinput.show()

    def popoutput(self):
        self.windowoutput = QtWidgets.QMainWindow()
        self.ui = output.first_gui.Ui_kGUI()
        self.ui.setupUi(self.windowoutput)
        self.windowoutput.show()








if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    setParameter = QtWidgets.QMainWindow()
    ui = gui()
    ui.setupUi(setParameter)
    setParameter.show()
    sys.exit(app.exec_())

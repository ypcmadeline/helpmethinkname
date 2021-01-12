from PyQt5 import QtCore, QtGui, QtWidgets

import output.first_gui


class process():

    def __init__(self, MainWindow, msg):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(600, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.msg = msg

    def popoutput(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = output.first_gui.Ui_kGUI(self.msg)
        self.ui.setupUi(self.window)
        self.window.show()
        self.MainWindow.close()

    def setupUi(self):
        # MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(600, 300)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 30, 171, 16))
        self.label.setText("Continue to generate output?")
        self.label.adjustSize()

        self.ybutton = QtWidgets.QPushButton(self.centralwidget)
        self.ybutton.setGeometry(QtCore.QRect(200, 200, 50, 50))
        self.ybutton.setText("OK")
        self.ybutton.adjustSize()
        self.ybutton.clicked.connect(lambda: self.popoutput())

        self.nbutton = QtWidgets.QPushButton(self.centralwidget)
        self.nbutton.setGeometry(QtCore.QRect(400, 200, 50, 50))
        self.nbutton.setText("No")
        self.nbutton.adjustSize()
        self.nbutton.clicked.connect(lambda: self.MainWindow.close())

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 422, 22))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = process(window)
    ui.setupUi()
    window.show()
    sys.exit(app.exec_())

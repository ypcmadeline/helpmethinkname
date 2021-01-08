import csv
import numpy as np
from PyQt5.QtWidgets import QFileDialog

import input.ErrorPane as ErrorPane
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import input.ProcessPane as ProcessPane


class inputFile:

    def __init__(self, varyParameter, constParameter):
        self.window = QtWidgets.QMainWindow()
        self.vary_name = []
        self.range_list = []
        self.sweep = []
        for i in range(len(varyParameter)):
            self.vary_name.append(varyParameter[i].name)

        self.const_name = []
        self.const_value = []
        for i in range(len(constParameter)):
            self.const_name.append(constParameter[i].getName())
            self.const_value.append(constParameter[i].getValue())
        self.write_list = []
        self.file_list = []
        self.csv = QFileDialog.getSaveFileName(self.window, "Save File", "",".csv")[0]
        self.f = open(self.csv+".csv", 'w+', newline='')

        try:
            for i in range(len(varyParameter)):
                tlist = []
                for j in range(len(varyParameter[i].range)):
                    num = varyParameter[i].range[j].split(",")
                    if varyParameter[i].sweep[j]:
                        # if first range sweep
                        tlist = tlist + list(np.linspace(float(num[0]), float(num[1]), int(num[2]))) \
                                + list(np.linspace(float(num[1]), float(num[0]), int(num[2])))
                    else:
                        tlist = tlist + list(np.linspace(float(num[0]), float(num[1]), int(num[2])))
                if (not tlist):
                    self.popErrorWindow("range doesnt make sense at " + str(i + 1) + "th vary item.")
                self.write_list.append(tlist)
            self.writeHead()
            self.recurse(len(varyParameter), len(varyParameter))
            # self.f.close()
            self.popProcessWindow()
        except:
            self.popErrorWindow("range doesnt make sense at " + str(i + 1) + "th vary item.")


    def writeHead(self):
        name_list = self.vary_name + self.const_name
        self.f.csv_write = csv.writer(self.f)
        self.f.csv_write.writerow(name_list)
        self.f.flush()
        print(name_list)

    def recurse(self, n, t):
        if n <= 0:
            return
        for i in range(len(self.write_list[n - 1])):
            if i == 0:
                if len(self.file_list) != t:
                    self.file_list.append(self.write_list[n - 1][i])
            # else:
            self.file_list[t - n] = self.write_list[n - 1][i]
            if len(self.file_list) == t and n == 1:
                # self.file_list.reverse()
                self.f.csv_write = csv.writer(self.f)
                self.f.csv_write.writerow(self.file_list[::-1] + self.const_value)
                self.f.flush()
                print(self.file_list[::-1] + self.const_value)
            self.recurse(n - 1, t)

    def popErrorWindow(self, msg):
        self.window = QtWidgets.QMainWindow()
        self.ui = ErrorPane.error(msg)
        self.ui.setupUi(self.window)
        self.window.show()

    def popProcessWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = ProcessPane.process(self.window, self.csv+".csv")
        self.ui.setupUi()
        self.window.show()

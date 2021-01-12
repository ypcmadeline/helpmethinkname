import csv
from PyQt5 import QtWidgets
import pandas as pd
import time
from PyQt5.QtWidgets import QFileDialog
import library.keithley_2440, library.keithley_6221, library.motor, library.keithley_2182a
import input.ErrorPane as ErrorPane
import library.keithley_2440, library.keithley_6221, library.motor


class output:

    def __init__(self, inputfile, mode):
        self.window = QtWidgets.QMainWindow()
        try:
            # self.ksm2440 = library.keithley_2440.keithley_2440()
            print("find 2440 cur")
        except:
            self.popErrorWindow("Fail to connect Keithley 2440 Source Meter")
        try:
            # self.ksm6221 = library.keithley_6221.keithley_6221()
            print("find 6221")
        except:
            self.popErrorWindow("Fail to connect Keithley 6221 Source Meter")
        try:
            # self.motor = library.motor.motor()
            print("find motor")
        except:
            self.popErrorWindow("Fail to connect motor")
        try:
            # self.ksm2182 = library.keithley_2182a.keithley_2182a()
            print("find 2182")
        except:
            self.popErrorWindow("Fail to connect Keithley 2182a Source Meter")
        try:
            self.input = pd.read_csv(inputfile)
            self.inputadress = inputfile
        except:
            self.popErrorWindow("Fail to read input file")
        try:
            self.csv = QFileDialog.getSaveFileName(self.window, "Save File", "", ".csv")[0]
            self.output = open(self.csv + ".csv", 'w+', newline='')
            # self.output = open(output+".csv", 'w+', newline='')
        except:
            self.popErrorWindow("Fail to create output file")
        self.mode = mode

    def write_output(self):
        if "Keithley 2440 cur (A)" or "Keithley 2440 com (V)" in self.input:
            # self.ksm2440 = library.keithley_2440.keithley_2440()
            print("construct 2440")
        if "Keithley 6221 cur (A)" or "Keithley 6221 com (V)" or "Keithley 6221 amp (A)" or "Keithley 6221 fre (Hz)" in self.input:
            # self.ksm6221 = library.keithley_6221.keithley_6221()
            # self.ksm6221.auto_range(True)
            print("construct 6221")
        if "Angle" in self.input:
            # self.motor = library.motor.motor()
            print("construct motor")
        # write header
        f = open(self.inputadress, newline='')
        csv_reader = csv.reader(f)
        csv_headings = next(csv_reader)
        f.close()
        self.output.csv_write = csv.writer(self.output)
        self.output.csv_write.writerow(csv_headings)
        self.output.flush()
        count = self.input.iloc[:, 0].count()
        for i in range(count):
            record = []
            if "Keithley 2440 cur (A)" in self.input:
                if i != 0:
                    if self.input["Keithley 2440 cur (A)"][i] != self.input["Keithley 2440 cur (A)"][i - 1]:
                        # self.ksm2440.set_current(self.input["Keithley 2440 cur (A)"][i])
                        print("set 2440 cur")
                else:
                    # self.ksm2440.set_current(self.input["Keithley 2440 cur (A)"][i])
                    print("set 2440 cur")
                record.append(self.input["Keithley 2440 cur (A)"][i])

            if "Keithley 2440 com (V)" in self.input:
                if i != 0:
                    if self.input["Keithley 2440 com (V)"][i] != self.input["Keithley 2440 com (V)"][i - 1]:
                        # self.ksm2440.set_compliance(self.input["Keithley 2440 com (V)"][i])
                        print("set 2440 com")
                else:
                    # self.ksm2440.set_compliance(self.input["Keithley 2440 com (V)"][i])
                    print("set 2440 com")
                record.append(self.input["Keithley 2440 com (V)"][i])

            if "Keithley 6221 cur (A)" in self.input:
                if i != 0:
                    if self.input["Keithley 6221 cur (A)"][i] != self.input["Keithley 6221 cur (A)"][i - 1]:
                        # self.ksm6221.set_current(self.input["Keithley 6221 cur (A)"][i])
                        print("set 6221 cur")
                else:
                    # self.ksm6221.set_current(self.input["Keithley 6221 cur (A)"][i])
                    print("set 6221 cur")
                record.append(self.input["Keithley 6221 cur (A)"][i])

            if "Keithley 6221 com (V)" in self.input:
                if i != 0:
                    if self.input["Keithley 6221 com (V)"][i] != self.input["Keithley 6221 com (V)"][i - 1]:
                        # self.ksm6221.set_compliance(self.input["Keithley 6221 com (V)"][i])
                        print("set 6221 com")
                else:
                    # self.ksm6221.set_compliance(self.input["Keithley 6221 com (V)"][i])
                    print("set 6221 com")
                record.append(self.input["Keithley 6221 com (V)"][i])

            if "Keithley 6221 amp (A)" in self.input:
                if i != 0:
                    if self.input["Keithley 6221 amp (A)"][i] != self.input["Keithley 6221 amp (A)"][i - 1]:
                        # self.ksm6221.set_wave_amp(self.input["Keithley 6221 amp (A)"][i])
                        print("set 6221 amp")
                else:
                    # self.ksm6221.set_wave_amp(self.input["Keithley 6221 amp (A)"][i])
                    print("set 6221 amp")
                record.append(self.input["Keithley 6221 amp (A)"][i])

            if "Keithley 6221 fre (Hz)" in self.input:
                if i != 0:
                    if self.input["Keithley 6221 fre (Hz)"][i] != self.input["Keithley 6221 fre (Hz)"][i - 1]:
                        # self.ksm6221.set_wave_fre(self.input["Keithley 6221 fre (Hz)"][i])
                        print("set 6221 fre")
                else:
                    # self.ksm6221.set_wave_fre(self.input["Keithley 6221 fre (Hz)"][i])
                    print("set 6221 fre")
                record.append(self.input["Keithley 6221 fre (Hz)"][i])

            if "Angle" in self.input:
                if i != 0:
                    if self.input["Angle"][i] != self.input["Angle"][i - 1]:
                        # self.motor.rotation(self.input["Angle"][i])
                        print("set angle")
                else:
                    # self.motor.rotation(self.input["Angle"][i])
                    print("angle")
                record.append(self.input["Angle"][i])
                # time.sleep(0.1)

            if i == 0:
                try:
                    # self.ksm2440.output(True)
                    print("turn on 2440")
                except:
                    pass
                try:
                    # self.ksm6221.output(True)
                    print("turn on 6221")
                except:
                    pass

            # measurement
            result = 0
            record.append(result)
            self.output.csv_write.writerow(record)
            self.output.flush()
            # time.sleep(2)
        print("end")
        self.output.close()
        return

    def popErrorWindow(self, msg):
        self.errorwindow = QtWidgets.QMainWindow()
        self.ui = ErrorPane.error(msg)
        self.ui.setupUi(self.errorwindow)
        self.errorwindow.show()


if __name__ == "__main__":
    o = output("C:/Users/Madeline Chan/PycharmProjects/GUI_all/output/tryin.csv", "none")
    o.getwindow()
    o.write_output()

import csv
from PyQt5 import QtWidgets
import pandas as pd
import time
from PyQt5.QtWidgets import QFileDialog
import library.keithley_2440, library.keithley_6221, library.motor, library.keithley_2182a
import input.ErrorPane as ErrorPane
import library.keithley_2440, library.keithley_6221, library.motor


# import zhinst.ziPython

class output:

    def __init__(self, inputfile, mode):
        self.mode = mode
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
        if self.mode == "Dc Sweep mode" or self.mode == "Ac Sweep Mode":
            try:
                # self.ksm2182 = library.keithley_2182a.keithley_2182a()
                print("find 2182")
            except:
                self.popErrorWindow("Fail to connect Keithley 2182a Source Meter")
        if self.mode == "MFLI mode":
            try:
                # d = zhinst.ziPython.ziDiscovery()
                # d.find('dev5062')
                # devProp = d.get('dev5062')
                # self.daq = zhinst.ziPython.ziDAQServer(devProp['serveraddress'], devProp['serverport'], 6)
                print("find mfli")
            except:
                self.popErrorWindow("Fail to connect MFLI")
        if self.mode == "sensor mode":
            try:
                from library.gdx_s import gdx
                self.gdx = gdx.gdx()
                self.gdx.open_usb()
                print("find sensor")
            except:
                self.popErrorWindow("Fail to connect sensor")
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
        if self.mode == "Dc Sweep mode" or self.mode == "Ac Sweep Mode":
            csv_headings = csv_headings + ["Keithley 2182a"]
        elif self.mode == "MFLI mode":
            csv_headings = csv_headings + ["MFLI-x", "MFLI-y"]
        else:
            csv_headings = csv_headings + ["Sensor x", "Sensor y", "Sensor z"]
        self.output.csv_write = csv.writer(self.output)
        self.output.csv_write.writerow(csv_headings)
        self.output.flush()
        count = self.input.iloc[:, 0].count()
        for i in range(count):

            if i == 0:
                if self.mode == "Ac sweep Mode":
                    try:
                        print("ac")
                        # self.ksm6221.auto_range(False)
                    #     equ_6221.write("curr 0")
                    except:
                        pass
                if self.mode == "MFLI Mode":
                    try:
                        print("mfli")
                        # self.ksm6221.set_offset(0)
                        # self.ksm6221.wave_range("best")
                        # self.ksm6221.arm_wave()
                        # self.ksm6221.wave_init()
                    #     equ_6221.write("curr 0")
                    except:
                        pass
                if self.mode == "Sensor Mode":
                    try:
                        print("sensor")
                        # self.gdx.select_sensors()
                        # self.gdx.start(70)
                    except:
                        pass
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

            # measurement
            result = [0]
            if self.mode == "Dc Sweep mode" or self.mode == "Dc Sweep mode":
                # result = self.ksm2182.record()
                result = [1]
            if self.mode == "MFLI mode":
                # mfli_data = self.daq.poll(0.1,10,1,True)
                # if '/dev5062/demods/0/sample' in mfli_data:
                #     x_1 = mfli_data['/dev5062/demods/0/sample']['x']
                #     y_1 = mfli_data['/dev5062/demods/0/sample']['y']
                #     result = [x_1[0], y_1[0]]
                result = [2, 3]
            if self.mode == "Sensor mode":
                # result = self.gdx.read()
                result = [4,5,6]
            record = record + result
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

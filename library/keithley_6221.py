# keithley_6221
# written by Jonathan Cheung (ECE HKUST)

import pyvisa as py

address_6221 = 'GPIB0::12::INSTR'


class keithley_6221:
    def __init__(self):
        rm = py.ResourceManager()
        self.equ_6221 = rm.open_resource(address_6221)
        # self.equ_6221.write("CLE")

    def reset(self):
        self.equ_6221.write("*rst")

    def auto_range(self, option):
        if (option):
            self.equ_6221.write("curr:rang:auto on")
        else:
            self.equ_6221.write("curr:rang:auto  off")

    def set_compliance(self, compliance):
        self.equ_6221.write("curr:comp %d" % compliance)

    def set_current(self, current):
        self.equ_6221.write("curr %f" % current)

    def output(self, option):
        if (option):
            self.equ_6221.write("outp on")
        else:
            self.equ_6221.write("outp off")

    def wave_sin(self, amplitude, frequency, offset):
        self.equ_6221.write("sour:wave:func sin")
        self.equ_6221.write("sour:wave:ampl %f" % amplitude)
        self.equ_6221.write("sour:wave:freq %d" % frequency)
        self.equ_6221.write("sour:wave:offs %f" % offset)

    def phase_maker(self, option):
        if (option):
            self.equ_6221.write("sour:wave:pmar:stat on")
        else:
            self.equ_6221.write("sour:wave:pmar:stat off")

    def set_phase_maker(self, degree):
        self.equ_6221.write("sour:wave:pmark %d" % degree)

    def wave_range(self, option):
        if (option == 'fix'):
            self.equ_6221.write("sour:wave:rang fix")
        else:
            self.equ_6221.write("sour:wave:rang best")

    def set_offset(self, offset):
        self.equ_6221.write("sour:wave:offs %f" % offset)

    def set_wave_duration(self, t):
        self.equ_6221.write("sour:wave:dur:time %f" % t)

    def set_wave_amp(self, amplitude):
        self.equ_6221.write("sour:wave:ampl %f" % amplitude)

    def set_wave_fre(self, frequency):
        self.equ_6221.write("sour:wave:freq %d" % frequency)

    def arm_wave(self):
        self.equ_6221.write("SOUR:WAVE:ARM")

    def wave_init(self):
        self.equ_6221.write("SOUR:WAVE:INIT")

    def wave_abort(self):
        self.equ_6221.write("sour:wave:abor")

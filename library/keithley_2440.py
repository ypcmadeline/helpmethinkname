# keithley_2440
# written by Jonathan Cheung (ECE HKUST)

import pyvisa as py

address_2440 = 'GPIB0::22::INSTR'

class keithley_2440:

    def __init__(self):
        rm = py.ResourceManager()
        self.equ_2440 = rm.open_resource(address_2440)
        self.equ_2440.write("*rst")
        self.equ_2440.write(":sour:func curr")
        self.equ_2440.write(":sour:curr:mode fix")

    def set_compliance(self,compliance):
        self.equ_2440.write(":sens:curr:prot %d" %compliance)
    
    def reset(self):
        self.equ_2440.write("*rst")
        self.equ_2440.write(":sour:func curr")
        self.equ_2440.write(":sour:curr:mode fix")

    def set_current(self, current):
        self.equ_2440.write(":sour:curr:level %f" %current)

    def output(self, option):
        if (option):
            self.equ_2440.write("outp on")
        else :
            self.equ_2440.write("outp off")

# keithley_2182a
# written by Jonathan Cheung (ECE HKUST)


import pyvisa as py

address_2182a = 'GPIB0::07::INSTR'


class keithley_2182a:

    def __init__(self):
        rm = py.ResourceManager()
        self.equ_2182a = rm.open_resource(address_2182a)
        #  set up here 
        self.equ_2182a.write("*rst")
        self.equ_2182a.write(":sens:chan 1")
        self.equ_2182a.write(":sens:func 'VOLT'")

    def record(self):
        reading = float(self.equ_2182a.query("read?"))
        return reading
# motor 
# written by Jonathan Cheung (ECE HKUST)

import serial
import time

# address = "/dev/cu.usbserial-14410"
address = 'COM3'
class motor:
    def __init__(self):
        self.ser = serial.Serial(address, 9600)
        self.angle = 0.0
        self.speed_mode = 0.05625
        self.angle_dif = 0.0

    def send_message(self,message):
        instruction = bytes(message, encoding = 'utf8')
        self.ser.write(instruction)
        time.sleep(0.02)

    def rotation(self, final_angle):

        if(final_angle <= 360.0 and final_angle >= 0):
            self.angle_dif = final_angle - self.angle
        elif(final_angle > -180):
            self.angle_dif = final_angle - self.angle

        pulse = int(self.angle_dif/self.speed_mode)
        
        self.send_message(str(pulse))
        self.angle = self.angle + pulse * self.speed_mode

    def get_ang_set_time(self):
        return self.angle_dif * 2.8

    def set_angle(self):
        self.angle = 0.0
    
    def return_zero(self):
        self.rotation(0) 

    def speed_control(self,speed):
        if (speed == '1'):
            self.send_message('10001')
            self.speed_mode = 0.9
        elif (speed == '1/2'):
            self.send_message('10002')
            self.speed_mode = 0.45
        elif (speed == '1/4'):
            self.send_message('10004')
            self.speed_mode = 0.225
        elif (speed == '1/8'):
            self.send_message('10008')
            self.speed_mode = 0.1125
        elif (speed == '1/16'):
            self.send_message('10016')
            self.speed_mode = 0.05625
        time.sleep(0.1)
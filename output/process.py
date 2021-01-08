# run process and task here

import time
import threading


class process():

    def __init__(self):
        self.file_address =''
        self.mode=''
        self.output_file_name = ''
        self.output_file_address = ''
        self.end = False
        self.test = 100
    
    def update(self,file_address, mode,output_file_name,output_file_address):
        self.file_address = file_address
        self.mode= mode
        self.output_file_name = output_file_name
        self.output_file_address = output_file_address

    def return_progress(self):
        return self.test


    def wait(self):
        self.test = 0
        for i in range(10):
            time.sleep(1)
            print("test "+ str(i))
            if (self.end):
                break
            self.test = i
        
        self.end = False
        self.test=36
        # print(self.file_address)
        # print(self.mode)
        # print(self.output_file_name)
        # print(self.output_file_address)

    def run(self):
        self.end = False
        th = threading.Thread(target=self.wait)
        th.start()


    def stop(self):
        self.end = True
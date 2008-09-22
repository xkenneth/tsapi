import pdb
import re
import dircache
import Pmw
import time
from Tkinter import *
import tkFileDialog
from copy import copy

from tsapi.SuperSerial import SuperSerial, to_string, to_int_list

def check_device(fun):
    def func(*args):
        if not isinstance(args[0],SuperSerial):
            print "Device has not been configured!"
            return
        return fun(*args)
    return func

@check_device
def set_system_time(ser,year,month,day,hour,minute,second):
    if year < 0 or month < 0 or month > 12 or day < 0 or day > 31 or hour < 0 or hour > 24 or minute < 0 or minute > 60 or second < 0 or second > 60:
        program_status.configure(text="Error: Time is not in the correct format, please check values.")
        return
    
    ser.tell('TY',year,flush=True)
    ser.tell('TM',month,flush=True)
    ser.tell('TD',day,flush=True)
    ser.tell('TH',hour,flush=True)
    ser.tell('TN',minute,flush=True)
    ser.tell('TS',second,flush=True)
    
    return True

@check_device
def get_tool_time(ser):
    sys_time = ser.ask('T').strip()
    return sys_time

#MEMORY MANAGEMENT
@check_device
def read_memory(ser):
    ser.tell('RL')
    
    buffer = []
    
    time.sleep(1)

    while(1):
        new = ser.read_line()
        new = to_int_list(new)
        all = True
        for n in new:
            if n != 65535:
                all &= False
        if all:
            break
        buffer.append(new)
        
    time.sleep(1)

    ser.write(chr(27))
    
    final_str = ''
    for line in buffer:
        for val in line:
            final_str += str(val) + '\t'
        final_str += '\n'
    return final_str

@check_device
def erase_memory(ser):
    ser.tell('WE')
    
    max_timeout = 60 #seconds
    
    for i in range(60):
        line = ser.read_line()
        if to_string(line).strip().lower() == 'Flash erased!'.lower():
            return True
        time.sleep(1)
    return False
        

if __name__ == '__main__':
    import unittest
    
    class Commands(unittest.TestCase):
        def setUp(self):
            try:
                self.ser
            except AttributeError:
                self.ser = SuperSerial('/dev/tty.BlueSnapXP-600D-SPP-1',2400,timeout=2)
                
        
        def testReadMemory(self):
            data = read_memory(self.ser)
            print "!", data
            
            
    unittest.main()

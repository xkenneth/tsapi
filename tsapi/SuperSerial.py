import serial
import pdb
import time

def to_hex(var):
    try:
        return '%x' % var
    except TypeError:
        return var

def sequence_to_string(sequence):
    t = ''
    for i in sequence:
        t += i
    return t

def filter_junk(sequence):
    filtered_sequence = []
    for i in sequence:
        if i != '\x00' and i != '>':
            filtered_sequence.append(i)
    
    return filtered_sequence


def to_string(hex_string):
    hex_string.strip()
    sequence = []
    for i in range(len(hex_string)):
        sequence.append(hex_string[i])
    return sequence_to_string(filter_junk(sequence))

def to_int_list(hex_string):
    hex_string = to_string(hex_string)
    
    hex_values = []
    for hex_value in hex_string.split('\t'):
        hex_values.append(hex_value.strip())
    #get rid of junk
    good_hex_values = []
    for value in hex_values:
        if value != '':
            good_hex_values.append(int(value,16))
        
        
    return good_hex_values
        
    

class SuperSerial(serial.Serial):
    def read_buffer(self):
        return self.read(self.inWaiting())

    def read_line(self):
        line = ''
        
        div = 10.0
        timeout = None
        if self.timeout:
            timeout = self.timeout/div
        count = 0
        while(1):
            if self.inWaiting() > 0:
                char = self.read(1)
                line += char
                if char == '\r':
                    break
            else:
                if timeout:
                    time.sleep(timeout)
                if count > div:
                    break
                count += 1

        return line
                    
                
            
            
    
    def ask(self,command):
        command += '\r'
        self.write(command)

        if self.timeout:
            time.sleep(self.timeout)

        data = to_string(self.read_buffer())
        return data

    def tell(self,command,options=None,flush=False):
        if options:
            try:
                for opt in options:
                    command += ' ' + to_hex(opt)
            except TypeError:
                command += ' ' + to_hex(options)
        command += '\r'
        self.write(command)
        if flush:
            return self.read_buffer()

if __name__ == '__main__':
    import unittest
    
    class SSTests(unittest.TestCase):
        def setUp(self):
            self.FFFF = '\x00\n\x00F\x00F\x00F\x00F\x00\t\x00F\x00F\x00F\x00F\x00\t\x00F\x00F\x00F\x00F\x00\t\x00F\x00F\x00F\x00F\x00\t\x00F\x00F\x00F\x00F\x00\t\x00F\x00F\x00F\x00F\x00\t\x00F\x00F\x00F\x00F\x00\t\x00F\x00F\x00F\x00F\x00\t\x00F\x00F\x00F\x00F\x00\t\x00F\x00F\x00F\x00F\x00\t\x00F\x00F\x00F\x00F\x00\t\x00F\x00F\x00F\x00F\x00\t\x00F\x00F\x00F\x00F\x00\t\x00F\x00F\x00F\x00F\x00\t\x00\r'
        def test_int_list(self):
            print to_int_list(self.FFFF)

    unittest.main()

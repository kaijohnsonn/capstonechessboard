import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev
import time

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

class NFC():
    def __init__(self, bus=0, device=0, spd=1000000):
        self.reader = SimpleMFRC522()
        self.boards = {}
        
        self.bus = bus
        self.device = device
        self.spd = spd

    def reinit(self):
        self.reader.READER.spi = spidev.SpiDev()
        self.reader.READER.spi.open(self.bus, self.device)
        self.reader.READER.spi.max_speed_hz = self.spd
        self.reader.READER.MFRC522_Init()

    def close(self):
        self.reader.READER.spi.close()

    def addBoard(self, rid, pin):
        self.boards[rid] = pin
        GPIO.setup(pin, GPIO.OUT) 

    def selectBoard(self, rid):
        if not rid in self.boards:
            print("readerid " + rid + " not found")
            return False

        for loop_id in self.boards:
            GPIO.output(self.boards[loop_id], loop_id == rid)
        return True

    def read(self, rid):
       
        if not self.selectBoard(rid):
            return None
        self.reinit()
        cid, val = self.reader.read_no_block()
        self.close()
        
        if(cid == 1086441994700):
            card_name = "tag 1"
        elif(cid == 674643451980):
            card_name = "tag 2"
        elif(cid == 670298021964):
            card_name = "both?"
        else:
            card_name = cid
        
        return card_name
    
    def write(self, rid, value):
        if not self.selectBoard(rid):
            return False

        self.reinit()
        self.reader.write_no_block(value)
        self.close()
        return True


if __name__ == "__main__":
    
    nfc = NFC(bus=0, device=0, spd=1000000)
    
    try:
        while True:
            #for i in range(26):
            nfc.addBoard("reader1",8)
                #nfc.addBoard("reader2",6)  
              
            data = nfc.read("reader1")
            print(f"Data: {data}")
            #print(f"gpio: {i}")
        
            time.sleep(2)
            
            #data2 = nfc.read("reader2")
            #print(f"Data2: {data2}")
            
            #time.sleep(2)
           
    finally:
        nfc.close()
        GPIO.cleanup()
                                                                                                                               
from gpiozero import MCP3008
import time, string
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev
import time
from settings import BINARY_IN, SIGNAL, ENABLE, NUM_MUX, NUM_RFID, CONTROL_PINS, SLEEP
from lcds import print_lcd1, print_lcd2, clear_lcd1, clear_lcd2
from read_board import create_board_matrix

def setup():
    GPIO.setwarnings(False)
    nfc = NFC(bus=0, device=0, spd=1000000)
    nfc.addAllBoards()
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONTROL_PINS, GPIO.OUT)  # Set GPIO pins 7~10 as outputs
    GPIO.setup(SIGNAL, GPIO.IN)  # Set GPIO pin 23 as input
    GPIO.setup(ENABLE, GPIO.OUT)
    GPIO.output(ENABLE, GPIO.HIGH) 
    return nfc

#enable selected multiplexer
def setEnable(mux):
    for e in range(NUM_MUX):    
        if e == mux :
            GPIO.output(ENABLE[e], GPIO.LOW)   # LOW = open
            print(f"Enable mux{ENABLE[e]} ")
        else:
            GPIO.output(En[e], GPIO.HIGH)   # HIGH = closed
            print(f"Disable mux{ENABLE[e]} ")

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
    
    def addAllBoards(self):
        #rid = port#
        for pin in range(16):
            label = "port" + str(pin)

            self.boards[label] = BINARY_IN[pin]  #4 digit binary
            
    def selectBoard(self, rid):
        if not rid in self.boards:
            # print("readerid " + rid + " not found")
            return False

        for loop_id in self.boards:
            if loop_id == rid:
                GPIO.output(CONTROL_PINS, self.boards[rid])
        return True

    def read(self, rid):
       
        if not self.selectBoard(rid):
            print("fail to set mux value")
            return None
        
        GPIO.setup(SIGNAL, GPIO.OUT)
        self.reinit()
        cid, val = self.reader.read_no_block()
        self.close()
        
        GPIO.setup(SIGNAL, GPIO.IN)
        
        return cid #card id

def read_rfid():

    adc = MCP3008(channel=0)
    nfc = setup()
    mux_values = [0 for _ in range(64)]

    try:
        for mux_idx in range(NUM_MUX):          # select mux 
            setEnable(mux_idx)                  # enable specific mux
            # 0 - 15 
            for rfid_idx in range(NUM_RFID):    # select specific mux element 
                #read RFID
                label = "port" + str(NUM_RFID)
                data = nfc.read(label)

                mux_values[mux_idx * NUM_RFID + rfid_idx] = data
                time.sleep(SLEEP)

        for mux_idx in range(NUM_MUX):          # select mux 
            setEnable(mux_idx)                  # enable specific mux
            for rfid_idx in range(NUM_RFID):    # select specific mux element 
                #read RFID
                label = "port" + str(NUM_RFID)                                                                                                                                                                
                data = nfc.read(label)

                # If first read has square empty and second reads a value then set second value to mux_vals
                if mux_values[mux_idx * NUM_RFID + rfid_idx] != data:
                    if mux_values[mux_idx * NUM_RFID + rfid_idx] is 'None':
                        mux_values[mux_idx * NUM_RFID + rfid_idx] = data;
                time.sleep(SLEEP)
      
        GPIO.cleanup()
        adc.close()
        return format_read(mux_values)

    except KeyboardInterrupt:
        clear_lcd1()
        print_lcd1('RFID Hardware Error. Assistance Needed')

def format_read(mux_values):
    board_read = create_board_matrix
    for row in range(8):
        for col in range(8):
            board_read[row][col][0] = chr(65 + col) + str(row+1) 
            board_read[row][col][1] = mux_values[row * 8 + col]

    return board_read

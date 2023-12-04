from gpiozero import MCP3008
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev
import time
from read_board import *
from settings import BINARY_IN, SIGNAL, ENABLE, CONTROL_PINS, SLEEP

NUM_MUX = 1
NUM_RFID = 16
piece_types = {
    'WHITE_PAWNS': [674638471224, 1086443239712, 1025010441526, 197324582532, 262472937108, 885279628554, 677819850842, 886084476253],
    'WHITE_QUEENS': [817320435191, 1086826095664],
    'WHITE_KING': 1086506482152,
    'WHITE_BISHOP': [1024829496822, 888356478249],
    'WHITE_ROOK': [887100611849, 1086384323001],
    'WHITE_KNIGHT': [887690435844, 1088019047542],
    'BLACK_PAWNS': [887764360576, 1082951612691, 819694869989, 885265472801, 1017929936283, 886871104781, 678595076137, 1025077550394],
    'BLACK_QUEENS': [820184227231, 1084908255694],
    'BLACK_KING': 885751029001,
    'BLACK_BISHOP': [818226994432, 1084755163431],
    'BLACK_ROOK': [1019873602945, 674986205381]
}

def setup():
    GPIO.setwarnings(False)
    nfc = NFC(bus=0, device=0, spd=1000000)
    nfc.addAllBoards()
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONTROL_PINS, GPIO.OUT)  # Set GPIO pins 7~10 as outputs
    GPIO.setup(SIGNAL, GPIO.IN)  # Set GPIO pin 23 as input
    GPIO.setup(ENABLE, GPIO.OUT)
    #GPIO.output(ENABLE, GPIO.HIGH) 
    return nfc

#enable selected multiplexer
def setEnable(mux):
    for e in range(NUM_MUX):    
        if e == mux :
            GPIO.output(ENABLE[e], GPIO.LOW)   # LOW = open
            print(f"Enable mux{e} ")
        else:
            GPIO.output(ENABLE[e], GPIO.HIGH)   # HIGH = closed
            print(f"Disable mux{e} ")

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
            print("readerid " + rid + " not found")
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
            #setEnable(mux_idx)                  # enable specific mux
            GPIO.output(ENABLE[0], GPIO.LOW)
            # 0 - 15 
            for rfid_idx in range(NUM_RFID):    # select specific mux element 
                #read RFID
                label = "port" + str(rfid_idx)

                data = nfc.read(label)
                print(str(label) + ": " + str(data) + "\n")
                #mux_values[mux_idx * NUM_RFID + rfid_idx] = data
                time.sleep(SLEEP)
      
                #GPIO.cleanup()
                #adc.close()
        #return format_read(mux_values)
        #print_arr(format_read(mux_values))
    except Exception as error:
        print(error)    



def format_read(mux_values):
    board_read = create_board_matrix
    for row in range(8):
        for col in range(8):
            board_read[row][col][0] = chr(65 + col) + str(row+1) 
            id_num = mux_values[row * 8 + col]
            board_read[row][col][1] = identify_piece_type(id_num)

    return board_read

def identify_piece_type(number):
    for piece_type, numbers in piece_types.items():
        if isinstance(numbers, list):
            if number in numbers:
                return piece_type
        else:
            if number == numbers:
                return piece_type
    return "Unknown"

def print_arr(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            print(str(arr[i][j][0]) + ':' + str(arr[i][j][1] + '\n'))


if __name__ == "__main__":
    #while True:
     read_rfid()
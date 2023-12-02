from gpiozero import MCP3008
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev
import time
from settings import BINARY_IN, SIGNAL, ENABLE, NUM_MUX, NUM_RFID, CONTROL_PINS

def setup():
    GPIO.setwarnings(False)
    
    mux_values = [[0 for _ in range(16)] for _ in range(16)]

    # Initialize MCP3008 ADC on channel 0
    adc = MCP3008(channel=0)

    nfc = NFC(bus=0, device=0, spd=1000000)
    nfc.addAllBoards()
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BINARY_IN, GPIO.OUT)  # Set GPIO pins 7~10 as outputs
    GPIO.setup(SIGNAL, GPIO.IN)  # Set GPIO pin 23 as input
    GPIO.setup(En, GPIO.OUT)
    GPIO.output(En, GPIO.HIGH) 
    return nfc

def set_pin(output_pin):
    # Function to select pin on 74HC4067
    GPIO.output(BINARY_IN, CONTROL_PINS[output_pin])
    
#enable selected multiplexer
def setEnable(mux):
    for e in range(NUM_MUX):    
        if e == mux :
            GPIO.output(Enable[e], GPIO.LOW)   # LOW = open
            print(f"Enable mux{Enable[e]} ")
        else:
            GPIO.output(En[e], GPIO.HIGH)   # HIGH = closed
            print(f"Disable mux{Enable[e]} ")

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

            self.boards[label] = CONTROL_PINS[pin]  #4 digit binary
            
     
    def selectBoard(self, rid):
        if not rid in self.boards:
            print("readerid " + rid + " not found")
            return False

        for loop_id in self.boards:
            if loop_id == rid:
                print(f"board id {self.boards[rid][0]} {self.boards[rid][1]} {self.boards[rid][2]} {self.boards[rid][3]} \n")
                GPIO.output(BINARY_IN, self.boards[rid])
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
    nfc = setup()
    
    try:
        while True:
            count = 0
            for mux in range(NUM_MUX):       # select mux 
                setEnable(mux)               # enable specific mux
                for rfid in range(NUM_RFID): # select specific mux element 
                    #read RFID
                    label = f"port{                                                                                                                                                                   rfid}"
                    data = nfc.read(label)
                    mux_values[mux * NUM_RFID + rfid] = data
                    print(f"{label} Data: {data}")
                    time.sleep(0.1)

    except KeyboardInterrupt:
        # Cleanup GPIO and ADC on Ctrl+C
        GPIO.cleanup()
        adc.close()
    
from gpiozero import MCP3008
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

# Control pins output table in array form
# See truth table on page 2 of TI 74HC4067 data sheet
# Connect 74HC4067 S0~S3 to Raspberry Pi GPIO pins 7~4 respectively
# Connect 74HC4067 pin 1 to Raspberry Pi GPIO pin 23 (BCM numbering)
control_pins = [
    [0, 0, 0, 0],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [1, 1, 0, 0],
    [0, 0, 1, 0],
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [1, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 0, 1, 1],
    [0, 1, 1, 1],
    [1, 1, 1, 1]
]

# Holds incoming values from 74HC4067
mux_values = [0] * 16
Sig = 8
GPIOPins = [5,6,13,26]
En1 = 16
En2 = 12

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOPins, GPIO.OUT)  # Set GPIO pins 7~10 as outputs
GPIO.setup(Sig, GPIO.OUT)  # Set GPIO pin 23 as input
GPIO.setup(En1, GPIO.OUT)
GPIO.setup(En2, GPIO.OUT)
initial_pin_state = GPIO.input(Sig)

# Initialize MCP3008 ADC on channel 0
adc = MCP3008(channel=0)

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
        
        return cid
    

def set_pin(output_pin):
    # Function to select pin on 74HC4067
    GPIO.output(GPIOPins, control_pins[output_pin])
    print(f"P1:{control_pins[output_pin][0]}\nP2:{control_pins[output_pin][1]}\n P3:{control_pins[output_pin][2]}\nP4:{control_pins[output_pin][3]}")

def read_channel():
    # Read the analog value from the MCP3008 ADC
    return adc.value

    
def loop():
    nfc = NFC(bus=0, device=0, spd=1000000)
    try:
        GPIO.output(En1, 1)
        GPIO.output(En2, 0)
        for i in range(3):
            nfc.addBoard("reader1",8)
              
            data = nfc.read("reader1")
            print(f"Data: {data}")
            # GPIO.output(Sig, 1)
            
            GPIO.output(GPIOPins, control_pins[i])
       
            time.sleep(.5)
            
        GPIO.output(En1, 0)
        GPIO.output(En2, 1)
        for i in range(4):
            nfc.addBoard("reader1",8)
              
            data = nfc.read("reader1")
            print(f"Data: {data}")
            # GPIO.output(Sig, 1)
            
            GPIO.output(GPIOPins, control_pins[i])
       
            time.sleep(.5)
            
    except KeyboardInterrupt:
        # Cleanup GPIO and ADC on Ctrl+C
        GPIO.cleanup()
        adc.close()

if __name__ == "__main__":
    try:
        while True:
            loop()

    except KeyboardInterrupt:
        # Cleanup GPIO and ADC on Ctrl+C
        GPIO.cleanup()
        adc.close()
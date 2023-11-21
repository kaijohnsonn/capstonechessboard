# [S0,S1,S2,S3] = [26,13,6,5]
# Sig = 22
# En = [16,12,?,?]

from gpiozero import MCP3008
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev
import time


GPIO.setwarnings(False)

control_pins = [
    [0, 0, 0, 0],#RFID1
    [1, 0, 0, 0],#RFID2
    [0, 1, 0, 0],#LED1
    [1, 1, 0, 0],#LED2
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

mux_values = [0] * 16
bin_inputs = [5,6,13,26]
Sig = 22
Enable = [16,12] # 2 more once impl [23 24]

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(bin_inputs, GPIO.OUT)  # Set GPIO pins 7~10 as outputs
GPIO.setup(Sig, GPIO.IN)  # Set GPIO pin 23 as input
GPIO.setup(Enable, GPIO.OUT)
GPIO.output(Enable, GPIO.LOW) 

# Initialize MCP3008 ADC on channel 0
adc = MCP3008(channel=0)

def set_pin(output_pin):
    # Function to select pin on 74HC4067
    GPIO.output(bin_inputs, control_pins[output_pin])
    print(f"P1:{control_pins[output_pin][0]}\nP2:{control_pins[output_pin][1]}\n P3:{control_pins[output_pin][2]}\nP4:{control_pins[output_pin][3]}")

def read_channel():
    # Read the analog value from the MCP3008 ADC
    return adc.value

def display_data(output_pin):
    # Dumps captured data from array to console
    print()
    print("Values from multiplexer:")
    print("========================")
    print(f"[{control_pins[output_pin][0]}, {control_pins[output_pin][1]}, {control_pins[output_pin][2]}, {control_pins[output_pin][3]}]")

    #for i in range(15):
    #    print(f"Input I{i} = {mux_values[i]}")
    print("========================")

#enable selected multiplexer
def setEnable(mux):
    for e in range(2):    #CHANGE TO 4 ONCE ADDING OTHER MUX
        if e == mux :
            GPIO.output(Enable[e], GPIO.LOW)   # LOW = open 
        else:
            GPIO.output(Enable[e], GPIO.HIGH)   # HIGH = closed

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
            self.addBoard(label, pin)

            self.boards[label] = control_pins[pin]  #4 digit binary
            
     
    def selectBoard(self, rid):
        if not rid in self.boards:
            print("readerid " + rid + " not found")
            return False

        for loop_id in self.boards:
            if loop_id == rid:
                print(f"board id {self.boards[rid][0]} {self.boards[rid][1]} {self.boards[rid][2]} {self.boards[rid][3]} \n")
                GPIO.output(bin_inputs, self.boards[rid])
        return True

    def read(self, rid):
       
        if not self.selectBoard(rid):
            print("fail to set mux value")
            return None
        
        GPIO.setup(Sig, GPIO.OUT)
        self.reinit()
        cid, val = self.reader.read_no_block()
        self.close()
        
        GPIO.setup(Sig, GPIO.IN)
        
        return cid #card id

       
if __name__ == "__main__":
    
    nfc = NFC(bus=0, device=0, spd=1000000)
    nfc.addAllBoards()
    
    try:
        while True:
            for e in range(1):       # select mux CHANGE TO 4 ONCE ADDING OTHER MUX
                setEnable(e)         # enable specific mux
                for i in range(2):  # select specific mux element CHANGE TO 16 ONCE ADDING OTHER RFIDS
                    #read RFID
                    label = "port" + str(i)
                    data = nfc.read(label)
                    print(f"{label} Data: {data}")
                    time.sleep(2)

    except KeyboardInterrupt:
        # Cleanup GPIO and ADC on Ctrl+C
        GPIO.cleanup()
        adc.close()
        
from gpiozero import MCP3008
import time
import RPi.GPIO as GPIO
from gpiozero import Button
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev

GPIO.setwarnings(False)

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
Delay = 0.1

#button1 = Button(Sig) 

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOPins, GPIO.OUT)  # Set GPIO pins 7~10 as outputs
GPIO.setup(Sig, GPIO.IN)  # Set GPIO pin 23 as input
GPIO.setup(En1, GPIO.OUT)
GPIO.setup(En2, GPIO.OUT)
#initial_pin_state = GPIO.input(Sig)

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
        try:
            self.reader.READER.spi = spidev.SpiDev()
            self.reader.READER.spi.open(self.bus, self.device)
            self.reader.READER.spi.max_speed_hz = self.spd
            self.reader.READER.MFRC522_Init()
        except Exception as e:
            print("Error during RFID initialization:")
            print(traceback.format_exc())
            
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

def read_channel():
    # Read the analog value from the MCP3008 ADC
    return adc.value

def display_data(output_pin):
    # Dumps captured data from array to console
    print()
    print("Values from multiplexer:")
    print("========================")
    print(f"P1:{control_pins[output_pin][0]}\nP2:{control_pins[output_pin][1]}\n P3:{control_pins[output_pin][2]}\nP4:{control_pins[output_pin][3]}")

    #for i in range(15):
    #    print(f"Input I{i} = {mux_values[i]}")
    print("========================")

   
def button1_pressed():
    print("Button 1 pressed!")

def button2_pressed():
    print("Button 2 pressed!")
    
def no_press():
    katie = 1
    
def loop():
    try:
        nfc = NFC(bus=0, device=0, spd=1000000)
        nfc.reinit()
        
        GPIO.output(En1, 0)
        GPIO.output(En2, 1)
        
        #GPIO.setup(Sig, GPIO.IN)
        GPIO.output(GPIOPins, control_pins[1])
        time.sleep(Delay)                                                                                                                                                                                                            
        nfc.addBoard("reader1",Sig)
        try:
            data = nfc.read("reader1")
            #                                                 print(f"Data 1: {data}")
        except Exception as e:
            print(f"Exception during RFID reading: {e}")
        time.sleep(Delay)
        
       # GPIO.output(En1, 0)
       # GPIO.output(En2, 1)
        
        #GPIO.setup(Sig, GPIO.IN)
        GPIO.output(GPIOPins, control_pins[0])
        time.sleep(Delay) 
        nfc.addBoard("reader1",Sig)
        try:
            data = nfc.read("reader1")
            print(f"Data 2: {data}")
        except Exception as e:
            print(f"Exception during RFID reading: {e}")
        time.sleep(Delay)        
        
        
        
        '''for i in range(3):
            if (i == 1):
                GPIO.setup(Sig, GPIO.IN)
                GPIO.output(GPIOPins, control_pins[i])
                time.sleep(0.1) 
                nfc.addBoard("reader1",Sig)
                data = nfc.read("reader1")
                #print(str(i)+"\n")
                print(f"Data: {data}")
                time.sleep(2)
        
            else:
                #button1.when_pressed = no_press
                GPIO.setup(Sig, GPIO.OUT)
                GPIO.output(Sig, 1)
                GPIO.output(GPIOPins, control_pins[i])
                print("Not pressed" + str(i))
                time.sleep(2) 


        GPIO.output(En1, 0)
        GPIO.output(En2, 1)
        
        for i in range(3):
            if (i == 1):
                #GPIO.setup(Sig, GPIO.IN)
                GPIO.output(GPIOPins, control_pins[1])
                nfc.addBoard("reader1",Sig)
                data = nfc.read("reader1")
                #print(str(i)+"\n")
                print(f"Data: {data}")
                time.sleep(2)
            
            else:
                #button1.when_pressed = no_press
                GPIO.setup(Sig, GPIO.OUT)
                GPIO.output(Sig, 1)
                GPIO.output(GPIOPins, control_pins[i])
                print("Not pressed" + str(i))
                time.sleep(2)
        '''
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


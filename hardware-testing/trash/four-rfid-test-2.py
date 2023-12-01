import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define the control pins for the multiplexers
EN_PIN = 17  # Enable pin (EN)
S0_PIN = 18  # Address pins (S0)
S1_PIN = 27  # Address pins (S1)
S2_PIN = 22  # Address pins (S2)
S3_PIN = 23  # Address pins (S3)
SIG_PIN = 26 # Address pins (SIG)



# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup([EN_PIN, S0_PIN, S1_PIN, S2_PIN, S3_PIN], GPIO.OUT)

# Function to select the channel on the multiplexer
def select_channel(multiplexer, channel):
    # Ensure EN is low to enable the multiplexer
    GPIO.output(EN_PIN, GPIO.LOW)

    # Set the address pins (S0, S1, S2, S3) for the specified multiplexer
    GPIO.output(S0_PIN, multiplexer & 1)
    GPIO.output(S1_PIN, (multiplexer >> 1) & 1)
    GPIO.output(S2_PIN, (multiplexer >> 2) & 1)
    GPIO.output(S3_PIN, (multiplexer >> 3) & 1)

    # Select the desired channel on the specified multiplexer
    channel_bits = [int(bit) for bit in format(channel, '04b')]
    for bit, channel_pin in zip(channel_bits, [8, 9, 10, 11]):
        GPIO.output(channel_pin, bit)

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
        if rid not in self.boards:
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

        if cid == 1086441994700:
            card_name = "tag 1"
        elif cid == 674643451980:
            card_name = "tag 2"
        elif cid == 670298021964:
            card_name = "both?"
        else:
            card_name = cid

        return card_name

def main():
    
    nfc = NFC(bus=0, device=0, spd=1000000)
    try:
        for multiplexer in range(0):
            for channel in range(1):
                # Call the function to select the channel
                print("here")
                select_channel(multiplexer, channel)
                
                #nfc.addBoard("reader1", 5)
                #data = nfc.read("reader1")
                print(f"Data: {data}")

                time.sleep(2)
    finally:
        nfc.close()
        GPIO.cleanup()
        
if __name__ == "__main__":
    main()


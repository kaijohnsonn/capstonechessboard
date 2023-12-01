import RPi.GPIO as GPIO
import spidev
from mfrc522 import SimpleMFRC522
import time
GPIO.setwarnings(False)
# Multiplexer control pins
s0 = 5
s1 = 6
s2 = 13
s3 = 19
en = 17
sig = 26



# Number of multiplexers
num_multiplexers = 1

# Multiplexer in "SIG" pin
SIG_pin = 26

# RFID reader setup
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

    def addBoard(self, multiplexer, rid, pin):
        self.boards[(multiplexer, rid)] = pin
        GPIO.setup(pin, GPIO.OUT)

    def selectBoard(self, multiplexer, rid):
        if (multiplexer, rid) not in self.boards:
            print(f"readerid {rid} not found on multiplexer {multiplexer}")
            return False

        for (loop_multiplexer, loop_id) in self.boards:
            GPIO.output(self.boards[(loop_multiplexer, loop_id)], loop_id == rid)
        return True

    def read(self, multiplexer, rid):
        if not self.selectBoard(multiplexer, rid):
            return None
        self.reinit()
        cid, val = self.reader.read_no_block()
        self.close()
        return cid

def setup_multiplexer():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(s0, GPIO.OUT)
    GPIO.setup(s1, GPIO.OUT)
    GPIO.setup(s2, GPIO.OUT)
    GPIO.setup(s3, GPIO.OUT)
    GPIO.output(s0, GPIO.LOW)
    GPIO.output(s1, GPIO.LOW)
    GPIO.output(s2, GPIO.LOW)
    GPIO.output(s3, GPIO.LOW)

def read_multiplexer(multiplexer, channel, nfc):
    control_pins = [s0, s1, s2, s3]

    mux_channel = [
        [0, 0, 0, 0],  # channel 0
        [1, 0, 0, 0],  # channel 1
        [0, 1, 0, 0],  # channel 2
        [1, 1, 0, 0],  # channel 3
        [0, 0, 1, 0],  # channel 4
        [1, 0, 1, 0],  # channel 5
        [0, 1, 1, 0],  # channel 6
        [1, 1, 1, 0],  # channel 7
        [0, 0, 0, 1],  # channel 8
        [1, 0, 0, 1],  # channel 9
        [0, 1, 0, 1],  # channel 10
        [1, 1, 0, 1],  # channel 11
        [0, 0, 1, 1],  # channel 12
        [1, 0, 1, 1],  # channel 13
        [0, 1, 1, 1],  # channel 14
        [1, 1, 1, 1]   # channel 15e
    ]

    for i in range(4):
        GPIO.output(control_pins[i], mux_channel[channel][i])
        nfc.addBoard("reader1",5)

def main():
    setup_multiplexer()
    nfc = NFC(bus=0, device=0, spd=1000000)

    try:
        for m in range(num_multiplexers):
            for i in range(16):
                
                read_multiplexer(m, i, nfc)
                data = nfc.read(0, "reader1")
                print(f"Data on multiplexer {m}, channel { mux_channel[i][0]}: {data}")
                time.sleep(2)
    finally:
        nfc.close()
        GPIO.cleanup()

if __name__ == "__main__":
    main()

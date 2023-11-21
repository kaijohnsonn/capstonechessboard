import RPi.GPIO as GPIO
import spidev
from mfrc522 import SimpleMFRC522
import time

# Multiplexer control pins
s0 = 8
s1 = 9
s2 = 10
s3 = 11

# Multiplexer in "SIG" pin
SIG_pin = 0

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
        return cid

    def write(self, rid, value):
        if not self.selectBoard(rid):
            return False
        self.reinit()
        self.reader.write_no_block(value)
        self.close()
        return True

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

def read_multiplexer(channel):
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

def main():
    setup_multiplexer()
    nfc = NFC(bus=0, device=0, spd=1000000)
    try:
        while True:
            for i in range(16):
                read_multiplexer(i)
                data = nfc.read("reader1")
                print(f"Data at channel {i}: {data}")
                time.sleep(2)
    finally:
        nfc.close()
        GPIO.cleanup()

if __name__ == "__main__":
    main()

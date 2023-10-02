from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()


"""
king: "K" queen: "Q" rook: "R" bishop: "B" knight: "N"
(ex: 2.Nf3)
pawn you see only the name of the square where the pawn moves.
(ex: 1.e4)
"""




button_pins = [1, 2]  # Example GPIO pins for two buttons
rfid_scanners = [SimpleMFRC522(0), SimpleMFRC522(1),SimpleMFRC522(2), SimpleMFRC522(3)]  # Initialize two RFID scanners

def on_button_pressed(button_id):
    print(f"Button {button_id} pressed.")
    
    read_rfids()


def read_rfids():
    for idx, scanner in enumerate(rfid_scanners):
        print(f"Scanning RFID scanner {idx}...")
        try:
            id, text = scanner.read()
            print(f"RFID scanner {idx} - Card ID: {id}, Data: {text}")
        except Exception as e:
            print(f"Error reading from RFID scanner {idx}: {str(e)}")

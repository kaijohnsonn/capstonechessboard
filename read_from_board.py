from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()


"""
king: "K" queen: "Q" rook: "R" bishop: "B" knight: "N"
(ex: 2.Nf3)
pawn you see only the name of the square where the pawn moves.
(ex: 1.e4)
king is threatened: "+" [end of string]
checkmate: "#" [end of string]
- Kingside Castling: O-O
- Queenside Castling: O-O-O
For capturing, put an “x” between piece moving and square moved to
Pawn promotion: [file][row] + "=" + [new-piece-code]
* files: a-h and ranks: 1-8.
"""
# convert the move made by player into chess notation
# check for castling [o-o] or [o-o-o] 
# [piece-code]+[from-file]+["x"]?+[to-file]+[to-row] + ["+"/"#""]
def chess_notation():
    
    return ""



button_pins = [1, 2]  # Example GPIO pins for two buttons
rfid_scanners = [SimpleMFRC522(0), SimpleMFRC522(1),SimpleMFRC522(2), SimpleMFRC522(3)]  # Initialize four RFID scanners

# user presses button signifying end of their turn
def on_user_button_press():
        print(f"Button {button_id} pressed.")  
        read_rfids()

#user presses button signifying they made the computer/other player's move
def on_comp_button_press():
         print(f"Button {button_id} pressed.")
         # start user's move timer

# read from sensors and detect changes from previous move 
"""
RFID tags should differentiate - 
king: "K" queen: "Q" rook: "R" bishop: "B" knight: "N"
RFID scanners should be assigned position (ex: e5)

"""
def read_rfids():
    for idx, scanner in enumerate(rfid_scanners):
        print(f"Scanning RFID scanner {idx}...")
        try:
            id, text = scanner.read()
            print(f"RFID scanner {idx} - Card ID: {id}, Data: {text}")
        except Exception as e:
            print(f"Error reading from RFID scanner {idx}: {str(e)}")



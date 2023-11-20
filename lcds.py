# Has not been tested yet

import board
import busio
from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C

def initialize_lcd(address=0x27):
    lcd_columns = 16
    lcd_rows = 2
    i2c = busio.I2C(board.SCL, board.SDA)
    lcd = Character_LCD_I2C(i2c, lcd_columns, lcd_rows, address=address)
    return lcd

def write_to_lcd(lcd, line1, line2):
    lcd.clear()
    lcd.message = f"{line1}\n{line2}"

# Initialize two LCD displays with different addresses
lcd1 = initialize_lcd(address=0x27)
lcd2 = initialize_lcd(address=0x28)

# Write to the first LCD display
write_to_lcd(lcd1, "LCD 1", "Line 1")

# Write to the second LCD display
write_to_lcd(lcd2, "LCD 2", "Line 2")
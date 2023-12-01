import I2C_LCD_driver
from time import *

# with the timer block on the right side of the board, lcd 1 is 0x26 and
# closest to you. the other is lcd 2

ADDRESS_LCD1 = 0x26
ADDRESS_LCD2 = 0x27

lcd1 = I2C_LCD_driver.lcd(ADDRESS_LCD1)
lcd2 = I2C_LCD_driver.lcd(ADDRESS_LCD2)

def print_lcd1(message):
    lcd1.lcd_display_string(message, 1)
    
def clear_lcd1():
    lcd1.lcd_clear()
    
def print_lcd2(message):
    lcd2.lcd_display_string(message, 1)

def clear_lcd2():
    lcd2.lcd_clear()

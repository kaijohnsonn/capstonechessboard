import I2C_LCD_driver
from time import *

ADDRESS_LCD1 = 0x26
ADDRESS_LCD2 = 0x27

lcd1 = I2C_LCD_driver.lcd(ADDRESS_LCD1)
lcd2 = I2C_LCD_driver.lcd(ADDRESS_LCD2)

lcd1.lcd_display_string("Hello World!", 1)
lcd2.lcd_display_string("Hello Katie!", 1)
#https://stackoverflow.com/questions/13034496/using-global-variables-between-files

global but1_pressed
global but2_pressed
global BINARY_IN
global CONTROL_PINS
global SIGNAL
global ENABLE
global NUM_MUX
global NUM_RFID
global SLEEP

but1_pressed = [False]
but2_pressed = [False]
CONTROL_PINS = [5,6,13,26]
SIGNAL = 8
ENABLE = [12, 16, 23, 24]
NUM_MUX = 4
NUM_RFID = 16
SLEEP = 0.01

BINARY_IN = [
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

global WHITE_PAWNS
global WHITE_QUEENS
global WHITE_KING
global WHITE_BISHOP
global WHITE_ROOK

global BLACK_PAWNS
global BLACK_QUEENS
global BLACK_KING
global BLACK_BISHOP
global BLACK_ROOK

WHITE_PAWNS =      [674638471224, 1086443239712, 1025010441526, 197324582532, 
                     262472937108, 885279628554, 677819850842, 886084476253]

WHITE_QUEENS =     [817320435191, 1086826095664]
WHITE_KING =         1086506482152
WHITE_BISHOP =     [1024829496822, 888356478249]
WHITE_ROOK =       [887100611849, 1086384323001]
WHITE_KNIGHT =     [887690435844, 1088019047542]

BLACK_PAWNS =      [887764360576, 1082951612691, 819694869989, 885265472801, 
                            1017929936283, 886871104781, 678595076137, 1025077550394]
BLACK_QUEENS =     [820184227231, 1084908255694]
BLACK_KING =       885751029001
BLACK_BISHOP =     [818226994432, 1084755163431]
BLACK_ROOK =       [1019873602945, 674986205381]
    
    
    

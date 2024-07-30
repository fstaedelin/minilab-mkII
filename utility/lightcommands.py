import device

SET_COLOR_COMMAND = bytes([0x02, 0x00, 0x10])

# 8*2-pad

ID_PAD1 = 0x70
ID_PAD2 = 0x71
ID_PAD3 = 0x72
ID_PAD4 = 0x73
ID_PAD5 = 0x74
ID_PAD6 = 0x75
ID_PAD7 = 0x76
ID_PAD8 = 0x77

ID_PAD9 = 0x78
ID_PAD10 = 0x79
ID_PAD11 = 0x7A
ID_PAD12 = 0x7B
ID_PAD13 = 0x7C
ID_PAD14 = 0x7D
ID_PAD15 = 0x7E
ID_PAD16 = 0x7F

# Color codes
C_OFF = 0x00
C_RED = 0x01
C_BLUE = 0x10
C_PURPLE = 0x11
C_GREEN = 0x04
C_YELLOW = 0x05
C_CYAN = 0x14
C_WHITE = 0x7F

# Matrix with PADS IDS
MATRIX_IDS_PAD = [
    [ID_PAD1, ID_PAD2, ID_PAD3, ID_PAD4, ID_PAD5, ID_PAD6, ID_PAD7, ID_PAD8],
    [ID_PAD9, ID_PAD10, ID_PAD11, ID_PAD12, ID_PAD13, ID_PAD14, ID_PAD15, ID_PAD16],
]

def send_to_device(data) :
    #The only function that will send SysEx data to the controller
    #Specific SYSEX commands are always prefixed by the following byte sequence: 
    #bytes([0xF0, 0x00, 0x20, 0x6B, 0x7F, 0x42]) + data + bytes([0xF7])
    # Which stands for:
        #   open,blank, Arturia ID, standard msg                close
    device.midiOutSysex(bytes([0xF0, 0x00, 0x20, 0x6B, 0x7F, 0x42]) + data + bytes([0xF7]))

def SetPadColor(pad, color) :
    send_to_device(SET_COLOR_COMMAND + bytes([pad, color]))
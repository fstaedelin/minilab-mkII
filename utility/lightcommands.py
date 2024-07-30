import device

ID_PADS = {
    1: 0x70,    9: 0x78, 
    2: 0x71,    10: 0x79,
    3: 0x72,    11: 0x7A,
    4: 0x73,    12: 0x7B,
    5: 0x74,    13: 0x7C,
    6: 0x75,    14: 0x7D,
    7: 0x76,    15: 0x7E,
    8: 0x77,    16: 0x7F,
}

SET_COLOR_COMMAND = bytes([0x02, 0x00, 0x10])

# Matrix with PADS IDS
MATRIX_IDS_PAD = [
    [ID_PADS[1], ID_PADS[2], ID_PADS[3], ID_PADS[4], ID_PADS[5], ID_PADS[6], ID_PADS[7], ID_PADS[8]],
    [ID_PADS[9], ID_PADS[10], ID_PADS[11], ID_PADS[12], ID_PADS[13], ID_PADS[14], ID_PADS[15], ID_PADS[16]],
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
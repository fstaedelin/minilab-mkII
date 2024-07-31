import device

SET_COLOR_COMMAND = bytes([0x02, 0x00, 0x10])

def send_to_device(data) :
    #The only function that will send SysEx data to the controller
    #Specific SYSEX commands are always prefixed by the following byte sequence: 
    #bytes([0xF0, 0x00, 0x20, 0x6B, 0x7F, 0x42]) + data + bytes([0xF7])
    # Which stands for:
        #   open,blank, Arturia ID, standard msg                close
    device.midiOutSysex(bytes([0xF0, 0x00, 0x20, 0x6B, 0x7F, 0x42]) + data + bytes([0xF7]))

def SetPadColor(pad, color) :
    send_to_device(SET_COLOR_COMMAND + bytes([pad, color]))
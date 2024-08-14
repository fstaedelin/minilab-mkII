import device
import time
from utility.mappings.maincontrollertypes import Pad
from utility.mappings.dictionaries import COLORS
from utility.mappings.baseclasses import ColorMapList
# MIT License
# Copyright (c) 2020 Ray Juang

# This class organize the LED functions usefull for visual returns.
# The class sets up a LED map depending on the controller

blinking_pattern = [COLORS['BLUE'],COLORS['PURPLE'],COLORS['GREEN'],COLORS['YELLOW'],COLORS['CYAN'],COLORS['WHITE'],COLORS['RED']]
SET_COLOR_COMMAND = bytes([0x02, 0x00, 0x10])

class MiniLabLeds:
    ID_PADS = [0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E, 0x7F]
    
    # Color codes
    COLORS = {
        'OFF' : 0x00,
        'RED' : 0x01,
        'BLUE' : 0x10,
        'PURPLE' : 0x11,
        'GREEN' : 0x04,
        'YELLOW' : 0x05,
        'CYAN' : 0x14,
        'WHITE' : 0x7F
    }


    def __init__(self, padList: "list[Pad]"):
        # A dict of 16 colorMaps, one for each pad
        self.PadLights : dict[int, ColorMapList] = {}
        i=0
        for pad in padList:
            self.PadLights[self.ID_PADS[i]] = pad.colorMaps
            i+=1
            
    def Welcome(self):
        for i in blinking_pattern:
            for pad in self.PadLights.items():
                    #print(bytes([pad[0]]))
                self.SetPadColor(pad[0] , i)
            time.sleep(0.25)
                
    def SetPadColor(self, PAD_ID, color):
        data=bytes([])
        data += bytes([PAD_ID, color])
        send_to_device(SET_COLOR_COMMAND + data)
        
    def SetDefault(self) :
        for key, value in self.PadLights.items():
            self.SetPadColor(key, value._colorMaps[0][0])
    
    def Update(self) :
        for colorMap in self.PadLights:
            if colorMap._isChanged:
                self.SetPadColor(colorMap[i].getID(), colorMap[colorMap._activeColorMaps][0])
                
def send_to_device(data) :
#The only function that will send SysEx data to the controller
#Specific SYSEX commands are always prefixed by the following byte sequence: 
#bytes([0xF0, 0x00, 0x20, 0x6B, 0x7F, 0x42]) + data + bytes([0xF7])
# Which stands for:
    #   open,blank, Arturia ID, standard msg                close
    device.midiOutSysex(bytes([0xF0, 0x00, 0x20, 0x6B, 0x7F, 0x42]) + data + bytes([0xF7]))

                
                
        
            
    

   
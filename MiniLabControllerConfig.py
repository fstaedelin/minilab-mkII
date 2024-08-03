import time
import transport

import utility.colors as colors
from utility.lightcommands import SetPadColor

from backend.MiniLabMk2Mapping import MiniLabMapping
from mappings.example_mapping import exampleMapping
# This is the master class. It will run the init lights pattern 
# and call the others class to process MIDI events

TEMP = 0.25

class ControllerConfig :
    
    def __init__(self, mapping: MiniLabMapping):
        self._lights = MiniLabmk2Led()
        self._lightReturn = MiniLabLightReturn(mapping)
        self._mapping = mapping
        self.blinkableIDs = []
        self.blinkingcolor1 = []
        self.blinkingcolor2 = []
        for pad in mapping.pads:
            if pad.LED_BLINKONPLAY:
                self.blinkableIDs.append(pad.ID_PAD)
                self.blinkingcolor1.append(pad.LED_COLOR)
                self.blinkingcolor2.append(pad.LED_BLINKCOLOR)
        
    def SetDefault(self) :
        for pad in self._mapping.pads:
            SetPadColor(pad.ID_PAD, pad.LED_COLOR)
            
    def InitSync(self):
        # Syncs up all visual indicators on keyboard with changes from FL Studio.
        for i in colors.blinking_pattern :
            for pad in self._mapping.pads:
                SetPadColor(pad.ID_PAD, i)
            time.sleep(TEMP)
        self.SetDefault()
        
    def Sync(self):
        self.SetDefault()
        
    def ProcessBlink(self, value):
        if transport.isPlaying():
                i=0
                for blinkingpad in self.blinkableIDs:
                    if value == 0:
                        SetPadColor(blinkingpad, self.blinkingcolor2[i])
                    else:
                        SetPadColor(blinkingpad, COLORS['OFF'])
                    i+=1
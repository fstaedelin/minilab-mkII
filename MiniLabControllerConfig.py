import time

from MiniLabLeds import MiniLabmk2Led
from MiniLabReturn import MiniLabLightReturn

import utility.colors as colors

from mapping import example_mapping
# This is the master class. It will run the init lights pattern 
# and call the others class to process MIDI events

TEMP = 0.25

class MidiControllerConfig :
    
    def __init__(self):
        self._lights = MiniLabmk2Led()
        self._lightReturn = MiniLabLightReturn()
        
    def lights(self):
        return self._lights

    def LightReturn(self) :
        return self._lightReturn
    
    def SetLights(self, led_mapping):
        return self._lights.SetLights(led_mapping)
    
    def SetPadLights(self, color_matrix):
        return self._lights.SetPadLights(color_matrix)
    
    def SetAllPadLights(self, color):
        return self._lights.SetAllPadLights(color)
    
    def SetDefault(self) :
        self.SetPadLights(colors.default_pad_colors)
    
    def SetTransport(self) :
        self.SetPadLights(colors.transport_pad_colors)
    
    def Sync(self):
        # Syncs up all visual indicators on keyboard with changes from FL Studio.
        for i in colors.blinking_pattern :
            self.SetAllPadLights(i)
            time.sleep(TEMP)
        self.SetTransport()

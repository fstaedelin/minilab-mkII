import time
import transport

from mappings.mappings_backend.MiniLabMk2Mapping import MiniLabMapping
from MiniLabLeds import MiniLabLeds
from MiniLabReturn import MiniLabLightReturn

# This is the master class. It will run the init lights pattern 
# and call the others class to process MIDI events



class ControllerConfig :
    
    def __init__(self, mapping: MiniLabMapping):
        self._lights = MiniLabLeds(mapping.pads)
        self._colorMaps = self._lights.PadLights
        self._lightReturn = MiniLabLightReturn(self._lights)
        
            
    def InitSync(self):
        # Syncs up all visual indicators on keyboard with changes from FL Studio.
        self.lights().Welcome()
        self.SetDefault()
        
    def Sync(self):
        self.SetDefault()
    
    def lights(self):
        return self._lights
    
    def lightReturn(self):
        return self._lightReturn
    
    def SetDefault(self):
        self.lights().SetDefault()
        
    def ProcessBlink(self, value):
        self.lightReturn().ProcessBlink(value)
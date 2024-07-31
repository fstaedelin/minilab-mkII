from backend.baseclasses import *
from mapping.dictionaries  import COLORS
from mapping.dictionaries  import ID_PADS
from mapping.dictionaries  import RESERVED_CC

class Pad(multipleControl):
    ID_PAD = 0x00
    LED_COLOR = COLORS['RED']
    LED_BLINKONPLAY = False
    LED_BLINKCOLOR = COLORS['RED']
    
    def __init__(self, callback_fn=None, controlMode=ControlModes['CC'][1], dataIn=0, LED_COLOR = COLORS['RED'], LED_BLINKONPLAY = False, LED_BLINKCOLOR = COLORS['OFF']):
        super().__init__('PAD', callback_fn, controlMode, dataIn)
        self.LED_COLOR = LED_COLOR
        self.LED_BLINKONPLAY = LED_BLINKONPLAY
        self.LED_BLINKCOLOR = LED_BLINKCOLOR
        self.SetID()
        
    
    def SetID(self):
        self.ID_PAD = ID_PADS[self.number]

class Knob(multipleControl):    
    def __init__(self, callback_fn=None, controlMode=ControlModes['CC'][1], dataIn=0):
        super().__init__('KNOB', callback_fn,controlMode, dataIn)
    
    def setNumber(self, num):
        self.number = num
        
class ModWheel(Control):    
    def __init__(self, callback_fn=None, channel=1):
        super().__init__('MOD_WHEEL', callback_fn,ControlModes['CC'][channel], RESERVED_CC['MOD_WHEEL'])

class PitchBend(Control):    
    def __init__(self, callback_fn=None, channel=1):
        super().__init__('PITCH_BEND', callback_fn, ControlModes['PITCHBEND'][channel])
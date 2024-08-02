from backend.baseclasses import *
from mapping.dictionaries  import COLORS
from mapping.dictionaries  import ID_PADS
from mapping.dictionaries  import RESERVED_CC

"""
This file contains specifications of base classes of controls useful for MiniLabmkII: Pad, Knob, ModWheel, PitchBend
"""

class Pad(multipleControl):
    def __init__(self, callback_fn=None, controlMode=ControlModes['CC'][1], dataOut=0, LED_COLOR = COLORS['RED'], LED_BLINKONPLAY = False, LED_BLINKCOLOR = COLORS['OFF']):
        """A Pad.

        Args:
            callback_fn (function, optional): The function the button should activate. Defaults to None.
            controlMode (int, optional): First MIDI argument of sent message. Use utility.dictionnaries.ControlModes to map them easily. Defaults to ControlModes['CC'][1].
            dataOut (int, optional): Second MIDI argument of sent message. Usually between 0 and 127. Defaults to 0.
            LED_COLOR (int, optional): The Pad color. Use utility.dictionaries.COLORS to set it up. Defaults to COLORS['RED'].
            LED_BLINKONPLAY (bool, optional): Does the pad blink when FL is playing ?. Defaults to False.
            LED_BLINKCOLOR (int, optional): If it blinks, what color ? Use utility.dictionaries.COLORS to set it up. Defaults to COLORS['OFF'].
        """
        super().__init__('PAD', callback_fn, controlMode, dataOut)
        self.LED_COLOR = LED_COLOR
        self.LED_BLINKONPLAY = LED_BLINKONPLAY
        self.LED_BLINKCOLOR = LED_BLINKCOLOR
        self.SetID()
        
    
    def SetID(self):
        self.ID_PAD = ID_PADS[self.number]

class Knob(multipleControl):
    def __init__(self, callback_fn=None, controlMode=ControlModes['CC'][1], dataOut=0):
        """A Knob.

        Args:
            callback_fn (function, optional): The function the button should activate. Defaults to None.
            controlMode (int, optional): First MIDI argument of sent message. Use utility.dictionnaries.ControlModes to map them easily. Defaults to ControlModes['CC'][1].
            dataOut (int, optional): Second MIDI argument of sent message. Usually between 0 and 127. Defaults to 0.
        """
        super().__init__('KNOB', callback_fn, controlMode, dataOut)
    
    def setNumber(self, num):
        self.number = num
        
class ModWheel(Control):
    def __init__(self, callback_fn=None, channel=1):
        """The Modulation Wheel.

        Args:
            callback_fn (function, optional): The function the button should activate. Defaults to None.
            controlMode (int, optional): First MIDI argument of sent message. Use utility.dictionnaries.ControlModes to map them easily. Defaults to ControlModes['CC'][1].
            dataOut (int, optional): Second MIDI argument of sent message. Usually between 0 and 127. Defaults to 0.
        """
        super().__init__('MOD_WHEEL', callback_fn, ControlModes['CC'][channel], RESERVED_CC['MOD_WHEEL'])

class PitchBend(Control):    
    def __init__(self, callback_fn=None, channel=1):
        """The Pitch Bend.

        Args:
            callback_fn (function, optional): The function the button should activate. Defaults to None.
            controlMode (int, optional): First MIDI argument of sent message. Use utility.dictionnaries.ControlModes to map them easily. Defaults to ControlModes['CC'][1].
            dataOut (int, optional): Second MIDI argument of sent message. Usually between 0 and 127. Defaults to 0.
        """
        super().__init__('PITCH_BEND', callback_fn, ControlModes['PITCHBEND'][channel])
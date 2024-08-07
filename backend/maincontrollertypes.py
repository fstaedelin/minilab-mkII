from backend.baseclasses import *
from backend.dictionaries  import COLORS
from backend.dictionaries  import RESERVED_CC
from backend.dictionaries  import SYSEX

"""
    This file contains specifications of base classes of controls useful for MiniLabmkII: Pad, Knob, ModWheel, PitchBend
"""

class Pad(MultipleControl):
    def __init__(self, callback_fn = function_dummy, LED_COLOR_DEFAULT = COLORS['RED'], LED_COLOR_BEAT = COLORS['OFF'], LED_COLOR_BAR = COLORS['OFF'], controlMode=ControlModes['CC'][0], controlData1=MultipleControl.AUTOCC_KEY, condition = True, name = 'PAD'):
        """A Pad.

        Args:
            callback_fn (function, optional): The function the button should activate. Defaults to None.
            controlMode (int, optional): First MIDI argument of sent message. Use utility.dictionnaries.ControlModes to map them easily. Defaults to ControlModes['CC'][1].
            dataOut (int, optional): Second MIDI argument of sent message. Usually between 0 and 127. Defaults to 0.
            LED_COLOR (int, optional): The Pad color. Use utility.dictionaries.COLORS to set it up. Defaults to COLORS['RED'].
            PLAY (bool, optional): Does the pad blink when FL is playing ?. Defaults to False.
            LED_BLINKCOLOR (int, optional): If it blinks, what color ? Use utility.dictionaries.COLORS to set it up. Defaults to COLORS['OFF'].
        """
        super().__init__(callback_fn, controlMode, controlData1, name)
        self._initColorMaps(LED_COLOR_DEFAULT, LED_COLOR_BEAT, LED_COLOR_BAR, condition)
        
    def _initColorMaps(self, LED_COLOR_DEFAULT = COLORS['RED'], LED_COLOR_BEAT = COLORS['OFF'], LED_COLOR_BAR = COLORS['OFF'], condition = True):
        self.colorMaps=ColorMapList()
        self.colorMaps._addColorMap(LED_COLOR_DEFAULT, LED_COLOR_BEAT, LED_COLOR_BAR, condition)
        return self.colorMaps
        
    def _addColorMap(self, LED_COLOR_DEFAULT=COLORS['RED'],LED_COLOR_BEAT=COLORS['OFF'],LED_COLOR_BAR=COLORS['OFF'], condition = True):
        self.colorMaps._addColorMap(LED_COLOR_DEFAULT, LED_COLOR_BEAT, LED_COLOR_BAR, condition)
        return self
    
    def _getColorMap(self, index):
        return self.colorMaps[index]


class emptyPad(Pad):
    def __init__():
        super.init(LED_COLOR_DEFAULT = COLORS['OFF'])
    
class sysexPad(Pad):         
    def __init__(self, callback_fn = function_dummy, sysexFn='PLAY', LED_COLOR_DEFAULT = COLORS['RED'], LED_COLOR_BEAT = COLORS['OFF'], LED_COLOR_BAR = COLORS['OFF']):
        """A SYSEX Pad.
        Warning : no advantage over MIDI CC so use only if necessary

        Args:
            sysexFn: The sysex function to be activated
            LED_COLOR (int, optional): The Pad color. Use utility.dictionaries.COLORS to set it up. Defaults to COLORS['RED'].
            LED_BLINKONPLAY (bool, optional): Does the pad blink when FL is playing ?. Defaults to False.
            LED_BLINKCOLOR (int, optional): If it blinks, what color ? Use utility.dictionaries.COLORS to set it up. Defaults to COLORS['OFF'].
        """
        super().__init__(callback_fn=callback_fn, controlMode = ControlModes['SYSEX'], controlData1=SYSEX[sysexFn], LED_COLOR_DEFAULT = LED_COLOR_DEFAULT, LED_COLOR_BEAT = LED_COLOR_BEAT, LED_COLOR_BAR = LED_COLOR_BAR)


class Knob(MultipleControl):
    def __init__(self, callback_fn = function_dummy, controlMode=ControlModes['CC'][0], controlData1=0, name = 'KNOB'):
        """A Knob.

        Args:
            callback_fn (function, optional): The function the button should activate. Defaults to None.
            controlMode (int, optional): First MIDI argument of sent message. Use utility.dictionnaries.ControlModes to map them easily. Defaults to ControlModes['CC'][1].
            dataOut (int, optional): Second MIDI argument of sent message. Usually between 0 and 127. Defaults to 0.
        """
        super().__init__(callback_fn, controlMode, controlData1, name)

class KnobShift(MultipleControl):
    def __init__(self, callback_fn = function_dummy, controlMode=ControlModes['CC'][0], controlData1=0, name = 'SHIFT + KNOB'):
        """A Shift Knob.

        Args:
            callback_fn (function, optional): The function the button should activate. Defaults to None.
            controlMode (int, optional): First MIDI argument of sent message. Use utility.dictionnaries.ControlModes to map them easily. Defaults to ControlModes['CC'][1].
            dataOut (int, optional): Second MIDI argument of sent message. Usually between 0 and 127. Defaults to 0.
        """
        super().__init__(callback_fn, controlMode, controlData1, name)
    
class KnobPress(MultipleControl):
    def __init__(self, callback_fn = function_dummy, controlMode=ControlModes['CC'][0], controlData1=0, name = 'PRESS KNOB'):
        """A Shift Knob.

        Args:
            callback_fn (function, optional): The function the button should activate. Defaults to None.
            controlMode (int, optional): First MIDI argument of sent message. Use utility.dictionnaries.ControlModes to map them easily. Defaults to ControlModes['CC'][1].
            dataOut (int, optional): Second MIDI argument of sent message. Usually between 0 and 127. Defaults to 0.
        """
        super().__init__(callback_fn, controlMode, controlData1, name)

class ModWheel(Control):
    def __init__(self, callback_fn = function_dummy, channel=1):
        """The Modulation Wheel.

        Args:
            callback_fn (function, optional): The function the button should activate. Defaults to None.
            controlMode (int, optional): First MIDI argument of sent message. Use utility.dictionnaries.ControlModes to map them easily. Defaults to ControlModes['CC'][1].
            dataOut (int, optional): Second MIDI argument of sent message. Usually between 0 and 127. Defaults to 0.
        """
        super().__init__(callback_fn, ControlModes['CC'][channel-1], RESERVED_CC['MOD_WHEEL'], name = 'MOD_WHEEL')

class PitchBend(Control):    
    def __init__(self, callback_fn = function_dummy, channel=1):
        """The Pitch Bend.

        Args:
            callback_fn (function, optional): The function the button should activate. Defaults to None.
            channel (int, optional): The channel to set it to.
        """
        super().__init__(callback_fn, ControlModes['PITCHBEND'][channel-1], name = 'PITCH_BEND')
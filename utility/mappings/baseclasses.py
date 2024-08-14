"""
    This file contains base classes of conntrols: Control and multipleControl
    Controls are linked to a callback function and a MIDI control Mode and argument they send.
    Multiple Controls allows to initialize a series of same-type controls and automatically numbers them
"""

from utility.midiutils import changeStatusChannel, statusToChannel
from utility.mappings.dictionaries import ControlModes, COLORS
from utility.toolbox import function_dummy

class Control:
    """
        A Control represents a physical button. It has a name, an FL callback function, a MIDI control mode and sends MIDI data.
    """
    def __init__(self, callback_fn = function_dummy, controlMode = ControlModes['OFF'], controlData1 = None, name = 'UNIDENTIFIED_CONTROL'):
        """A physical button

        Args:
            name (str, optional): Control name. Defaults to 'UNIDENTIFIED_CONTROL'.
            callback_fn (function, optional): The function the button should activate. Defaults to None.
            controlMode (int, optional): First MIDI argument of sent message. Use utility.dictionnaries.ControlModes to map them easily. Defaults to ControlModes['CC'][1].
            data (int, optional): Second MIDI argument of sent message. Usually between 0 and 127. Defaults to 0.
        """
        self._setName(name)
        self._setFn(callback_fn)
        self.setControlMode(controlMode)
        self._setControlData(controlData1)
        
    def _setName(self, name):
        self.name = name
        
    def _setFn(self, callback_Fn):
        self.callback_fn = callback_Fn
        
    def _setControlData(self, controlData1):
        self.controlData1 = controlData1
        
    def setControlMode(self, controlMode):
        self.controlMode = controlMode
    
    def setChannel(self, channel):
        self.controlMode = changeStatusChannel(self.controlMode, channel)
    
    def getChannel(self):
        return statusToChannel(self.controlMode)
    
class MultipleControl(Control):
    """
        One Control in a series of similar ones. It is a control with a number that can be set via self.setNumber(int)
        
    """
    # If the control Mode is in CC range and controlData1 is AUTOCC_KEY, the mapping will auto-attribute a CC number.
    AUTOCC_KEY = 0
    
    # First non-reserved CC channel
    AUTOCC_FIRST = 2
    
    # number of controls set by auto CC
    AUTOCCD = 0
    
    # Same "master" types in a row
    INAROW = 0
    
    #
    ISSAMETYPE = False
    
    def __init__(self, callback_fn = function_dummy, controlMode = ControlModes['CC'][1], controlData1 = AUTOCC_KEY, name = 'UNIDENTIFIED_MULTIPLE_CONTROL'):
        """One Control in a series of similar ones.
    
       Args:
            name (str, optional): Control name. Defaults to 'UNIDENTIFIED_MULTIPLE_CONTROL'.
            callback_fn (function, optional): The function the button should activate. Defaults to None.
            controlMode (int, optional): First MIDI argument of sent message. Use utility.dictionnaries.ControlModes to map them easily. Defaults to ControlModes['CC'][1].
            data (int, optional): Second MIDI argument of sent message. Usually between 0 and 127. Defaults to 0.
        """
        super().__init__(callback_fn, controlMode, controlData1, name)
        self._setNumber(1)
        
    def _setNumber(self, num):
        self.number = num
    
    def _autoSetNumber(self, number_mapping=[]):
        if MultipleControl.ISSAMETYPE:
            MultipleControl.INAROW +=1
        else:
            MultipleControl.INAROW = 1
        if number_mapping:
            self._setNumber(number_mapping[MultipleControl.INAROW-1])
        else:
            self._setNumber(MultipleControl.INAROW)
    
    def _setDefaultName(self):
        self._setName(self.name+str(self.number))
    
    def _initControl(self, channel, number_mapping=[]):
        self._autoSetNumber(number_mapping)
        self._setDefaultName()
        self.setChannel(channel)
        self._autoSetCCNumber()
    
    def _autoSetCCNumber(self):
        if self.controlMode in ControlModes['CC'] and self.controlData1==self.AUTOCC_KEY:
            MultipleControl.AUTOCCD+=1
            self.controlData1 = self.AUTOCC_FIRST + MultipleControl.AUTOCCD

class ColorMapList:
    def __init__(self):
        # The active colorMap
        self._activeColorMap = 0
        # The list containing colorMaps
        self._colorMaps=[]
        
        self._isChanged= bool
        self._conditions=[]
    
    def setActivity(self, activeControl):
        self._activeColorMap = activeControl
            
        
    def _addColorMap(self, LED_COLOR_DEFAULT=COLORS['RED'], LED_COLOR_BEAT=COLORS['OFF'], LED_COLOR_BAR=COLORS['OFF'], condition=True):
        self._colorMaps.append([LED_COLOR_DEFAULT, LED_COLOR_BEAT, LED_COLOR_BAR])
        self._conditions.append(condition)
        self._updateActivity()
        
    def getColorMapNumber(self): return len(self._colorMaps)
    def _updateActivity(self):
        i=1
        # This way first buttons have priority, but we ignore the first (default)
        for cond in reversed(self._conditions):
            if cond:
                self.setActivity(i)
                return
            i+=1
        # Defaults to first ColorMap
        self.setActivity(0)
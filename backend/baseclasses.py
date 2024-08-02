"""
    This file contains base classes of conntrols: Control and multipleControl
    Controls are linked to a callback function and a MIDI control Mode and argument they send.
    Multiple Controls allows to initialize a series of same-type controls and automatically numbers them
"""

from utility.midiutils import changeStatusChannel, statusToChannel
from backend.dictionaries import ControlModes

class Control:
    """
        A Control represents a physical button. It has a name, an FL callback function, a MIDI control mode and sends MIDI data.
    """
    def __init__(self, name = 'UNIDENTIFIED_CONTROL', callback_fn = None, controlMode = ControlModes['CC'][1], data = 0):
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
        self._setControlData(data)
        
    def _setName(self, name):
        self.name = name
        
    def _setFn(self, callback_Fn):
        self.callback_fn = callback_Fn
        
    def _setControlData(self, dataIn):
        self.control_data = dataIn
        
    def setControlMode(self, controlMode):
        self.controlMode = controlMode
    
    def changeChannel(self, channel):
        self.controlMode = changeStatusChannel(self.controlMode, channel)
    
    def getChannel(self):
        return statusToChannel(self.controlMode)
    
class multipleControl(Control):
    """
        One Control in a series of similar ones. It is a control with a number that can be set via self.setNumber(int)
        
    """
    def __init__(self, name = 'UNIDENTIFIED_MULTIPLE_CONTROL', callback_fn = None, controlMode = ControlModes['CC'][1], dataIn = 0):
        """One Control in a series of similar ones.
    
       Args:
            name (str, optional): Control name. Defaults to 'UNIDENTIFIED_MULTIPLE_CONTROL'.
            callback_fn (function, optional): The function the button should activate. Defaults to None.
            controlMode (int, optional): First MIDI argument of sent message. Use utility.dictionnaries.ControlModes to map them easily. Defaults to ControlModes['CC'][1].
            data (int, optional): Second MIDI argument of sent message. Usually between 0 and 127. Defaults to 0.
        """
        super().__init__(name, callback_fn, controlMode, dataIn)
        self.setNumber(0)
        
    def setNumber(self, num):
        self.number = num
    
    def setDefaultName(self):
        self._setName(self.name+str(self.number))
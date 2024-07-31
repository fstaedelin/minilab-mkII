from utility.midiutils import changeStatusChannel, statusToChannel
from mapping.dictionaries import ControlModes

class Control:
    name='UNIDENTIFIED_CONTROL'
    callback_fn = None
    controlMode = ControlModes['CC'][0]
    control_data = 0
    
    def __init__(self, name = 'UNIDENTIFIED_CONTROL', callback_fn = None, controlMode = ControlModes['CC'][1], data = 0):
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
    number = 0
    def __init__(self, name = 'UNIDENTIFIED_MULTIPLE_CONTROL', callback_fn = None, controlMode = ControlModes['CC'][1], dataIn = 0):
        super().__init__(name, callback_fn, controlMode, dataIn)
        
    def setNumber(self, num):
        self.number = num
    
    def setDefaultName(self):
        self._setName(self.name+str(self.number))
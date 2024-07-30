from utility.midistati import *
from utility.cccodes import *
from utility.flcommands import *
from utility.lightcommands import *
from utility.colors import COLORS

NUMBER_OF_PADS = 16
NUMBER_OF_KNOBS = 20 # Incudes shift+knobs 1/9 and press knobs 1/9

ControlModes = {
    'SYSEX' : MIDI_STATUS_SYSEX,
    'CC' : MIDI_STATUS_CONTROL_CHANGE,
    'PC' : MIDI_STATUS_PROGRAM_CHANGE,
    'PITCHBEND' : MIDI_STATUS_PITCH_BEND,
    'NOTE_ON' : MIDI_STATUS_NOTE_ON,
    'NOTE_OFF' : MIDI_STATUS_NOTE_OFF,
    'PAD_AFTERTOUCH' : MIDI_STATUS_POLYPHONIC_AFTERTOUCH,
    'AFTERTOUCH2' : MIDI_STATUS_AFTERTOUCH 
}

class Control:
    name='UNIDENTIFIED_CONTROL'
    callback_fn = normal_dummy
    controlMode = ControlModes['CC'][0]
    
    def __init__(self, name = 'UNIDENTIFIED_CONTROL', callback_fn = normal_dummy, controlMode = ControlModes['CC'][1]):
        self._setName(name)
        self._setFn(callback_fn)
        self.setControlMode(controlMode)        
        
    def _setName(self, name):
        self.name = name
        
    def _setFn(self, callback_Fn):
        self.callback_fn = callback_Fn
        
    def _setData(self, dataIn):
        self.data = dataIn
        
    def setControlMode(self, controlMode):
        self.controlMode = controlMode
    
    def changeChannel(self, channel):
        changeChannel(self.controlMode, channel)
    
    def getChannel(self):
        return statusToChannel(self.controlMode)
    
class multipleControl(Control):
    number = 0
    def __init__(self, name = 'UNIDENTIFIED_MULTIPLE_CONTROL', callback_fn = normal_dummy, controlMode = ControlModes['CC'][1]):
        super().__init__(name, callback_fn, controlMode)
        
    def setNumber(self, num):
        self.number = num
    
    def setDefaultName(self):           
        self._setName(self.name+str(self.number))
    
    
class Pad(multipleControl):
    number = 0 # Pad 0 if it is off ?
    DATA_CODE = 0
    ID_PAD = 0x00
    LED_COLOR = COLORS['RED']
    LED_BLINKONPLAY = False
    
    def __init__(self, callback_fn=normal_dummy, controlMode=ControlModes['CC'][1], DATA_CODE=0, LED_COLOR = COLORS['RED'], LED_BLINKONPLAY = False):
        super().__init__('PAD', callback_fn, controlMode)
        self.DATA_CODE = DATA_CODE
        self.LED_COLOR = LED_COLOR
        self.LED_BLINKONPLAY = LED_BLINKONPLAY
        self.SetID()
    
    def SetID(self):
        self.ID_PAD = ID_PADS[self.number]

class Knob(multipleControl):
    DATA_CODE = 0
    
    def __init__(self, callback_fn=normal_dummy, controlMode=ControlModes['CC'][1], DATA_CODE=0):
        super().__init__('KNOB', callback_fn,controlMode)
        self.DATA_CODE = DATA_CODE
    
    def setNumber(self, num):
        self.number = num
        

class Mapping:
    knobs = [Knob]
    pads = [Pad]    
    
    ## the same for all modes, shouldn't be changed
    keyboard_channel = 1
    control_channel = 2
    
    def __init__(self, knobList: "list[Knob]", padList: "list[Pad]"):
        i=0
        for pad in padList:
            i+=1
            pad.setNumber(i)
            pad.SetID()
            pad.setDefaultName()
            self.pads.append(pad)
            
        if i < NUMBER_OF_PADS:
            print("Unmapped pads !")
        
        i=0
        for knob in knobList:
           i+=1
           knob.setNumber(i)
           knob.setDefaultName()
           self.knobs.append(knob)
        
        if i < NUMBER_OF_KNOBS:
            print(NUMBER_OF_KNOBS-i, " unmapped knobs !")
            
    def __init__(self, control_chn, knobList: "list[Knob]", padList: "list[Pad]"):
        self.__init__(knobList, padList)
        self._setControlChannel(control_chn)
        self._updateControlChannels()
        
    def _setControlChannel(self, chn):
        self.control_channel = chn
        
    def _updateControlChannels(self):
        for controller in self.pads + self.knobs:
            if controller.controlMode in ControlModes['CC']+ControlModes['PAD_AFTERTOUCH']:
                controller.changeChannel(self.control_channel)
            
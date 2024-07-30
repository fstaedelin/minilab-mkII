from utility.midistati import *
from utility.cccodes import *
from utility.flcommands import *
from utility.lightcommands import *
from utility.colors import COLORS

NUMBER_OF_PADS = 16
NUMBER_OF_KNOBS = 20 # Incudes shift+knobs 1/9 and press knobs 1/9

class Control:
    name='UNIDENTIFIED_CONTROL'
    callback_fn = normal_dummy
    MIDI_STATUS = MIDI_STATUS_CONTROL_CHANGE_CHAN1
    
    def __init__(self, name = 'UNIDENTIFIED_CONTROL', callback_fn = normal_dummy, MIDI_STATUS = MIDI_STATUS_CONTROL_CHANGE_CHAN1):
        self._setName(name)
        self._setFn(callback_fn)
        self._setMidiStatus(MIDI_STATUS)
        
        
    def _setName(self, name):
        self.name = name
        
    def _setFn(self, callback_Fn):
        self.callback_fn = callback_Fn
        
    def _setMidiStatus(self, MIDI_STATUS):
        self.MIDI_STATUS = MIDI_STATUS
    
class multipleControl(Control):
    number = 0
    def __init__(self, name = 'UNIDENTIFIED_MULTIPLE_CONTROL', callback_fn = normal_dummy, MIDI_STATUS = MIDI_STATUS_CONTROL_CHANGE_CHAN1, number = 0):
        super().__init__(name, callback_fn, MIDI_STATUS)
        
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
    
    def __init__(self, callback_fn=normal_dummy, MIDI_STATUS=MIDI_STATUS_CONTROL_CHANGE_CHAN1, DATA_CODE=0, LED_COLOR = COLORS['RED'], LED_BLINKONPLAY = False):
        super().__init__('PAD', callback_fn, MIDI_STATUS, 0)
        self.DATA_CODE = DATA_CODE
        self.LED_COLOR = LED_COLOR
        self.LED_BLINKONPLAY = LED_BLINKONPLAY
        self.SetID()
    
    def SetID(self):
        self.ID_PAD = ID_PADS[self.number]
        
        
    
    

class Knob(multipleControl):
    DATA_CODE = 0
    
    def __init__(self, callback_fn=normal_dummy, MIDI_STATUS=MIDI_STATUS_CONTROL_CHANGE_CHAN1, DATA_CODE=0):
        super().__init__('KNOB', callback_fn,MIDI_STATUS, 0)
        self.DATA_CODE = DATA_CODE
    
    def setNumber(self, num):
        self.number = num
        

class Mapping:
    pads = [Pad]
    knobs = [Knob]
    
    def __init__(self, padList: "list[Pad]", knobList: "list[Knob]"):
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
            print("Unmapped knobs !")
            

from backend.maincontrollertypes import *

class MiniLabMk2Mapping:
    
    NUMBER_OF_PADS = 16
    NUMBER_OF_KNOBS = 20 # Incudes shift+knobs 1/9 and press knobs 1/9
    
    ## The same for all mappings, shouldn't be changed
    # carries keyboard info + mod wheel + pitch bend
    keyboard_channel = 1
    mod_wheel = ModWheel(keyboard_channel)
    pitch_bend = PitchBend(keyboard_channel)
    
    # This one is variable, each mapping should have its own
    control_channel = 2
    knobs = []
    pads = []
            
    def __init__(self, control_chn, knobList: "list[Knob]", padList: "list[Pad]"):
        i=0
        for pad in padList:
            i+=1
            pad.setNumber(i)
            pad.SetID()
            if pad.number > self.NUMBER_OF_PADS:
                if pad.number in [18, 20]:
                    pad._setName(self.name+'+SHIFT')
                elif pad.number in [19, 21]:
                    pad._setName(self.name+'SWITCH')
            else:
                pad.setDefaultName()
            self.pads.append(pad)
            
        if i < self.NUMBER_OF_PADS:
            print(self.NUMBER_OF_PADS-i, " unmapped pads !")
        
        i=0
        for knob in knobList:
           i+=1
           knob.setNumber(i)
           knob.setDefaultName()
           self.knobs.append(knob)
        
        if i < self.NUMBER_OF_KNOBS:
            print(self.NUMBER_OF_KNOBS-i, " unmapped knobs !")
            
        self._setControlChannel(control_chn)            
        self._updateControlChannels()
        
    def _setControlChannel(self, chn):
        self.control_channel = chn
        
    def _updateControlChannels(self):
        for controller in self.knobs + self.pads :
            if controller.controlMode in list(ControlModes['CC'])+list(ControlModes['PAD_AFTERTOUCH']):
                chn = self.control_channel
                #print(controller.name)
                #print(chn)
                controller.changeChannel(chn)

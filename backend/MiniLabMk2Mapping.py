"""
    This file contains MiniLabMk2Mapping class definition
"""

from backend.maincontrollertypes import *
from midi import REC_TrackRange
from utility.toolbox import checkHandled

class MiniLabMapping:
    
    NUMBER_OF_PADS = 16
    NUMBER_OF_KNOBS = 20 # Incudes shift+knobs 1/9 and press knobs 1/9
    
    ## The same for all mappings, shouldn't be changed
    # carries keyboard info + mod wheel + pitch bend
    
    
    
    # This one is variable, each mapping should have its own ?
    control_channel = 2
    knobs = []
    pads = []
            
    def __init__(self, control_chn, knobList: "list[Knob]", padList: "list[Pad]"):
        """A mapping of controls corresponding to MiniLab mkII

        Args:
            control_chn (int): The MIDI channel this mapping needs to control. Needs to be in 1, 16 and match the MIDI Control Center number.
            knobList (list[Knob]): a list of 20 Knobs
            padList (list[Pad]): a list of 16 Pads
        Raises:
            ValueError: If the channel is not in [[ 1, 16  ]]
        """
        self.keyboard_channel = 1
        self.mod_wheel = ModWheel(self.ProcessModWheelEvent, self.keyboard_channel)
        self.pitch_bend = PitchBend(self.ProcessPitchBendEvent, self.keyboard_channel)
        i=0
        
        # Sets up the pad numbers, IDs and names
        for pad in padList:
            i+=1
            pad.setNumber(i)
            pad.SetID()
            pad.setDefaultName()
            self.pads.append(pad)
            
        # checks if there are unmapped pads
        if i < self.NUMBER_OF_PADS:
            print(self.NUMBER_OF_PADS-i, " unmapped pads !")
        
        i=0
        # Sets up the numbers and names
        for knob in knobList:
            i+=1
            knob.setNumber(i)
            knob.setDefaultName()
            if knob.number > self.NUMBER_OF_PADS:
                if knob.number == 17:
                    knob._setName('KNOB1+SHIFT')
                elif knob.number == 19:
                    knob._setName('KNOB9+SHIFT')
                elif knob.number ==18:
                    knob._setName('KNOB1 SWITCH')
                elif knob.number == 20:
                    knob._setName('KNOB9 SWITCH')
            
            self.knobs.append(knob)
        
        # checks if there are unmapped knobs
        if i < self.NUMBER_OF_KNOBS:
            print(self.NUMBER_OF_KNOBS-i, " unmapped knobs !")
        
        if control_chn in range(1, REC_TrackRange+1):
            self._setControlChannel(control_chn) 
            self._updateControlChannels()           
        else:
            ValueError("Channel number must be in [[ 1, 16 ]]")
        
    def _setControlChannel(self, chn):
        """change the MIDI control channel

        Args:
            chn (int): new midi channel. Must be in [[ 1, 16 ]]
        """
        self.control_channel = chn
        
    def _updateControlChannels(self):
        """Updates all the controls' channels via their commanded MIDI status. Might need to change to include midi notes for pads.
        """
        for controller in self.knobs + self.pads :
            if controller.controlMode in list(ControlModes['CC'])+list(ControlModes['PAD_AFTERTOUCH']):
                chn = self.control_channel
                #print(controller.name)
                #print(chn)
                controller.changeChannel(chn)
                
    def ProcessModWheelEvent(self, event):
        print('####### Processing ModWheelEvent #######')
        # what to do ?
        print('TODO')
        return event.handled
        
    def ProcessPitchBendEvent(self, event):
        print('####### Processing PitchBendlEvent #######')
        # what to do ?
        print('TODO')
        event.handled = True
        checkHandled(event)
        return event.handled

"""
    This file contains MiniLabMk2Mapping class definition
"""

from utility.mappings.maincontrollertypes import *
from utility.midiutils import MIDI_N_CHANNELS

class MiniLabMapping:
    
    NUMBER_OF_PADS = 16
    NUMBER_OF_KNOBS = 16 # Incudes shift+knobs 1/9 and press knobs 1/9
    
    INDEX_PRESSSHIFT_KNOBS = [1, 9]
    NUMBER_OF_PRESSABLE_KNOBS = len(INDEX_PRESSSHIFT_KNOBS)
    NUMBER_OF_SHIFTABLE_KNOBS = len(INDEX_PRESSSHIFT_KNOBS)
    
    ## The same for all mappings, shouldn't be changed
    KEYBOARD_CHANNEL = 1
    
    # This one is variable, each mapping should have its own ?
            
    def __init__(self, control_chn, knobList: "list[Knob]", shiftKnobList: "list[KnobShift]", pressKnobList: "list[KnobPress]", padList: "list[Pad]"):
        """A mapping of controls corresponding to MiniLab mkII

        Args:
            control_chn (int): The MIDI channel this mapping needs to control. Needs to be in 1, 16 and match the MIDI Control Center number.
            knobList (list[Knob]): a list of 20 Knobs
            padList (list[Pad]): a list of 16 Pads
        Raises:
            ValueError: If the channel is not in [[ 1, 16  ]]
        """
        
        ## 1 mapping -> 1 channel
        self._checkInitParams(control_chn, knobList, shiftKnobList, pressKnobList, padList)
        
        self.control_channel = control_chn
        
        self.knobs: "list[Knob]" = self._setMultipleControls(knobList)
        self.shiftKnobs: "list[KnobShift]" = self._setMultipleControls(shiftKnobList, self.INDEX_PRESSSHIFT_KNOBS)
        self.pressKnobs: "list[KnobPress]" = self._setMultipleControls(pressKnobList, self.INDEX_PRESSSHIFT_KNOBS)
        self.pads: "list[Pad]" = self._setMultipleControls(padList)
        
        self.mod_wheel = ModWheel(self.ProcessModWheelEvent, MiniLabMapping.KEYBOARD_CHANNEL)
        self.pitch_bend = PitchBend(self.ProcessPitchBendEvent, MiniLabMapping.KEYBOARD_CHANNEL)
        
        self._checkIfComplete()
    
    def _controls(self):
        return self.knobs + self.shiftKnobs + self.pressKnobs + self.pads + self.mod_wheel + self.pitch_bend
    
    def _multiControls(self):
        return self.knobs + self.shiftKnobs + self.pressKnobs + self.pads
    
    #### Helpers to set up the mapping's multiple controls
    def _setMultipleControls(self, controlList: "list[MultipleControl]", number_mapping = []):
        MultipleControl.ISSAMETYPE = False
        for multiControl in controlList:
            multiControl._initControl(self.control_channel, number_mapping)
            MultipleControl.ISSAMETYPE = True
        
        return controlList            
    
    ##### Define mapping ModWheel similar for all mappings ? #####
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
        #checkHandled(event)
        return event.handled
    
    ##### CHANNEL MANAGEMENT HELPERS #####
    def _setControlChannel(self, chn):
        """change the MIDI control channel

        Args:
            chn (int): new midi channel. Must be in [[ 1, 16 ]]
        """
        self.control_channel = chn
        
    def _updateControlChannels(self):
        """Updates all the controls' channels via their commanded MIDI status. Might need to change to include midi notes for pads.
        """
        for controller in self._controls :
            if controller.controlMode in list(ControlModes['CC'])+list(ControlModes['PAD_AFTERTOUCH']):
                chn = self.control_channel
                #print(controller.name)
                #print(chn)
                controller.changeChannel(chn)
                
    ##### INIT HELPERS ########
    def _checkInitParams(self, control_chn, knobList: "list[Knob]", shiftKnobList: "list[KnobShift]", pressKnobList: "list[KnobPress]", padList: "list[Pad]"):
        if control_chn not in range(1, MIDI_N_CHANNELS+1):
            raise ValueError("Channel number must be in [[ 1, 16 ]]")
        elif control_chn == self.KEYBOARD_CHANNEL:
            print("Control channel set to keyboard channel")
        
        if len(knobList) > MiniLabMapping.NUMBER_OF_KNOBS:
            ValueError("Too many Knobs for Arturia MiniLab mkII !")
        
                
    def _checkIfComplete(self):
        # checks if there are unmapped pads
        if len(self.knobs) < self.NUMBER_OF_KNOBS:
             print(self.NUMBER_OF_PADS-len(self.knobs), " unmapped knobs !")
        if len(self.pads) < self.NUMBER_OF_PADS:
             print(self.NUMBER_OF_PADS-len(self.pads), " unmapped pads !")
        if len(self.shiftKnobs) < self.NUMBER_OF_SHIFTABLE_KNOBS:
             print(self.NUMBER_OF_PADS-len(self.shiftKnobs), " unmapped shiftKnobs !")
        if len(self.pressKnobs) < self.NUMBER_OF_PRESSABLE_KNOBS:
             print(self.NUMBER_OF_PADS-len(self.pressKnobs), " unmapped pressKnobs !")
            

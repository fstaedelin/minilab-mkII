import channels
import mixer
import patterns
import playlist
import transport
import ui
import device
#import plugins
import midi
#import MiniLabmk2Plugin
#import FelixTemplate as template

import general

from MiniLabDispatch import MidiEventDispatcher

from utility.flcommands import *
from utility.toolbox import checkHandled, printCommandChannel

from mapping.dictionaries import SYSEX, ControlModes

from mapping.example import exampleMapping


#import ArturiaVCOL


# This class processes all CC coming from the controller
# The class creates new handler for each function
# The class calls the right fonction depending on the incoming CC

class MiniLabMidiProcessor:
    @staticmethod
    def _is_pressed(event):
        return event.controlVal != 0

    def __init__(self, controller):
        def by_data1(event) : return event.data1
        def by_data2(event) : return event.data2
        def by_status(event) : return event.status
        def by_sysex(event) : return event.sysex
        def ignore_release(event): return self._is_pressed(event)
        def ignore_press(event): return not self._is_pressed(event)

        self._controller = controller
        
    # DISPATCHERS            
        ## SysEx dispatcher
        self._sysex_dispatcher = (
            MidiEventDispatcher(by_sysex)
            .NewHandler(SYSEX['STOP'], sysex_stop)
            .NewHandler(SYSEX['PLAY'], sysex_start)
            .NewHandler(SYSEX['DEFERRED_PLAY'], sysex_dummy)
            .NewHandler(SYSEX['FAST_FORWARD'], sysex_fastforward)
            .NewHandler(SYSEX['REWIND'], sysex_rewind)
            .NewHandler(SYSEX['REC_STROBE'], sysex_rec_strobe)
            .NewHandler(SYSEX['REC_EXIT'], sysex_dummy)
            .NewHandler(SYSEX['REC_READY'], sysex_dummy)
            .NewHandler(SYSEX['PAUSE'], sysex_dummy)
            .NewHandler(SYSEX['EJECT'], sysex_dummy)
            .NewHandler(SYSEX['CHASE'], sysex_dummy)
            .NewHandler(SYSEX['INLIST_RESET'], sysex_dummy)
        )
        
        ## Control change dispatcher. Supports:
            # Modulation Wheel (reserved CC)
        self._CC_dispatcher = (
            MidiEventDispatcher(by_data1)
            .NewHandler(exampleMapping.mod_wheel.control_data, self.ProcessModWheelEvent)
            .NewCCHandlersFromMapping(exampleMapping)
            
        )
        
        ## Master dispatcher
        # Sends to proper dispatcher depending on received MIDI key (event.status). Supports:
            # Pitch bends on 16 channels
            # call to CC generic dispatcher
            
        self._status_dispatcher = (
            MidiEventDispatcher(by_status)
            # No need to redirect those because they are caught before
            #.NewHandler(MIDI_STATUS_SYSEX, self.ProcessSysExEvent)
            # Pitch bends can be assigned to processPitchBend at once
            .NewHandler(exampleMapping.pitch_bend.controlMode, self.ProcessPitchBendEvent)
            .NewHandlerForKeys(ControlModes['CC'], self.ProcessCommandEvent)
        )

    
    # PROCESSORS
    # Master processor
    def ProcessEvent(self, event) :
        print('#######  ... Processing ... #######')
        return self._status_dispatcher.Dispatch(event)
    
    # Sysex processor
    def ProcessSysExEvent(self, event):
        print('####### Processing SysExEvent #######')
        print('event status: ', event.status)
        print('event sysex: ', event.sysex)
        event.handled = self._sysex_dispatcher.Dispatch(event)
        checkHandled(event)
        return event.handled

    def ProcessCommandEvent(self, event):
        print('####### Processing CommandEvent #######')
        event.handled = self._CC_dispatcher.Dispatch(event)
        if event.handled == False:
            print('/!\/!\/!\/!\/!\ CC not set ! /!\/!\/!\/!\/!')
            printCommandChannel(event)
        return event.handled
    
    def ProcessModWheelEvent(self, event):
        print('####### Processing ModWheelEvent #######')
        # what to do ?
        print('TODO')
        event.handled = True
        checkHandled(event)
        return event.handled
        
    def ProcessPitchBendEvent(self, event):
        print('####### Processing PitchBendlEvent #######')
        # what to do ?
        print('TODO')
        event.handled = True
        checkHandled(event)
        return event.handled
    

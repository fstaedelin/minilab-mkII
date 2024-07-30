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
from utility.sysexcodes import *

from utility.midistati import MIDI_CHANNEL_INDEX
from utility.midistati import MIDI_STATUS_SYSEX
from utility.midistati import MIDI_STATUS_CONTROL_CHANGE
from utility.midistati import MIDI_STATUS_PITCH_BEND

from utility.cccodes import *

from utility.toolbox import *

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
            .NewHandler(SYSEX_STOP, sysex_stop)
            .NewHandler(SYSEX_PLAY, sysex_start)
            .NewHandler(SYSEX_DEFERRED_PLAY, sysex_dummy)
            .NewHandler(SYSEX_FAST_FORWARD, sysex_fastforward)
            .NewHandler(SYSEX_REWIND, sysex_rewind)
            .NewHandler(SYSEX_REC_STROBE, sysex_rec_strobe)
            .NewHandler(SYSEX_REC_EXIT, sysex_dummy)
            .NewHandler(SYSEX_REC_READY, sysex_dummy)
            .NewHandler(SYSEX_PAUSE, sysex_dummy)
            .NewHandler(SYSEX_EJECT, sysex_dummy)
            .NewHandler(SYSEX_CHASE, sysex_dummy)
            .NewHandler(SYSEX_INLIST_RESET, sysex_dummy)
        )
        
        ## Control change dispatcher
        self._CC_dispatcher = (
            MidiEventDispatcher(by_data1)
            .NewHandler(CC_MODULATION_WHEEL, self.ProcessModWheelEvent)
            
        )
        
        ## Master dispatcher
        self._status_dispatcher = (
            MidiEventDispatcher(by_status)
            #.NewHandler(MIDI_STATUS_SYSEX, self.ProcessSysExEvent)
            # Pitch bends can be assigned to processPitchBend at once
            .NewHandlerForKeys(MIDI_STATUS_PITCH_BEND, self.ProcessPitchBendEvent)
            .NewHandler(MIDI_STATUS_CONTROL_CHANGE[MIDI_CHANNEL_INDEX], self.ProcessCommandEvent)
        )

    # DISPATCH
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
    
    def ProcessEvent(self, event) :
        print('#######  ... Processing ... #######')
        #if event.status in [153,137] :
        #    return self.OnDrumEvent(event)
        #else :

        #print(event.status,"\t",event.data1,"\t",event.controlNum,"\t",event.data2,"\t",event.midiId)
        return self._status_dispatcher.Dispatch(event)

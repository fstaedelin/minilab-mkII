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
from utility.toolbox import printCommandChannel, Tagable, Debug, ProcessorWarning

from backend.dictionaries import SYSEX, ControlModes

from backend.MiniLabMk2Mapping import MiniLabMapping

#import ArturiaVCOL


# This class processes all CC coming from the controller
# The class creates new handler for each function
# The class calls the right fonction depending on the incoming CC

class MidiProcessor:
    @staticmethod
    def _is_pressed(event):
        return event.controlVal != 0

    def __init__(self, map: MiniLabMapping):
        def by_data1(event) : return event.data1
        def by_data2(event) : return event.data2
        def by_status(event) : return event.status
        def by_sysex(event) : return event.sysex
        def ignore_release(event): return self._is_pressed(event)
        def ignore_press(event): return not self._is_pressed(event)

        #self.mapping.mod_wheel._setFn(self.ProcessModWheelEvent)
        self.natively_handled = [ControlModes['NOTE_OFF']]+[ControlModes['NOTE_ON']]+[ControlModes['PAD_AFTERTOUCH']]
        
    # DISPATCHERS            
        ## SysEx dispatcher
        self._sysex_dispatcher = (
            MidiEventDispatcher(by_sysex)
            .NewSYSEXHandlersFromMapping(map)
        )
        
        ## Control change dispatcher. Supports:
            # Modulation Wheel (reserved CC)
        self._CC_dispatcher = (
            MidiEventDispatcher(by_data1)
            ## handles knobs, pads and the modulation wheel
            .NewCCHandlersFromMapping(map)
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
            .NewHandler(map.pitch_bend.controlMode, map.ProcessPitchBendEvent)
            .NewHandlerForKeys(ControlModes['CC'], self.ProcessCommandEvent)
        )

    
    # PROCESSORS
    # Master processor
    def ProcessEvent(self, event) :
        processDebug = Debug(title = 'Processing')
        if event.status not in self.natively_handled:
            Debug("Event not natively handled, Dispatching by status", callback_fn= Tagable.printEvent(event))
            return self._status_dispatcher.Dispatch(event)
        else:
            Debug("Natively handled", callback_fn=Tagable.printEvent(event))
            return False
        processDebug._close()
        
    
    # Sysex processor
    def ProcessSysExEvent(self, event):
        if not event.sysex == None:
            Debug('Processing SysExEvent',
                ['event status: '+str(event.status),
                'event sysex: '+str(event.sysex),
                ])
            event.handled = self._sysex_dispatcher.Dispatch(event)
        return event.handled

    def ProcessCommandEvent(self, event):
        __PROCESSCOMMAND = Debug(title = "ProcessCommandEvent", key = self._CC_dispatcher.Dispatch(event))
        if event.handled == False:
            ProcessorWarning('CC not set !')
            printCommandChannel(event)
        return event.handled
    

    

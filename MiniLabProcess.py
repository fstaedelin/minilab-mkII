#import channels
#import mixer
#import patterns
#import playlist
#import transport
#import ui
#import device
##import plugins
#import midi
##import MiniLabmk2Plugin
##import FelixTemplate as template
#
#import general

from MiniLabDispatch import MidiEventDispatcher

from utility.midiutils import *
#from utility.toolbox import printCommandChannel

from utility.mappings.dictionaries import SYSEX, ControlModes
#, getControlMode

from utility.mappings.MiniLabMk2Mapping import MiniLabMapping

from utility.fl_commands.actions import Actions
#import ArturiaVCOL
from utility.JARVIS import _JARVIS
#, printCommandChannel

# This class processes all CC coming from the controller
# The class creates new handler for each function
# The class calls the right fonction depending on the incoming CC

class MidiProcessor:
    @staticmethod
    def _is_pressed(event):
        return event.controlVal != 0

    def __init__(self, map: MiniLabMapping):
        _JARVIS.Navigate("Processor Initialization")
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
            .NewCCHandlersFromMapping(map, ignore_release)
            .NewHandlerForKeys(ControlModes['CC'], self.ProcessCommandEvent)
            .NewHandlerForKeys(range(2, 17), self.OnPanKnobTurned)
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
        
        _JARVIS.Navigate("parent")

    
    # PROCESSORS
    # Master processor
    def ProcessEvent(self, event) :
        _JARVIS.Navigate("PROCESS_EVENT")
        if event.status not in self.natively_handled:
            _JARVIS.Debug("Event not natively handled, Dispatching by status")
            _JARVIS.Navigate("parent")
            return self._status_dispatcher.Dispatch(event)
        else:
            _JARVIS.Debug("Natively handled")
            _JARVIS.Navigate("parent")
            return False
        
    
    # Sysex processor
    def ProcessSysExEvent(self, event):
        _JARVIS.Navigate("SYSEX_EVENT")
        if not event.sysex is None:
            _JARVIS.Debug('Processing SysExEvent',
                ['event status: '+str(event.status),
                'event sysex: '+str(event.sysex),
                ])
            event.handled = self._sysex_dispatcher.Dispatch(event)
        _JARVIS.Navigate("parent")
        return event.handled

    def ProcessCommandEvent(self, event):
        _JARVIS.Navigate("COMMAND_EVENT")
        if event.handled == False:
            self._CC_dispatcher.Dispatch(event)
            _JARVIS.printCommandChannel(event)
        _JARVIS.Navigate("parent")
        return event.handled
    

    
    def _get_knob_delta(self, event):
        val = event.controlVal
        return val if val < 64 else 64 - val
    
    def OnPanKnobTurned(self, event):
        channelIndex = event.controlNum - 2
        Actions.OnUpdatePanning(channelIndex, self._get_knob_delta(event))

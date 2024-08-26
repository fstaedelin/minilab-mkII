#import channels
#import mixer
#import patterns
#import playlist
#import transport
import ui
#import device
import plugins
import midi
##import MiniLabmk2Plugin
##import FelixTemplate as template
#
#import general

import channels
import device

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


PORT_MIDICC_ANALOGLAB = 10

V_COL = ['Analog Lab V',
         'ARP 2600 V3',
         'B-3 V2',
         'Buchla Easel V',
         'Clavinet V',
         'CMI V',
         'CS-80 V3',
         'CZ V',
         'DX7 V',
         'Emulator II V',
         'Farfisa V',
         'Jun-6 V',
         'Jup-8 V4',
         'Matrix-12 V2',
         'Mellotron V',
         'Mini V3',
         'Modular V3',
         'OB-Xa V',
         'PatchWorks',
         'Piano V2',
         'Prophet V3',
         'SEM V2',
         'Solina V2',
         'SQ80 V',
         'Stage-73 V2',
         'Synclavier V',
         'Synthi V',
         'Synthopedia',
         'Vocoder V',
         'Vox Continental V2',
         'Wurli V2'
         ]

MY_CC_TO_ANALOGLAB = {
    1 : 0x01,
    2 : 0x70,
    20 : 0x71,
    10 : 0x72,
    21: 0x73,
    3 : 0x4A,
    4 : 0x47, 
    5: 0x4C, 
    6: 0x4D, 
    7: 0x5D, 
    8: 0x49, 
    9: 0x4B, 
    11: 0x12, 
    12: 0x13, 
    13: 0x10, 
    14: 0x11, 
    15: 0x5B, 
    16: 0x4F, 
    17: 0x48}

ANALOG_IDS = [ 0x01, 0x70, 0x71, 0x72, 0x73, 0x4A, 0x47, 0x4C, 0x4D, 0x5D, 0x49, 0x4B, 0x12, 0x13, 0x10, 0x11, 0x5B, 0x4F, 0x48]
class MidiProcessor:
    @staticmethod
    def _is_pressed(event):
        return event.controlVal != 0

    def __init__(self, map: MiniLabMapping):
        _JARVIS.Navigate("Processor Initialization")
        def by_data1(event) : return event.data1
        def by_control_num(event) : return event.controlNum
        def by_data2(event) : return event.data2
        def by_status(event) : return event.status
        def by_sysex(event) : return event.sysex
        def ignore_release(event): return self._is_pressed(event)
        def ignore_press(event): return not self._is_pressed(event)

        #self.mapping.mod_wheel._setFn(self.ProcessModWheelEvent)
        self.natively_handled = [ControlModes['NOTE_OFF']]+[ControlModes['NOTE_ON']]+[ControlModes['PAD_AFTERTOUCH']]
        self._analogMode = False
    # DISPATCHERS            
       
        ## Control change dispatcher. Supports:
            # Modulation Wheel (reserved CC)
        self._CC_dispatcher = (
            MidiEventDispatcher(by_data1)
            ## handles knobs, pads and the modulation wheel
            # Absolute knobs from 3 to 9 and 11 through 16
            .NewHandlerForKeys(range(3, 10), self.OnVolumeKnobTurned)
            .NewHandlerForKeys(range(11, 18), self.OnPanKnobTurned)
            
            # Relative Knobs for knobs 1 and 9, CC 2 and 10
            
            
            
            # shift knobs are CC 18/19
            
            
            
            # Pressable knobs are CC 20/21
            # Master elements
            .NewHandler(20, Actions.cycle_active_window)
            .NewHandler(21, Actions.noop)
            
            
            ## BASIC PLAY/PAUSE BUTTONS
            .NewHandler(22, Actions.playpause)
            .NewHandler(23, Actions.stop)
            .NewHandler(24, Actions.toggle_rec)
            .NewHandler(25, Actions.toggle_metronome)
            .NewHandler(26, Actions.toggle_loop_recording)
            .NewHandler(27, Actions.toggle_overdub)
            
            
            ## Channel rack up / down
            .NewHandler(28, self.activate_prev_channel)
            .NewHandler(29, self.activate_next_channel)
            
        )
        
        self.Arturia_dispatcher = (
            MidiEventDispatcher(by_control_num)
            .NewHandlerForKeys(range(2, 18), self.remapForArturia)
            .NewHandler(1, self.remapForArturia)
            .NewHandler(0, self.remapForArturia)
            .NewHandler(20, self.remapForArturia)
            .NewHandler(21, self.remapForArturia)
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
            .NewHandlerForKeys(ControlModes['CC'], self.ProcessCommandEvent)
            .NewHandlerForKeys(ControlModes['PITCHBEND'], self.ProcessCommandEvent)
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
            if self._analogMode and (event.data1 in MY_CC_TO_ANALOGLAB):
                _JARVIS.Warning("Analog Mode On")
                self.Arturia_dispatcher.Dispatch(event)
            elif self._analogMode and event.status in ControlModes["PITCHBEND"]:
                self.pitchBendForArturia(event)
            else:
                _JARVIS.Warning("Analog Mode Off")
                self._CC_dispatcher.Dispatch(event)
        
        
        #_JARVIS.printCommandChannel(event)
        _JARVIS.Navigate("parent")
        return event.handled
    

    
    def _get_knob_delta(self, event):
        val = event.controlVal
        return val
    
    def OnVolumeKnobTurned(self, event):
        channelIndex = event.controlNum - 3 # 2 is the start index for CC
        channels.setChannelVolume(channelIndex, event.data2/127)
        
    def OnPanKnobTurned(self, event):
        channelIndex = event.controlNum - 3 - 8 # I already assigned 8 knobs for volume
        channels.setChannelPan(channelIndex, (event.data2-63.5)/63.5)

    def ForwardAnalogLab(self, event) :
        _JARVIS.Warning("FORWARDANALOGLAB")
        device.forwardMIDICC(event.status + (event.data1 << 8) + (event.data2 << 16) + (PORT_MIDICC_ANALOGLAB << 24))
            
    def activateChannel(self):
        # TOGGLE PLUGIN VISIBILITY
        if channels.getChannelType(channels.channelNumber()) == midi.CT_GenPlug:
            channels.showCSForm(channels.channelNumber(), 1)
        self.updateMode()

        
            
    def remapForArturia(self, event):
        #_JARVIS.printCommandChannel(event)
        #_JARVIS.Warning(f"event data1 translated to: {MY_CC_TO_ANALOGLAB[event.data1]}")
        _JARVIS.Debug("remap for Arturia")
        _JARVIS.Debug(f"Original data1: {event.data1}")
        _JARVIS.Debug(f"Modified data1: {MY_CC_TO_ANALOGLAB[event.data1]}")
        # Need to send to CC mode in same channel as keyboard
        # You also need to set PORT_MIDICC_ANALOGLAB as the midi input port in the plugin settings
        device.forwardMIDICC(ControlModes['CC'][0] + (MY_CC_TO_ANALOGLAB[event.data1] << 8) + (event.data2 << 16) + (PORT_MIDICC_ANALOGLAB << 24))
    
    def pitchBendForArturia(self, event):
        
        # Need to send to CC mode in same channel as keyboard
        # You also need to set PORT_MIDICC_ANALOGLAB as the midi input port in the plugin settings
        device.forwardMIDICC(ControlModes['PITCHBEND'][0] + (event.data1 << 8) + (event.data2 << 16) + (PORT_MIDICC_ANALOGLAB << 24))
        
    def updateMode(self):
        if channels.getChannelType(channels.channelNumber()) == midi.CT_GenPlug:
            self._analogMode = plugins.getPluginName(channels.channelNumber()) in V_COL
        else:
            self._analogMode = False
        
        
    def activate_prev_channel(self, event):
        Actions.channel_rack_up(event)
        self.activateChannel()
        
    def activate_next_channel(self, event):
        Actions.channel_rack_down(event)
        self.activateChannel()
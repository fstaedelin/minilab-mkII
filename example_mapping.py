"""
    This file contains an implemented example of mapping
"""


from utility.mappings.dictionaries import COLORS, SYSEX, ControlModes
from utility.flcommands import *

from utility.mappings.maincontrollertypes import Pad, sysexPad, emptyPad, Knob, KnobPress, KnobShift
from utility.mappings.MiniLabMk2Mapping import MiniLabMapping

# Define the channels set in MIDI Control Center. You should put all buttons of the same mode in the same channel, which shouldn't be the keyboard one
CONTROL_CHANNEL = 2 # Shouldn't be 1

exampleMapping = MiniLabMapping(
    CONTROL_CHANNEL,
    # Knob mapping first
    [   
        # Knobs 1 to 8
        Knob(dummy),
        Knob(dummy),
        Knob(dummy),
        Knob(dummy),
        Knob(dummy),
        Knob(dummy),
        Knob(dummy),
        Knob(dummy),
        
        # Knobs 9 to 16
        Knob(dummy),
        Knob(dummy),
        Knob(dummy),
        Knob(dummy),
        Knob(dummy),
        Knob(dummy),
        Knob(dummy),
        Knob(dummy),
    ],
    
    # Shiftable knobs
    [        # Knobs 1 and 9 + SHIFT
        KnobShift(dummy),
        KnobShift(dummy),
    ],
    
    # Pressable knobs
    [    
        # Knobs 1 and 9 PRESS
        KnobPress(JogUp),
        KnobPress(JogDown),
    ],
    
    #Then Pads
    [
        # play/pause
        Pad(start, COLORS['GREEN'], COLORS['YELLOW'])
            ._addColorMap(COLORS['GREEN'], COLORS['YELLOW'], COLORS['RED'], transport.isRecording()),
        Pad(toggle_rec, COLORS['RED'], COLORS['RED'])
            ._addColorMap(COLORS['RED'], COLORS['RED'], transport.isRecording()),
        
        
        
        # Record drums
        Pad(Overdub, LED_COLOR_DEFAULT=COLORS['YELLOW']),
        # Record bass
        Pad(toggle_metronome, LED_COLOR_DEFAULT=COLORS['YELLOW']),
        # Record Synth1
        Pad(PlayDrums, COLORS['RED'], COLORS['RED']),
        # Record Synth2
        Pad(PlayMidKeys, COLORS['YELLOW'], COLORS['YELLOW']),
        # Record Sax
        Pad(PlayHiKeys, COLORS['YELLOW'], COLORS['YELLOW']),
        # Record Vocals
        Pad(vocalRecord, LED_COLOR_DEFAULT=COLORS['BLUE']),
        
        Pad(start, COLORS['GREEN'], COLORS['YELLOW'])
            ._addColorMap(COLORS['GREEN'], COLORS['YELLOW'], COLORS['RED'], transport.isRecording()),
        Pad(stop, COLORS['RED'], COLORS['RED']),
        # ToggleMute drums
        Pad(FPCToggleMute, LED_COLOR_DEFAULT=COLORS['RED']),
        # ToggleMute bass
        Pad(bassToggleMute, LED_COLOR_DEFAULT=COLORS['BLUE']),
        # ToggleMute Synth1
        Pad(MidKeysToggleMute, LED_COLOR_DEFAULT=COLORS['YELLOW']),
        # ToggleMute Synth2
        Pad(HiKeysToggleMute, LED_COLOR_DEFAULT=COLORS['YELLOW']),
        # ToggleMute Sax
        Pad(saxToggleMute, LED_COLOR_DEFAULT=COLORS['CYAN']),
        # ToggleMute Vocals
        Pad(vocalToggleMute, LED_COLOR_DEFAULT=COLORS['BLUE']),
    ]
)
         
        
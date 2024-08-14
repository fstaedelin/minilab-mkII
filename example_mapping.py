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
        Knob(normal_dummy),
        Knob(normal_dummy),
        Knob(normal_dummy),
        Knob(normal_dummy),
        Knob(normal_dummy),
        Knob(normal_dummy),
        Knob(normal_dummy),
        Knob(normal_dummy),
        
        # Knobs 9 to 16
        Knob(normal_dummy),
        Knob(normal_dummy),
        Knob(normal_dummy),
        Knob(normal_dummy),
        Knob(normal_dummy),
        Knob(normal_dummy),
        Knob(normal_dummy),
        Knob(normal_dummy),
    ],
    
    # Shiftable knobs
    [        # Knobs 1 and 9 + SHIFT
        KnobShift(normal_dummy),
        KnobShift(normal_dummy),
    ],
    
    # Pressable knobs
    [    
        # Knobs 1 and 9 PRESS
        KnobPress(normal_dummy),
        KnobPress(normal_dummy),
    ],
    
    #Then Pads
    [
        Pad(start, COLORS['GREEN'], COLORS['YELLOW'])
            ._addColorMap(COLORS['GREEN'], COLORS['YELLOW'], COLORS['RED'], transport.isRecording()),
        Pad(stop, COLORS['RED'], COLORS['RED']),
        # Record drums
        Pad(FPCRecord, LED_COLOR_DEFAULT=COLORS['RED']),
        # Record bass
        Pad(bassRecord, LED_COLOR_DEFAULT=COLORS['BLUE']),
        # Record Synth1
        Pad(MidKeysRecord, LED_COLOR_DEFAULT=COLORS['YELLOW']),
        # Record Synth2
        Pad(HiKeysRecord, LED_COLOR_DEFAULT=COLORS['YELLOW']),
        # Record Sax
        Pad(saxRecord, LED_COLOR_DEFAULT=COLORS['CYAN']),
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
         
        
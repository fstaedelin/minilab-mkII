"""
    This file contains an implemented example of mapping
"""


from backend.dictionaries import COLORS
from backend.dictionaries import SYSEX
from backend.dictionaries import ControlModes
from utility.flcommands import *

from backend.maincontrollertypes import Pad, sysexPad, emptyPad, Knob
from backend.MiniLabMk2Mapping import MiniLabMapping

# Define the channels set in MIDI Control Center. You should put all buttons of the same mode in the same channel, which shouldn't be the keyboard one
CONTROL_CHANNEL = 2 # Shouldn't be 1

exampleMapping = MiniLabMapping(
    CONTROL_CHANNEL,
    # Knob mapping first
    [
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 2),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 3),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 4),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 5),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 6),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 7),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 8),
        
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 9),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 10),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 11),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 12),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 13),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 14),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 15),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 16),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 17),
        
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 18),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 19),
        
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 20),
        Knob(normal_dummy, ControlModes['CC'][CONTROL_CHANNEL], 21),
    ],
    
    #Then Pads
    [
        sysexPad(callback_fn=sysex_start, sysexFn='PLAY', LED_COLOR_DEFAULT = COLORS['GREEN'], LED_COLOR_BEAT = COLORS['YELLOW'], LED_COLOR_BAR = COLORS['GREEN']),
        sysexPad(sysex_stop, sysexFn='STOP', LED_COLOR_DEFAULT=COLORS['RED']),
        # Record drums
        Pad(normal_dummy, ControlModes['CC'], dataout = 22, LED_COLOR_DEFAULT=COLORS['BLUE']),
        # Record bass
        Pad(normal_dummy, ControlModes['CC'], dataout = 23, LED_COLOR_DEFAULT=COLORS['BLUE']),
        # Record Synth1
        Pad(normal_dummy, ControlModes['CC'], dataout = 24, LED_COLOR_DEFAULT=COLORS['BLUE']),
        # Record Synth2
        Pad(normal_dummy, ControlModes['CC'], dataout = 25, LED_COLOR_DEFAULT=COLORS['BLUE']),
        # Record Sax
        Pad(normal_dummy, ControlModes['CC'], dataout = 26, LED_COLOR_DEFAULT=COLORS['BLUE']),
        # Record Vocals
        Pad(normal_dummy, ControlModes['CC'], dataout = 27, LED_COLOR_DEFAULT=COLORS['BLUE']),
        
        sysexPad(sysex_fastforward ,'FAST_FORWARD', COLORS['CYAN']),
        emptyPad(),
        emptyPad(),
        emptyPad(),
        sysexPad(sysex_rec_strobe ,'REC_STROBE', COLORS['RED'], COLORS['OFF']),
        
        Pad(normal_dummy, ControlModes['CC'], LED_COLOR_DEFAULT=COLORS['BLUE']),
        Pad(normal_dummy, ControlModes['CC'], LED_COLOR_DEFAULT=COLORS['BLUE']),
        Pad(normal_dummy, ControlModes['CC'], LED_COLOR_DEFAULT=COLORS['BLUE']),
        Pad(normal_dummy, ControlModes['CC'], LED_COLOR_DEFAULT=COLORS['BLUE']),
        Pad(normal_dummy, ControlModes['CC'], LED_COLOR_DEFAULT=COLORS['BLUE']),
        Pad(normal_dummy, ControlModes['CC'], LED_COLOR_DEFAULT=COLORS['BLUE']),
        Pad(normal_dummy, ControlModes['CC'], LED_COLOR_DEFAULT=COLORS['BLUE']),
        Pad(normal_dummy, ControlModes['CC'], LED_COLOR_DEFAULT=COLORS['BLUE']),
    ]
)
         
        
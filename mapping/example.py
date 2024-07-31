from mapping.dictionaries import COLORS
from mapping.dictionaries import SYSEX
from mapping.dictionaries import ControlModes
from utility.flcommands import *

from backend.maincontrollertypes import Pad, Knob
from mapping.MiniLabMk2Mapping import MiniLabMk2Mapping
    
KEYBOARD_CHANNEL = 1
CONTROL_CHANNEL = 2

exampleMapping = MiniLabMk2Mapping(
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
        Pad(sysex_start, ControlModes['SYSEX'], SYSEX['PLAY'], COLORS['GREEN'], True),
        Pad(sysex_stop, ControlModes['SYSEX'], SYSEX['STOP'], COLORS['RED'], False),
        Pad(sysex_rewind, ControlModes['SYSEX'], SYSEX['REWIND'], COLORS['CYAN'], False),
        Pad(sysex_fastforward, ControlModes['SYSEX'], SYSEX['FAST_FORWARD'], COLORS['CYAN'], False),
        Pad(None, 0, 0, COLORS['OFF'], False),
        Pad(None, 0, 0, COLORS['OFF'], False),
        Pad(None, 0, 0, COLORS['OFF'], False),
        Pad(sysex_rec_strobe, ControlModes['SYSEX'], SYSEX['REC_STROBE'], COLORS['YELLOW'], False),
        
        Pad(normal_dummy, ControlModes['CC'], 0, COLORS['RED'], False),
        Pad(normal_dummy, ControlModes['CC'], 0, COLORS['RED'], False),
        Pad(normal_dummy, ControlModes['CC'], 0, COLORS['RED'], False),
        Pad(normal_dummy, ControlModes['CC'], 0, COLORS['RED'], False),
        Pad(normal_dummy, ControlModes['CC'], 0, COLORS['RED'], False),
        Pad(normal_dummy, ControlModes['CC'], 0, COLORS['RED'], False),
        Pad(normal_dummy, ControlModes['CC'], 0, COLORS['RED'], False),
        Pad(normal_dummy, ControlModes['CC'], 0, COLORS['RED'], False),
    ]
)
         
        
"""
    This file contains an implemented example of mapping
"""


from backend.dictionaries import COLORS
from backend.dictionaries import SYSEX
from backend.dictionaries import ControlModes
from utility.flcommands import *

from backend.maincontrollertypes import Pad, sysexPad, Knob
from backend.MiniLabMk2Mapping import MiniLabMk2Mapping

# Define the channels set in MIDI Control Center. You should put all buttons of the same mode in the same channel, which shouldn't be the keyboard one
CONTROL_CHANNEL = 2 # Shouldn't be 1

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
        sysexPad(callback_fn=sysex_start, sysexFn='PLAY', LED_COLOR=COLORS['GREEN'], LED_BLINKONPLAY=True, LED_BLINKCOLOR=COLORS['YELLOW']),
        sysexPad(sysex_stop, 'STOP', COLORS['RED'], False),
        Pad(LED_COLOR=COLORS['OFF']),
        sysexPad(sysex_rec_strobe ,'REC_STROBE', COLORS['RED'], False),
        Pad(LED_COLOR=COLORS['BLUE']),
        Pad(LED_COLOR=COLORS['BLUE']),
        Pad(LED_COLOR=COLORS['BLUE']),
        Pad(LED_COLOR=COLORS['BLUE']),
        
        Pad(LED_COLOR=COLORS['BLUE']),
        Pad(LED_COLOR=COLORS['BLUE']),
        Pad(LED_COLOR=COLORS['BLUE']),
        Pad(LED_COLOR=COLORS['BLUE']),
        Pad(LED_COLOR=COLORS['BLUE']),
        Pad(LED_COLOR=COLORS['BLUE']),
        Pad(LED_COLOR=COLORS['BLUE']),
        Pad(LED_COLOR=COLORS['BLUE']),
    ]      

)
         
        
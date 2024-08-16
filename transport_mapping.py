"""
    This file contains a mapping for transport setup
"""


from utility.mappings.dictionaries import COLORS, SYSEX, ControlModes
from utility.fl_commands.actions import Actions

from utility.mappings.maincontrollertypes import Pad, sysexPad, emptyPad, Knob, KnobPress, KnobShift
from utility.mappings.MiniLabMk2Mapping import MiniLabMapping

# Define the channels set in MIDI Control Center. You should put all buttons of the same mode in the same channel, which shouldn't be the keyboard one
CONTROL_CHANNEL = 2 # Shouldn't be 1

transportMapping = MiniLabMapping(
    CONTROL_CHANNEL,
    # Knob mapping first
    [   
        # Knobs 1 to 8
        Knob(Actions.noop),
        Knob(Actions.noop),
        Knob(Actions.noop),
        Knob(Actions.noop),
        Knob(Actions.noop),
        Knob(Actions.noop),
        Knob(Actions.noop),
        Knob(Actions.noop),
        
        # Knobs 9 to 16
        Knob(Actions.noop),
        Knob(Actions.noop),
        Knob(Actions.noop),
        Knob(Actions.noop),
        Knob(Actions.noop),
        Knob(Actions.noop),
        Knob(Actions.noop),
        Knob(Actions.noop),
    ],
    
    # Shiftable knobs
    [        # Knobs 1 and 9 + SHIFT
        KnobShift(Actions.noop),
        KnobShift(Actions.noop),
    ],
    
    # Pressable knobs
    [    
        # Knobs 1 and 9 PRESS
        KnobPress(Actions.cycle_active_window),
        KnobPress(Actions.current_channel_toggle_mute),
    ],
    
    #Then Pads
    [
        # play/pause
        Pad(Actions.playpause, COLORS['GREEN'], COLORS['YELLOW']),
      
        # Stop
        Pad(Actions.stop, COLORS['RED']),
        
        # toggle record
        Pad(Actions.toggle_rec, COLORS['RED'], COLORS['RED']),
        
        # toggle metronome
        Pad(Actions.toggle_metronome, COLORS['YELLOW']),
        
        # toggle loop recording
        Pad(Actions.toggle_loop_recording, COLORS['YELLOW']),
        
        # toggle overdub
        Pad(Actions.toggle_overdub, COLORS['YELLOW']),
        
        # channel up
        Pad(Actions.channel_rack_up, COLORS['CYAN']),
        
        # channel down
        Pad(Actions.channel_rack_down, COLORS['CYAN']),
        
        ######################## REPEAT TO HAVE THEM FROM 1 TO 16
        # play/pause
        Pad(Actions.playpause, COLORS['GREEN'], COLORS['YELLOW']),
      
        # Stop
        Pad(Actions.stop, COLORS['RED']),
        
        # toggle record
        Pad(Actions.toggle_rec, COLORS['RED'], COLORS['RED']),
        
        # toggle metronome
        Pad(Actions.toggle_metronome, COLORS['YELLOW']),
        
        # toggle loop recording
        Pad(Actions.toggle_loop_recording, COLORS['YELLOW']),
        
        # toggle overdub
        Pad(Actions.toggle_overdub, COLORS['YELLOW']),
        
        # channel up
        Pad(Actions.channel_rack_up, COLORS['CYAN']),
        
        # channel down
        Pad(Actions.channel_rack_down, COLORS['CYAN']),
        
    ]
)
         
        
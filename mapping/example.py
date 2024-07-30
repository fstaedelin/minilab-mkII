from utility.midistati import *
from utility.cccodes import *
from utility.flcommands import normal_dummy
from utility.lightcommands import *
from utility.colors import COLORS

from mapping.backend import Pad
from mapping.backend import Knob
from mapping.backend import Mapping
        
exampleMapping = Mapping(
    # Knob mapping first
    [
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
        Knob(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 2),
    ],
    
    #Then Pads
    [
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
        Pad(normal_dummy, MIDI_STATUS_CONTROL_CHANGE_CHAN1, 0, COLORS['RED'], False),
    ],
)
         
        
"""
This file contains dictionnaries :
    ControlModes:       Functionality (str) -> MIDI stati (range),
    RESERVED_CC:        Functionality (str) -> Reserved CC adresses (int)
    SYSEX:              Functionality (str) -> SYSEX codes (bytes)
    COLORS:             Color name    (str) -> color code for lights (int)
    ID_PADS:            Pad number    (int) -> PAD Codes used to control lights (int)
"""

from midi import *

ControlModes = {
    'OFF' : 0,
    'NOTE_OFF' : range(MIDI_NOTEOFF, MIDI_NOTEON),
    'NOTE_ON' : range(MIDI_NOTEON, MIDI_KEYAFTERTOUCH),
    'PAD_AFTERTOUCH' : range(MIDI_KEYAFTERTOUCH, MIDI_CONTROLCHANGE),
    'CC' : range(MIDI_CONTROLCHANGE, MIDI_PROGRAMCHANGE),
    'PC' : range(MIDI_PROGRAMCHANGE, MIDI_CHANAFTERTOUCH),
    'AFTERTOUCH2' : range(MIDI_CHANAFTERTOUCH,MIDI_PITCHBEND),
    'PITCHBEND' : range(MIDI_PITCHBEND, MIDI_BEGINSYSEX),
    'SYSEX' : [MIDI_BEGINSYSEX, MIDI_ENDSYSEX],
    'OTHER' : range(MIDI_BEGINSYSEX, MIDI_SYSTEMRESET)
}

## Reserved CCs:
RESERVED_CC = {
    'MOD_WHEEL' : 1
}

# Color codes
COLORS = {
    'OFF' : 0x00,
    'RED' : 0x01,
    'BLUE' : 0x10,
    'PURPLE' : 0x11,
    'GREEN' : 0x04,
    'YELLOW' : 0x05,
    'CYAN' : 0x14,
    'WHITE' : 0x7F
}

SYSEX = {
    'STOP' : b'\xf0\x7f\x7f\x06\x01\xf7',
    'PLAY' : b'\xf0\x7f\x7f\x06\x02\xf7',
    'DEFERRED_PLAY' : b'\xf0\x7f\x7f\x06\x03\xf7',
    'FAST_FORWARD' : b'\xf0\x7f\x7f\x06\x04\xf7',
    'REWIND' : b'\xf0\x7f\x7f\x06\x05\xf7',
    'REC_STROBE' : b'\xf0\x7f\x7f\x06\x06\xf7',
    'REC_EXIT' : b'\xf0\x7f\x7f\x06\x07\xf7',
    'REC_READY' : b'\xf0\x7f\x7f\x06\x08\xf7',
    'PAUSE' : b'\xf0\x7f\x7f\x06\x09\xf7',
    'EJECT' : b'\xf0\x7f\x7f\x06\x0a\xf7',
    'CHASE' : b'\xf0\x7f\x7f\x06\x0b\xf7',
    'INLIST_RESET' : b'\xf0\x7f\x7f\x06\x0c\xf7',
}
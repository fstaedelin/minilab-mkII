"""
This file contains dictionnaries :
    ControlModes:       Functionality (str) -> MIDI stati (range),
    RESERVED_CC:        Functionality (str) -> Reserved CC adresses (int)
    SYSEX:              Functionality (str) -> SYSEX codes (bytes)
    COLORS:             Color name    (str) -> color code for lights (int)
    ID_PADS:            Pad number    (int) -> PAD Codes used to control lights (int)
    MATRIX_IDS_PADS:    Matrix containing Pads IDS
    
"""

from midi import *

ControlModes = {
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

ID_PADS = {
    0: 0x70, ## Default initialize to existing pad to not risk messing with sysex ...
    1: 0x70,    9: 0x78, 
    2: 0x71,    10: 0x79,
    3: 0x72,    11: 0x7A,
    4: 0x73,    12: 0x7B,
    5: 0x74,    13: 0x7C,
    6: 0x75,    14: 0x7D,
    7: 0x76,    15: 0x7E,
    8: 0x77,    16: 0x7F,
}

# Matrix with PADS IDS
MATRIX_IDS_PAD = [
    [ID_PADS[1], ID_PADS[2], ID_PADS[3], ID_PADS[4], ID_PADS[5], ID_PADS[6], ID_PADS[7], ID_PADS[8]],
    [ID_PADS[9], ID_PADS[10], ID_PADS[11], ID_PADS[12], ID_PADS[13], ID_PADS[14], ID_PADS[15], ID_PADS[16]],
]

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
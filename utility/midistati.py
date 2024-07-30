# The midi channel you want to send your info through
MIDI_SELECTED_CHANNEL = 1
MIDI_KEYBOARD_CHANNEL = 2
MIDI_FPC_CHANNEL = 3
MIDI_CHANNEL_INDEX = MIDI_SELECTED_CHANNEL-1

# Max supported MIDI channels ?
MIDI_N_CHANNELS=16

## from midi expanded message list PDF
## This is event.status in midiEvents

MIDI_STATUS_NOTE_OFF_CHAN1 = 128
MIDI_STATUS_BEGIN = MIDI_STATUS_NOTE_OFF_CHAN1
MIDI_STATUS_NOTE_ON_CHAN1 = MIDI_STATUS_NOTE_OFF_CHAN1 + MIDI_N_CHANNELS
MIDI_STATUS_POLYPHONIC_AFTERTOUCH_CHAN1 = MIDI_STATUS_NOTE_OFF_CHAN1 + 2*MIDI_N_CHANNELS
MIDI_STATUS_CONTROL_CHANGE_CHAN1 = MIDI_STATUS_NOTE_OFF_CHAN1 + 3*MIDI_N_CHANNELS
MIDI_STATUS_PROGRAM_CHANGE_CHAN1 = MIDI_STATUS_NOTE_OFF_CHAN1 + 4*MIDI_N_CHANNELS
MIDI_STATUS_AFTERTOUCH_CHAN1 = MIDI_STATUS_NOTE_OFF_CHAN1 + 5*MIDI_N_CHANNELS
MIDI_STATUS_PITCH_BEND_CHAN1 = MIDI_STATUS_NOTE_OFF_CHAN1 + 6*MIDI_N_CHANNELS
MIDI_STATUS_SYSEX = 240
MIDI_STATUS_END = MIDI_STATUS_SYSEX

# Small utility to define tables of length MIDI_N_CHANNELS starting from above indexes
def setStatusRange(firstChannelCode):
    return range(firstChannelCode, firstChannelCode+MIDI_N_CHANNELS)

MIDI_STATUS_NOTE_OFF=setStatusRange(MIDI_STATUS_NOTE_OFF_CHAN1)
MIDI_STATUS_NOTE_ON=setStatusRange(MIDI_STATUS_NOTE_ON_CHAN1)
MIDI_STATUS_POLYPHONIC_AFTERTOUCH=setStatusRange(MIDI_STATUS_POLYPHONIC_AFTERTOUCH_CHAN1)
MIDI_STATUS_CONTROL_CHANGE=setStatusRange(MIDI_STATUS_CONTROL_CHANGE_CHAN1)
MIDI_STATUS_PROGRAM_CHANGE=setStatusRange(MIDI_STATUS_PROGRAM_CHANGE_CHAN1)
MIDI_STATUS_AFTERTOUCH=setStatusRange(MIDI_STATUS_AFTERTOUCH_CHAN1)
MIDI_STATUS_PITCH_BEND=setStatusRange(MIDI_STATUS_PITCH_BEND_CHAN1)

# Utility to convert status to channel:
def statusToChannel(status):
    chn = -1
    if (status < MIDI_STATUS_BEGIN) or (status > MIDI_STATUS_END):
        print("Midi Status not recognized")
    elif status == MIDI_STATUS_SYSEX :
        print("Midi status SYSEX, do not change channel !")
    else:
        chn = (status-MIDI_STATUS_NOTE_OFF_CHAN1) % MIDI_N_CHANNELS +1
        
    return chn

# Utility to change to another channel:
def changeChannel(status, channel):
    offset = 0
    if (status < MIDI_STATUS_BEGIN) or (status > MIDI_STATUS_END):
        print("Midi Status not recognized")
    elif status == MIDI_STATUS_SYSEX :
        print("Midi status SYSEX, not changing channel !")
    else:
        offset = channel-((status-MIDI_STATUS_NOTE_OFF_CHAN1) % MIDI_N_CHANNELS +1)
    
    return status+offset
        
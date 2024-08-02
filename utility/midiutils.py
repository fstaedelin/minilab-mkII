### Contains definitions of MIDI statuses reported in ../doc/Expanded Messages List (Status Bytes).pdf
# This corresponds to event.status in midiEvents

# Max supported MIDI channels ?
MIDI_N_CHANNELS=16

## Here, could use the fl-api-stubs extension to retrieve midi codes from FL Studio
### DID NOT DO IT because fl python external libraries are not intuitive.
### Channel one of channel-linked MIDI functionalities
MIDI_STATUS_NOTE_OFF_CHAN1 = 128
MIDI_STATUS_BEGIN = MIDI_STATUS_NOTE_OFF_CHAN1
MIDI_STATUS_NOTE_ON_CHAN1 = MIDI_STATUS_NOTE_OFF_CHAN1 + MIDI_N_CHANNELS
MIDI_STATUS_POLYPHONIC_AFTERTOUCH_CHAN1 = MIDI_STATUS_NOTE_OFF_CHAN1 + 2*MIDI_N_CHANNELS
MIDI_STATUS_CONTROL_CHANGE_CHAN1 = MIDI_STATUS_NOTE_OFF_CHAN1 + 3*MIDI_N_CHANNELS
MIDI_STATUS_PROGRAM_CHANGE_CHAN1 = MIDI_STATUS_NOTE_OFF_CHAN1 + 4*MIDI_N_CHANNELS
MIDI_STATUS_AFTERTOUCH_CHAN1 = MIDI_STATUS_NOTE_OFF_CHAN1 + 5*MIDI_N_CHANNELS
MIDI_STATUS_PITCH_BEND_CHAN1 = MIDI_STATUS_NOTE_OFF_CHAN1 + 6*MIDI_N_CHANNELS

### Non channel-linked functionalities
MIDI_STATUS_SYSEX = 240
MIDI_STATUS_MIDI_TIME_CODE_QTR_FRAME = 241
MIDI_STATUS_SONG_POSITION_POINTER = 242
MIDI_STATUS_SONG_SELECT = 243
MIDI_STATUS_UNDEFINED_RESERVED = [244, 245, 253]
MIDI_STATUS_TUNE_REQUEST = 246
MIDI_STATUS_EOX = 247
MIDI_STATUS_TIMING_CLOCK = 248
MIDI_STATUS_START = 250
MIDI_STATUS_CONTINUE = 251
MIDI_STATUS_STOP = 252
MIDI_STATUS_ACTIVE_SENSING = 254
MIDI_STATUS_SYSTEM_RESET = 255
### Last MIDI status
MIDI_STATUS_END = MIDI_STATUS_SYSTEM_RESET


def setStatusRange(firstChannelCode):
    """Utility to define range containing all MIDI stati for a channel-linked functionality

    Args:
        firstChannelCode (int): The status code of channel1 for this functionality

    Returns:
        range: if status is channel-linked, returns the full range of midi stati that correspond to the functionality, else: returns a range containing the single input
    """
    if isChannelLinked(firstChannelCode):
        return range(firstChannelCode, firstChannelCode+MIDI_N_CHANNELS)
    else:
        return range(firstChannelCode,firstChannelCode+1)

def statusToChannel(status):
    """ Utility to convert MIDI status to channel number:

    Args:
        status (int): the MIDI status (event.status)

    Returns:
        int: Channel number between 0 and 16 inclusive
            if 0: input status is not a channel-linked MIDI code.
    """
    
    if isChannelLinked(status):
        return (status-MIDI_STATUS_NOTE_OFF_CHAN1) % MIDI_N_CHANNELS +1
    else:
        return 0
        
def changeStatusChannel(status: int, channel: int):
    """Utility to change a MIDI status to another channel:

    Args:
        status (int): the MIDI status (event.status)
        channel (1 << int << 16): the MIDI channel you want to set the status to

    Returns:
        int: if isChannelLinked: the status corresponding to the proper channel, else: the input status
    Raises:
        ValueError: if channel is not in 1, 16
    """
    
    if channel not in range(1, MIDI_N_CHANNELS+1):
        raise ValueError("utility.midiutils.changeStatusChannel: input channel must be in [[1, ", MIDI_N_CHANNELS, "]]")
    elif isChannelLinked(status):
        offset = channel-((status-MIDI_STATUS_NOTE_OFF_CHAN1) % MIDI_N_CHANNELS +1)
        return status+offset
    else:
        return status
    
    
    
def isChannelLinked(status: int):
    """returns True is the input status is in channel-linked status list

    Args:
        status (int): the midi status (event.status)

    Returns:
        bool: True is midi status corresponds to a channel-linked status, False if not
    Raises:
        ValueError: if input is not a midi status
    """
    
    if status in range(MIDI_STATUS_NOTE_OFF_CHAN1, MIDI_STATUS_SYSEX):
        return True
    elif (status < MIDI_STATUS_BEGIN) or (status > MIDI_STATUS_END):
        raise ValueError("utility.midiutils.isChannelLinked: This is not a MIDI status !")
    else:
        Warning("utility.midiUtils.isChannelLinked: Midi Status does not correspond to a channel-linked control")
        return False
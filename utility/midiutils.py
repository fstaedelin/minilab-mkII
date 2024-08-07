### Contains definitions of MIDI statuses reported in ../doc/Expanded Messages List (Status Bytes).pdf
# This corresponds to event.status in midiEvents

from midi import *
from utility.toolbox import MIDIWarning

MIDI_N_CHANNELS = 16

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
        return (status-MIDI_NOTEOFF) % MIDI_N_CHANNELS +1
    else:
        return status
        
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
        offset = channel-((status-MIDI_NOTEOFF) % MIDI_N_CHANNELS +1)
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
    
    if status in range(MIDI_NOTEOFF, MIDI_BEGINSYSEX):
        return True
    elif (status < MIDI_NOTEOFF) or (status > MIDI_SYSTEMRESET):
        raise ValueError("utility.midiutils.isChannelLinked: This is not a MIDI status !")
    else:
        MIDIWarning("utility.midiUtils.isChannelLinked: Midi Status does not correspond to a channel-linked control")
        return False
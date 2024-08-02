# name=MiniLab - Fef - WIP
"""
[[
    Surface:    MiniLab mkII
    Developer:    Fef
    Version:    Alpha 1.1
    Date:        30/07/2024

]]
"""

import midi
import ui
import sys
import mixer
import transport
import channels
import playlist
import patterns
import device


from MiniLabProcess import MiniLabMidiProcessor
from MiniLabControllerConfig import MidiControllerConfig

#import mapping
from utility.toolbox import checkHandled
from utility.toolbox import filterNotes
from utility.toolbox import filterAftertouch
from backend.dictionaries import ControlModes

from mappings.example_mapping import exampleMapping
#import ArturiaVCOL

#-----------------------------------------------------------------------------------------


_mk2 = MidiControllerConfig()
_processor = MiniLabMidiProcessor(_mk2, exampleMapping)


#----------STOCK FL EVENT HANDLER FUNCTIONS ------------------------------------------------------------------------------
# The event is received by OnMidiIn
# |-> OnSysEx: Processes SYSEX events
# |-> OnMidiMsg:
#       |-> Filters message if note or aftertouch (natively handled)
#       |-> Else, process event with generic processor


# Function called for each event
def OnMidiIn(event) :
    print("############## Event Received #############")
    # If you want to process SYSEX events before FL studio does, you need to do that here.
    if event.status == ControlModes['SYSEX']:
        _processor.ProcessSysExEvent(event)
        checkHandled(event)
    
    
        

def OnSysEx(event) :
    print('############## Enter OnSYSEX #############')
    #_processor.ProcessSysExEvent(event)
    checkHandled(event)
        
    
# Function called for each event not dealt with by onMidiIn
def OnMidiMsg(event) :
    
    print('############## Enter OnMidiMsg #############')
    # Ignore Notes On, Off, (maybe Pitch bends ?) to not transmit them to OnMidiMsg
    if filterNotes(event):
        #event.handled=True
        print("############## NoteOn/NoteOff Events natively handled #############")
    elif filterAftertouch(event):
        print("############## Pad aftertouch suppressed #############")
    elif not _processor.ProcessEvent(event):
        print('!\/!\/!\/!\/!\ EVENT NOT PROCESSED /!\/!\/!\/!\/!')
            
    #checkHandled(event)

def OnPitchBend(event) :
    print('############## Enter OnPitchBend #############')
    checkHandled(event)

def OnKeyPressure(event):
    print('############## Enter OnKeyPressure #############')
    checkHandled(event)

def OnChannelPressure(event):
    print('############## Enter OnChannelPressure #############')
    checkHandled(event)

def OnControlChange(event):
    print('############## Enter OnControlChange #############')
    checkHandled(event)
    
def OnProgramChange(event):
    print('############## Enter OnProgramChange #############')
    checkHandled(event)

#----------STOCK FL EVENT RETURN FUNCTIONS ------------------------------------------------------------------------------
# Function called when Play/Pause button is ON
def OnUpdateBeatIndicator(value):
    _mk2.LightReturn().ProcessPlayBlink(value)
    _mk2.LightReturn().ProcessRecordBlink(value)

#----------REACTIONS TO FL EVENTS FUNCTIONS ------------------------------------------------------------------------------

# Function called when FL Studio is starting
def OnInit():
    print('Loaded MIDI script for Arturia MiniLab mkII')
    _mk2.Sync()
    
def OnProjectLoad(status):
    print('############## Enter OnProjectLoad #############')

def OnRefresh(flags):
    print('############## Enter OnRefresh #############')
#    _mk2.LightReturn().MetronomeReturn()
    _mk2.SetTransport()
    _mk2.LightReturn().RecordReturn()
#        _mk2.LightReturn().BrowserReturn()
#        _mk2.LightReturn().NotBlinkingLed()
    
# Handles the script when FL Studio closes
def OnDeInit():
    print('############## Enter OnDeInit #############')
    return

# Function called at refresh, flag value changes depending on the refresh type 
#def OnRefresh(flags) :
#    print("enter OnRefresh")
#    if not AL_MEMORY :
#        _mk2.LightReturn().MetronomeReturn()
#        _mk2.LightReturn().RecordReturn()
#        #_mk2.LightReturn().PlayReturn()
#        _mk2.LightReturn().BrowserReturn()
#        _mk2.LightReturn().NotBlinkingLed()
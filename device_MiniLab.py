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
import utils

import ui
import sys
import mixer
import transport
import channels
import playlist
import patterns
import device
import gc

from MiniLabProcess import MidiProcessor
from MiniLabControllerConfig import ControllerConfig

#import mapping
from utility.toolbox import filterNotes, filterAftertouch
from utility.logger import Logger
from backend.dictionaries import ControlModes
from mappings.example_mapping import exampleMapping
#import ArturiaVCOL

#-----------------------------------------------------------------------------------------
# Set up the logger with the coolest name
_JARVIS = Logger()
_JARVIS.set_level("DEBUG")

#-----------------------------------------------------------------------------------------
_mk2 = ControllerConfig(exampleMapping)
_processor = MidiProcessor(exampleMapping)

#----------STOCK FL EVENT HANDLER FUNCTIONS ------------------------------------------------------------------------------
# The event is received by OnMidiIn
# |-> OnSysEx: Processes SYSEX events
# |-> OnMidiMsg:
#       |-> Filters message if note or aftertouch (natively handled)
#       |-> Else, process event with generic processor


# Function called for each event
def OnMidiIn(event) :
    __MIDIIN = Debug("OnMidiIn")
    # If you want to process SYSEX events before FL studio does, you need to do that here.
    if event.status == ControlModes['SYSEX']:
        _processor.ProcessSysExEvent(event)
    __MIDIIN.close()
    

def OnSysEx(event) :
    __ONSYSEX = DeviceWarning('OnSysEx')
    #_processor.ProcessSysExEvent(event)
    __ONSYSEX.close()
        
    
# Function called for each event not dealt with by onMidiIn
def OnMidiMsg(event) :
    # To test
    __ONMIDIMSG = DeviceWarning(title = "OnMidiMsg")
    #device.processMIDICC(event)
    #device.directFeedback(event)    
    # Ignore Notes On, Off, (maybe Pitch bends ?) to not transmit them to OnMidiMsg
    if filterNotes(event):
        Debug("Notes filtered")
    elif filterAftertouch(event):
        Debug("Pad aftertouch suppressed")
    else:
        _processor.ProcessEvent(event)
    __ONMIDIMSG.close()
        
    

def OnPitchBend(event) :
    Debug('Enter OnPitchBend')
    

def OnKeyPressure(event):
    __ONKEYPRESSURE = DeviceWarning('Enter OnKeyPressure')
    __ONKEYPRESSURE.close()

def OnChannelPressure(event):
   __ONCHANNELPRESSURE = DeviceWarning('Enter OnChannelPressure')
   __ONCHANNELPRESSURE.close()

def OnControlChange(event):
    __ONCONTROLCHANGE = DeviceWarning('Enter OnControlChange')
    __ONCONTROLCHANGE.close()
    
def OnProgramChange(event):
    __ONPROGRAMCHANGE = DeviceWarning('Enter OnProgramChange')
    __ONPROGRAMCHANGE.close()

#----------STOCK FL EVENT RETURN FUNCTIONS ------------------------------------------------------------------------------
# Function called when Play/Pause button is ON
#def OnUpdateBeatIndicator(value):
    #_mk2.ProcessBlink(value)

#----------REACTIONS TO FL EVENTS FUNCTIONS ------------------------------------------------------------------------------

# Function called when FL Studio is starting
def OnInit():
    print('Loaded MIDI script for Arturia MiniLab mkII')
    _mk2.InitSync()
    
def OnProjectLoad(status):
    Debug('Enter OnProjectLoad')

def OnRefresh(flags):
    Debug('Enter OnRefresh')
    _mk2.Sync()

# Handles the script when FL Studio closes
def OnDeInit():
    Debug('Enter OnDeInit')
    return
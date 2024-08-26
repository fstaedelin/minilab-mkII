# name=MiniLab - Fef - JARVISV2
"""
[[
    Surface:    MiniLab mkII
    Developer:    Fef
    Version:    Alpha 1.2
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
from utility.mappings.dictionaries import ControlModes
from transport_mapping import transportMapping
from utility.JARVIS import _JARVIS

#import ArturiaVCOL



#-----------------------------------------------------------------------------------------
_mk2 = ControllerConfig(transportMapping)
_processor = MidiProcessor(transportMapping)


#----------STOCK FL EVENT HANDLER FUNCTIONS ------------------------------------------------------------------------------
# The event is received by OnMidiIn
# |-> OnSysEx: Processes SYSEX events
# |-> OnMidiMsg:
#       |-> Filters message if note or aftertouch (natively handled)
#       |-> Else, process event with generic processor

# _JARVIS.WriteLog()

# Function called for each event
def OnMidiIn(event):
    _JARVIS.Navigate("OnMidiIn")
    if event.sysex != None:
        _JARVIS.Warning('Processing sysex event:')
        _JARVIS.Warning(f"event sysex: {event.sysex}")
        _JARVIS.WriteLog()
        _JARVIS.ClearLog()

    # If you want to process SYSEX events before FL studio does, you need to do that here.
    if event.status == ControlModes['SYSEX']:
        _processor.ProcessSysExEvent(event)
    _JARVIS.Navigate("parent")
    

def OnSysEx(event) :
    _JARVIS.Navigate("OnSysEx")
    #_processor.ProcessSysExEvent(event)
    _JARVIS.Navigate("parent")

        
    
# Function called for each event not dealt with by onMidiIn
def OnMidiMsg(event) :
    # To test
    _JARVIS.Navigate("OnMidiMsg")
    #device.processMIDICC(event)
    #device.directFeedback(event)    
    # Ignore Notes On, Off, (maybe Pitch bends ?) to not transmit them to OnMidiMsg
    if filterNotes(event):
        _JARVIS.Debug("Notes filtered")
    elif filterAftertouch(event):
        _JARVIS.Debug("Pad aftertouch suppressed")
    else:
        _processor.ProcessEvent(event)
    _JARVIS.WriteLog()
    _JARVIS.Navigate("parent")
        
    

def OnPitchBend(event) :
    _JARVIS.Navigate("Enter OnPitchBend")
    _JARVIS.Navigate("parent")

def OnKeyPressure(event):
    _JARVIS.Navigate("Enter OnKeyPressure")
    _JARVIS.Navigate("parent")

def OnChannelPressure(event):
    _JARVIS.Navigate("Enter OnChannelPressure")
    _JARVIS.Navigate("parent")

def OnControlChange(event):
    _JARVIS.Navigate("Enter OnControlChange")
    _JARVIS.Navigate("parent")
    
def OnProgramChange(event):
    _JARVIS.Navigate("Enter OnProgramChange")
    _JARVIS.Navigate("parent")

#----------STOCK FL EVENT RETURN FUNCTIONS ------------------------------------------------------------------------------
# Function called when Play/Pause button is ON
#def OnUpdateBeatIndicator(value):
    #_mk2.ProcessBlink(value)

#----------REACTIONS TO FL EVENTS FUNCTIONS ------------------------------------------------------------------------------

# Function called when FL Studio is starting
def OnInit():
    _JARVIS.Navigate("SCRIPT INIT")
    _JARVIS.Debug('Loaded MIDI script for Arturia MiniLab mkII')
    _mk2.InitSync()
    _JARVIS.Navigate("parent")
    _JARVIS.WriteLog()
    _JARVIS.ClearLog()
    
def OnProjectLoad(status):
    _JARVIS.Debug('Enter OnProjectLoad')

def OnRefresh(flags):
    _JARVIS.Debug('Enter OnRefresh')
    _mk2.Sync()
    _processor.updateMode()

# Handles the script when FL Studio closes
def OnDeInit():
    _JARVIS.Debug('Enter OnDeInit')
    return
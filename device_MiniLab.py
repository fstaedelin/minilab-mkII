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

from midi_check.MIDI_CHECK import MIDI_CHECK as MC

from MiniLabProcess import MidiProcessor
from MiniLabControllerConfig import ControllerConfig

#import mapping
from utility.toolbox import filterNotes, filterAftertouch
from backend.dictionaries import ControlModes
from mappings.example_mapping import exampleMapping
#import ArturiaVCOL

#-----------------------------------------------------------------------------------------
# Set up the logger with the coolest name
_JARVIS = MC("DEBUG")

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
    _JARVIS.Navigate("OnMidiIn")
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
    print('Loaded MIDI script for Arturia MiniLab mkII')
    _mk2.InitSync()
    
def OnProjectLoad(status):
    _JARVIS.Debug('Enter OnProjectLoad')

def OnRefresh(flags):
    _JARVIS.Debug('Enter OnRefresh')
    _mk2.Sync()

# Handles the script when FL Studio closes
def OnDeInit():
    _JARVIS.Debug('Enter OnDeInit')
    return
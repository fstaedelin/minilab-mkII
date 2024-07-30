# name=MiniLab - Fef - Stripped

"""
[[
    Surface:    MiniLab mkII
    Developer:    Fef
    Version:    Alpha 1.0
    Date:        09/08/2023

]]
"""


import time
import midi
import ui
import sys
import mixer
import transport
import channels
import playlist
import patterns
import device

from MiniLabLeds import MiniLabmk2Led
from MiniLabProcess import MiniLabMidiProcessor
from MiniLabReturn import MiniLabLightReturn

#import mapping
import utility.colors as colors
from utility.toolbox import checkHandled
from utility.toolbox import filterNotes
from utility.toolbox import filterAftertouch
#import ArturiaVCOL

## CONSTANT

TEMP = 0.25

#-----------------------------------------------------------------------------------------

# This is the master class. It will run the init lights pattern 
# and call the others class to process MIDI events

class MidiControllerConfig :
    def __init__(self):
        self._lights = MiniLabmk2Led()
        self._lightReturn = MiniLabLightReturn()
        
    def lights(self):
        return self._lights

    def LightReturn(self) :
        return self._lightReturn
    
    def SetLights(self, led_mapping):
        return self._lights.SetLights(led_mapping)
    
    def SetPadLights(self, color_matrix):
        return self._lights.SetPadLights(color_matrix)
    
    def SetAllPadLights(self, color):
        return self._lights.SetAllPadLights(color)
    
    def SetDefault(self) :
        self.SetPadLights(colors.default_pad_colors)
    
    def SetTransport(self) :
        self.SetPadLights(colors.transport_pad_colors)
    
    def Sync(self):
        # Syncs up all visual indicators on keyboard with changes from FL Studio.
        for i in colors.blinking_pattern :
            self.SetAllPadLights(i)
            time.sleep(TEMP)
        self.SetTransport()

_mk2 = MidiControllerConfig()
_processor = MiniLabMidiProcessor(_mk2)


#----------STOCK FL EVENT HANDLER FUNCTIONS ------------------------------------------------------------------------------

# Function called for each event
def OnMidiIn(event) :
    print("############## Event Received #############")
        
        

def OnSysEx(event) :
    print('############## Enter OnSYSEX #############')
    _processor.ProcessSysExEvent(event)
    checkHandled(event)
        
    
# Function called for each event not dealt with by onMidiIn
def OnMidiMsg(event) :
    
    print('############## Enter OnMidiMsg #############')
    # Ignore Notes On, Off, (maybe Pitch bends ?) to not transmit them to OnMidiMsg
    if filterNotes(event):
        #event.handled=True
        print("############## NoteOn/NoteOff Events natively handled ? #############")
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

def OnChannelPressure(event):
    print('############## Enter OnChannelPressure #############')

def OnControlChange(event):
    print('############## Enter OnControlChange #############')
    
def OnProgramChange(event):
    print('############## Enter OnProgramChange #############')

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
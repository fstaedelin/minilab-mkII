import device
import ui
import time
import transport
import mixer
from utility.lightcommands import SetPadColor
from backend.dictionaries import COLORS, ID_PADS


# This class handles visual feedback functions.


WidMixer = 0
WidChannelRack = 1
WidPlaylist = 2
WidBrowser = 4
WidPlugin = 5
from backend.MiniLabMk2Mapping import MiniLabMapping

class MiniLabLightReturn:
    def __init__(self, mapping: MiniLabMapping):
        self.padIDs = []
        self.fixedpadcolors = []
        self.blinkableIDs = []
        self.blinkingcolor1 = []
        self.blinkingcolor2 = []
        for pad in mapping.pads:
            self.padIDs.append(pad.ID_PAD)
            self.fixedpadcolors.append(pad.LED_COLOR)
            if pad.LED_BLINKONPLAY:
                self.blinkableIDs.append(pad.ID_PAD)
                self.blinkingcolor1.append(pad.LED_COLOR)
                self.blinkingcolor2.append(pad.LED_BLINKCOLOR)
        
        
    def MetronomeReturn(self) :
        if ui.isMetronomeEnabled() :
            print('Metronome Enabled')
        else :
            print('Metronome Not Enabled')

    def RecordReturn(self) :
        if transport.isRecording() :
            print('transport is Recording')
            SetPadColor(ID_PADS[8], COLORS['RED'])
        else :
            print('transport is not Recording')
            SetPadColor(ID_PADS[8], COLORS['YELLOW'])

    def PlayReturn(self) :
        if transport.isPlaying():
            SetPadColor(ID_PADS[1], COLORS['RED'])
        else :
            SetPadColor(ID_PADS[1], COLORS['OFF'])
                    
    def ProcessBlink(self, value):
        if transport.isPlaying():
                i=0
                for blinkingpad in self.blinkableIDs:
                    if value > 0:
                        SetPadColor(blinkingpad, self.blinkingcolor2[i])
                    else:
                        SetPadColor(blinkingpad, COLORS['OFF'])
                    i+=1
            
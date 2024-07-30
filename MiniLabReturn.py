import device
import ui
import time
import transport
import mixer
from utility.lightcommands import *
from utility.colors import *


# This class handles visual feedback functions.


WidMixer = 0
WidChannelRack = 1
WidPlaylist = 2
WidBrowser = 4
WidPlugin = 5


class MiniLabLightReturn:
# 0x02 :write param
# 0x00 :standard break
# 0x10 : Set Color
# 0x7C : Pad ID
# 0x05 : color
    def MetronomeReturn(self) :
        if ui.isMetronomeEnabled() :
            print('Metronome Enabled')
        else :
            print('Metronome Not Enabled')

    def RecordReturn(self) :
        if transport.isRecording() :
            print('transport is Recording')
            SetPadColor(ID_PAD8, C_RED)
        else :
            print('transport is not Recording')
            SetPadColor(ID_PAD8, C_YELLOW)

    def PlayReturn(self) :
        if transport.isPlaying():
            SetPadColor(ID_PAD1, C_RED)
        else :
            SetPadColor(ID_PAD1, C_OFF)
    
    def ProcessPlayBlink(self, value):
        if transport.isPlaying():
            if value == 0 :
                SetPadColor(ID_PAD1, C_YELLOW)
            else :
                SetPadColor(ID_PAD1, C_OFF)
        
    def ProcessRecordBlink(self, value) :
        if transport.isPlaying():
            if transport.isRecording() :            
                if value == 0 :
                    SetPadColor(ID_PAD8, C_RED)
                else :
                    SetPadColor(ID_PAD8, C_OFF)
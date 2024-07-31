import device
import ui
import time
import transport
import mixer
from utility.lightcommands import SetPadColor
from mapping.dictionaries import COLORS, ID_PADS


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
            SetPadColor(ID_PADS[8], COLORS['RED'])
        else :
            print('transport is not Recording')
            SetPadColor(ID_PADS[8], COLORS['YELLOW'])

    def PlayReturn(self) :
        if transport.isPlaying():
            SetPadColor(ID_PADS[1], COLORS['RED'])
        else :
            SetPadColor(ID_PADS[1], COLORS['OFF'])
    
    def ProcessPlayBlink(self, value):
        if transport.isPlaying():
            if value == 0 :
                SetPadColor(ID_PADS[1], COLORS['YELLOW'])
            else :
                SetPadColor(ID_PADS[1], COLORS['OFF'])
        
    def ProcessRecordBlink(self, value) :
        if transport.isPlaying():
            if transport.isRecording() :            
                if value == 0 :
                    SetPadColor(ID_PADS[8], COLORS['RED'])
                else :
                    SetPadColor(ID_PADS[8], COLORS['OFF'])
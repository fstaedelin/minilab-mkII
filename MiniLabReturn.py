import device
import ui
import time
import transport
import mixer
from utility.mappings.mappings_backend.dictionaries import COLORS


# This class handles visual feedback functions.


WidMixer = 0
WidChannelRack = 1
WidPlaylist = 2
WidBrowser = 4
WidPlugin = 5

ISPLAYING = 0
ISRECORDING = 1

from MiniLabLeds import MiniLabLeds

class MiniLabLightReturn:
    def __init__(self, leds: MiniLabLeds):
        self._lights = leds
        self.metronome_return = {}
        self.record_return = {}
        self.metronome_return = {}

    def MetronomeReturn(self) :
        if ui.isMetronomeEnabled() :
            print('Metronome Enabled')
        else :
            print('Metronome Not Enabled')

    def RecordReturn(self) :
        if transport.isRecording() :
            print('transport is Recording')
            self._lights.SetPadColor(MiniLabLeds.ID_PADS[8], COLORS['RED'])
        else :
            print('transport is not Recording')
            self._lights.SetPadColor(MiniLabLeds.ID_PADS[8], COLORS['YELLOW'])

    def PlayReturn(self) :
        if transport.isPlaying():
            self._lights.SetPadColor(MiniLabLeds.ID_PADS[1], COLORS['RED'])
        else :
            self._lights.SetPadColor(MiniLabLeds.ID_PADS[1], COLORS['OFF'])
                    
    def ProcessBlink(self, value):
        if transport.isPlaying():
                i=0
                for blinkingpad in self.blinkableIDs:
                    if value > 0:
                        self._lights.SetPadColor(blinkingpad, self.blinkingcolor2[i])
                    else:
                        self._lights.SetPadColor(blinkingpad, COLORS['OFF'])
                i+=1
            
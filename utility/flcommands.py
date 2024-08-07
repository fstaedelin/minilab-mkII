# import your template presets:
#import utility.FelixTemplate as template

# import proper FL STUDIO functions
import transport
import mixer
import patterns
import ui
import  midi
import general
import channels

#WINDOW TYPES
wdMixer=0
wdChannelRack=1
wdPlaylist=2
wdPianoRoll=3
wdBrowser=4
wdPlugin=5
wdPluginEffect=6
wdPluginGenerator=7

def start(event):
    print('Start')
    transport.start()

def stop(event):
    print('Stop')
    transport.stop()

def sysex_start(event):
    print('sysex_dispatcher -> sysex_start')
    start(event)
    
def sysex_stop(event):
    print('sysex_dispatcher -> sysex_stop')
    stop(event)
    
def sysex_fastforward(event):
    print('sysex_dispatcher -> sysex_ff')
    print('TODO: Modify this function to move two bars up or smth')
    transport.fastForward(2)

def sysex_rewind(event):
    print('sysex_dispatcher -> sysex_rewind')
    print('TODO: Modify this function to move two bars down or smth')
    transport.rewind(2)

def sysex_rec_strobe(event):
    print('sysex_dispatcher -> sysex_rec_strobe')
    transport.record()
    
def sysex_dummy(event):
    print('sysex_dispatcher -> sysex_dummy')
    print('TODO')
    print('\t |-> Check in MiniLabProcessor.sysex_dispatcher name of key')
    print('\t |-> Code in utility/flcommands')

def normal_dummy(event):
    print('Normal dummy')
# Record
def bassRecord(self, event):
    #mixer.armTrack(template.bass_trk)
    print('TODO')

def saxRecord(self, event):
    #mixer.armTrack(template.sax_trk)
    print('TODO')
    
def vocalRecord(self, event):
    #mixer.armTrack(template.vocals_trk)
    print('TODO')

def in4Record(self, event):
    #mixer.armTrack(template.in_4_trk)
    print('TODO')

def in5Record(self, event):
    #mixer.armTrack(template.in_5_trk)
    print('TODO')
    
def MidKeysRecord(self, event):
    #mixer.armTrack(template.in_5_trk)
    print('TODO')
    
def HiKeysRecord(self, event):
    #mixer.armTrack(template.in_5_trk)
    print('TODO')

def FPCRecord(self, event):
    channels.selectChannel(0, 1)
    transport.record()

# ToggleMute
def bassToggleMute(self, event):
    #mixer.armTrack(template.bass_trk)
    print('TODO')

def saxToggleMute(self, event):
    #mixer.armTrack(template.sax_trk)
    print('TODO')
    
def vocalToggleMute(self, event):
    #mixer.armTrack(template.vocals_trk)
    print('TODO')

def in4ToggleMute(self, event):
    #mixer.armTrack(template.in_4_trk)
    print('TODO')

def in5ToggleMute(self, event):
    #mixer.armTrack(template.in_5_trk)
    print('TODO')
    
def MidKeysToggleMute(self, event):
    #mixer.armTrack(template.in_5_trk)
    print('TODO')
    
def HiKeysToggleMute(self, event):
    #mixer.armTrack(template.in_5_trk)
    print('TODO')

def FPCToggleMute(self, event):
    channels.selectChannel(0, 1)
    transport.record()
    
# NAVIGATE

def loopThroughChannels(self, event):
    # Show channel rack and get to next track
    if ui.getFocused(wdChannelRack) != True :
        self._hideAll(event)
        self._show_and_focus(wdChannelRack)
    ui.jog(1)
    print(channels.getChannelName(channels.selectedChannel()))

def loopThroughPatterns(self, event):
    # Show channel rack and get to next track
    if ui.getFocused(wdPlaylist) != True :
        self._hideAll(event)
        self._show_and_focus(wdPlaylist)
    if patterns.patternNumber() < patterns.patternCount():
        patterns.jumpToPattern(patterns.patternNumber()+1)
    else:
        patterns.jumpToPattern(0)
    
    #print(patterns.getTrackName(patterns.selectedPattern()))

def NextWindow(self, event):
    ui.nextWindow()
    if ui.getFocused(wdPlugin) == True :
        self.PluginTest(event)

def Jog(self, event):
    if event.data2 in [63,62,61]:
        ui.jog(-1)
    if event.data2 in [65,65,67]:
        ui.jog(1)

#Patterns

def getPatternNames(self, event):
    patternNames=[]
    for i in range(patterns.patternCount()+1):
        patternNames.append(patterns.getPatternName(i))
    return patternNames

def getPatternColors(self, event):
    patternColors=[]
    for i in range(patterns.patternCount()+1):
        patternColors.append(patterns.getPatternColor(i))
    return patternColors

def clonePattern(self, event):
    colors = self.getPatternColors(event)
    names = self.getPatternNames(event)
    currentPattern = patterns.patternNumber()
    
            # Show channel rack and get to next track
    if ui.getFocused(wdPlaylist) != True :
        self._hideAll(event)
        self._show_and_focus(wdPlaylist)
    
    newPattern=patterns.patternCount()+1
    patterns.jumpToPattern(newPattern)
    patterns.setPatternName(newPattern, names[currentPattern]+str(newPattern))
    patterns.setPatternColor(newPattern, colors[currentPattern])

def Undo(self, event):
    general.undoUp()

# DISPATCH



def OnCommandEvent(self, event):
    self._midi_command_dispatcher.Dispatch(event)

def OnWheelEvent(self, event):
    self._wheel_dispatcher.Dispatch(event)

def OnKnobEvent(self, event):
    self._knob_dispatcher.Dispatch(event)

def OnDrumEvent(self, event) :
    #if event.status == 153 :
        #event.data1 = FPC_MAP.get(str(event.data1))
    #elif event.status == 137 :
        #event.data1 = FPC_MAP.get(str(event.data1))
    event.handled = False

# WINDOW
def _show_and_focus(self, window):
    if not ui.getVisible(window):
        ui.showWindow(window)
    if not ui.getFocused(window):
        ui.setFocused(window)


def _hideAll(self, event) :
    for i in range (channels.channelCount()) :
        channels.showEditor(i,0)


def SwitchWindow(self, event) :
    if ui.getFocused(wdChannelRack) :
        self.showPlugin(event)
    elif ui.getFocused(wdPlugin) :
        self.showPlugin(event)
    elif ui.getFocused(wdMixer) :
        mixer.armTrack(mixer.trackNumber())
        # plugin = channels.channelNumber()
        # for i in range(plugins.getParamCount(plugin)) :
            # print(i, plugins.getParamName(i,plugin), plugins.getParamValue(i,plugin))
    else :
        nodeFileType = ui.getFocusedNodeFileType()
        if nodeFileType == -1:
            return
        if nodeFileType <= -100:
            transport.globalTransport(midi.FPT_Enter, 1)
        else:
            ui.selectBrowserMenuItem()
            
def ToggleMixerChannelRack(self, event) :
    self.FakeMIDImsg()
    self._hideAll(event)
    global MIXER_MODE
    if MIXER_MODE == 0 :
        MIXER_MODE = 1
        self._show_and_focus(wdMixer)
    else :
        MIXER_MODE = 0
        self._show_and_focus(wdChannelRack)
    

def ToggleBrowserChannelRack(self, event) :
    if ui.getFocused(wdBrowser) != True :
        self._hideAll(event)
        self._show_and_focus(wdBrowser)
    else :
        self._hideAll(event)
        self._show_and_focus(wdChannelRack)
        
        
def TogglePlaylistChannelRack(self, event) :
    if ui.getFocused(wdPlaylist) != True :
        self._hideAll(event)
        self._show_and_focus(wdPlaylist)
    else :
        self._hideAll(event)
        self._show_and_focus(wdChannelRack)



# NAVIGATION

def TestCutOrNav(self, event) :
    if ui.getFocused(wdChannelRack) :
        self.Cut(event)
    elif ui.getFocused(wdPlugin) :
        self.PluginPreset
        

def Navigator(self, event):
    if ui.getFocused(wdPlugin) == True :
        self._hideAll(event)    
    elif ui.getFocused(wdBrowser) == True :
        if event.data2 in [63,62,61] :
            self._show_and_focus(wdBrowser)
            self._hideAll(event)
            ui.up()
        elif event.data2 in [65,66,67] :  
            self._show_and_focus(wdBrowser)
            self._hideAll(event)
            ui.down()
    elif ui.getFocused(wdMixer) == True :
        if event.data2 in [63,62,61] :
            self._show_and_focus(wdMixer)
            self._hideAll(event)
            ui.previous()
        elif event.data2 in [65,66,67] :  
            self._show_and_focus(wdMixer)
            self._hideAll(event)
            ui.next()
    else :
        self._show_and_focus(wdChannelRack)
        if event.data2 in [63,62,61] :
            self._show_and_focus(wdChannelRack)
            self._hideAll(event)
            ui.previous()
            mixer.setTrackNumber(channels.getTargetFxTrack(channels.channelNumber()),3)
        elif event.data2 in [65,66,67] :  
            self._show_and_focus(wdChannelRack)
            self._hideAll(event)
            ui.next()
            mixer.setTrackNumber(channels.getTargetFxTrack(channels.channelNumber()),3)


def PluginTest(self, event) :
    if ui.getFocused(wdPlugin) :
        string = channels.getChannelName(channels.channelNumber())
        if string in ['Hi Keys', 'Mid Keys'] :
            self.AnalogLabPreset(event)
        else :
            self.PluginPreset(event)
    elif ui.getFocused(wdPlaylist) :
        zoom = event.data2 - 64
        ui.horZoom(zoom)


def showPlugin(self, event) :
    channels.showEditor(channels.channelNumber())


# FUNCTIONS
def FastForward(self, event):
    if event.data2 == 1:
        transport.fastForward(2)
    else:
        transport.fastForward(0)

def Rewind(self, event):
    if event.data2 == 1:
        transport.rewind(2)
    else:
        transport.rewind(0)

def LoopMode(self, event) :
    transport.setLoopMode()

def Record(self, event) :
    transport.record()


def Start(self, event) :
    transport.start()          

def PlayPause(self, event) :
    if transport.isPlaying() == True:
        transport.stop()
    else:
        transport.start()

def Stop(self, event) :
    transport.stop()
    

def Loop(self, event) :
    transport.globalTransport(midi.FPT_LoopRecord,1)


def Cut(self, event) :
    self._show_and_focus(midi.wdChannelRack)
    ui.cut()
    
def Undo(self, event) :
    transport.globalTransport(midi.FPT_Undo, midi.FPT_Undo, event.pmeFlags)
    

def Overdub(self, event) :
    transport.globalTransport(midi.FPT_Overdub,1)


def SetClick(self, event) :
    transport.globalTransport(midi.FPT_Metronome,1)
    self._controller.blink()
    

def TapTempo(self, event) :
    transport.globalTransport(midi.FPT_TapTempo,1)
    
    
def SetVolumeTrack(self, event) :
    value = event.data2/127
    mixer.setTrackVolume(mixer.trackNumber(),0.8*value)
        

def SetPanTrack(self, event) :
    value = (event.data2-64)/64
    mixer.setTrackPan(mixer.trackNumber(),value)


#def AnalogLabPreset(self, event) :
#    if event.data2 == 65 :
#        device.forwardMIDICC(event.status + (0x1D << 8) + (0x7F << 16) + (PORT_MIDICC_ANALOGLAB << 24))
#    elif event.data2 ==63 :
#        device.forwardMIDICC(event.status + (0x1C << 8) + (0x7F << 16) + (PORT_MIDICC_ANALOGLAB << 24))


def Plugin(self, event) :
    if ui.getFocused(wdPlugin) :
        if event.status != 224 :
            clef = event.data1
        else :
            clef = 224
        #param, value = MiniLabmk2Plugin.Plugin(event, clef)
        

def PluginPreset(self, event) :
    return 0
    #if event.data2 == 65  :
        #plugins.nextPreset(channels.channelNumber())
    #elif event.data2 == 63 :
        #plugins.prevPreset(channels.channelNumber())


#def ForwardAnalogLab(self, event) :
#    if channels.getChannelName(channels.channelNumber()) in ['Hi Keys', 'Mid #Keys'] :
#        device.forwardMIDICC(event.status + (event.data1 << 8) + (event.data2 << #16) + (PORT_MIDICC_ANALOGLAB << 24))
#    else :            
#        self.Plugin(event)


def MixerParam(self, event) :
    if event.controlNum == 35 :
        value = 32*(event.data2-64)
        self.HandleKnob(midi.REC_Mixer_EQ_Gain + 0 + mixer.getTrackPluginId(mixer.trackNumber(), 0), value)
    elif event.controlNum == 36 :
        value = 32*(event.data2-64)
        self.HandleKnob(midi.REC_Mixer_EQ_Gain + 2 + mixer.getTrackPluginId(mixer.trackNumber(), 0), value)
    elif event.controlNum == 6 :
        value = 512*event.data2
        self.HandleKnob(midi.REC_Mixer_EQ_Freq + 0 + mixer.getTrackPluginId(mixer.trackNumber(), 0), value)    
    elif event.controlNum == 7 :
        value = 512*event.data2
        self.HandleKnob(midi.REC_Mixer_EQ_Freq + 2 + mixer.getTrackPluginId(mixer.trackNumber(), 0), value)


def HandleKnob(self, ID, Data2):
    mixer.automateEvent(ID, Data2, midi.REC_Mixer_EQ_Gain, 0, 0, 0) 
    
# UTILITY
def FakeMIDImsg(self) :
    transport.globalTransport(midi.FPT_Punch,1)
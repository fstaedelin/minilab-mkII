import channels
import mixer
import patterns
import playlist
import transport
import ui
import device
#import plugins
import midi
#import MiniLabmk2Plugin
import FelixTemplate as template

import mapping
import general

from MiniLabDispatch import MidiEventDispatcher
from MiniLabDispatch import send_to_device
import ArturiaVCOL


# This class processes all CC coming from the controller
# The class creates new handler for each function
# The class calls the right fonction depending on the incoming CC

## CONSTANT

PORT_MIDICC_ANALOGLAB = 10

#WINDOW TYPES
wdMixer=0
wdChannelRack=1
wdPlaylist=2
wdPianoRoll=3
wdBrowser=4
wdPlugin=5
wdPluginEffect=6
wdPluginGenerator=7

# MIXER
MIXER_MODE = 0

DRUM_PATTERNS = 1
MID_KEYS_PATTERNS = 1
HI_KEYS_PATTERNS = 1

class MiniLabMidiProcessor:
    @staticmethod
    def _is_pressed(event):
        return event.controlVal != 0

    def __init__(self, controller):
        def by_midi_id(event) : return event.midiId
        def by_control_num(event) : return event.controlNum
        def by_velocity(event) : return event.data2
        def by_status(event) : return event.status
        def ignore_release(event): return self._is_pressed(event)
        def ignore_press(event): return not self._is_pressed(event)

        self._controller = controller

        self._midi_id_dispatcher = (
            MidiEventDispatcher(by_midi_id)
            .NewHandler(176, self.OnCommandEvent)
            .NewHandler(224, self.OnWheelEvent)
            )
        
        self._midi_command_dispatcher = (
            MidiEventDispatcher(by_control_num)
            # Transport mode Knobs
            .NewHandler(mapping.transportKnobs.KnobList[0].CC, self.NextWindow, ignore_release)
            .NewHandler(mapping.transportKnobs.KnobList[2].CC, self.Jog)
            .NewHandler(mapping.transportKnobs.KnobList[12].CC, self.Navigator)   
            # Transport Pads           
            .NewHandler(mapping.transportPads.PadList[0].CC, self.Start)
            .NewHandler(mapping.transportPads.PadList[1].CC, self.Stop)
            .NewHandler(mapping.transportPads.PadList[2].CC, self.Record)
            .NewHandler(mapping.transportPads.PadList[3].CC, self.Rewind)
            .NewHandler(mapping.transportPads.PadList[4].CC, self.FastForward)
            .NewHandler(mapping.transportPads.PadList[5].CC, self.SetClick)
            .NewHandler(mapping.transportPads.PadList[6].CC, self.Overdub)
            .NewHandler(mapping.transportPads.PadList[7].CC, self.LoopMode)
            .NewHandler(mapping.transportPads.PadList[8].CC, self.bassRecord)
            .NewHandler(mapping.transportPads.PadList[9].CC, self.saxRecord)
            .NewHandler(mapping.transportPads.PadList[10].CC, self.vocalRecord)
            .NewHandler(mapping.transportPads.PadList[11].CC, self.in4Record)
            .NewHandler(mapping.transportPads.PadList[12].CC, self.Start)
            .NewHandler(mapping.transportPads.PadList[13].CC, self.Stop)
            .NewHandler(mapping.transportPads.PadList[14].CC, self.Record)
            .NewHandler(mapping.transportPads.PadList[15].CC, self.loopThroughChannels, ignore_press)
            
            # FPC Pads, only last two ones are handled here
            .NewHandler(mapping.FPCPads.PadList[6].CC, self.FPCRecord)
            .NewHandler(mapping.FPCPads.PadList[7].CC, self.Start)

            .NewHandler(mapping.FPCPads.PadList[14].CC, self.FPCRecord)
            .NewHandler(mapping.FPCPads.PadList[15].CC, self.Start)

            # Keyboard mode knobs
            .NewHandler(mapping.KeyboardKnobs.KnobList[0].CC, self.NextWindow, ignore_release)
            .NewHandler(mapping.KeyboardKnobs.KnobList[2].CC, self.Jog)
            .NewHandler(mapping.KeyboardKnobs.KnobList[12].CC, self.Navigator)          
            
            # Keyboard mode pads
            .NewHandler(mapping.KeyboardPads.PadList[3].CC, self.Overdub, ignore_release)
            .NewHandler(mapping.KeyboardPads.PadList[4].CC, self.loopThroughPatterns, ignore_press)
            .NewHandler(mapping.KeyboardPads.PadList[5].CC, self.loopThroughChannels, ignore_press)
            .NewHandler(mapping.KeyboardPads.PadList[6].CC, self.clonePattern, ignore_press)
            .NewHandler(mapping.KeyboardPads.PadList[7].CC, self.Undo, ignore_press)
            


            
            
        )
        
        self._knob_dispatcher = (
            MidiEventDispatcher(by_velocity)

        )
        
            # MAPPING WHEEL
        
        self._wheel_dispatcher = (
            MidiEventDispatcher(by_status)
            .NewHandler(224, self.ForwardAnalogLab)
        )

    # Record
    def bassRecord(self, event):
        mixer.armTrack(template.bass_trk)
    
    def saxRecord(self, event):
        print("hey")
        mixer.armTrack(template.sax_trk)

    def vocalRecord(self, event):
        mixer.armTrack(template.vocals_trk)
    
    def in4Record(self, event):
        mixer.armTrack(template.in_4_trk)

    def in5Record(self, event):
        mixer.armTrack(template.in_5_trk)
    
    def FPCRecord(self, event):
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

    def ProcessEvent(self, event) :
        #if event.status in [153,137] :
        #    return self.OnDrumEvent(event)
        #else :
        print(event.status,"\t",event.data1,"\t",event.controlNum,"\t",event.data2,"\t",event.midiId)
        return self._midi_id_dispatcher.Dispatch(event)


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

  
    def AnalogLabPreset(self, event) :
        if event.data2 == 65 :
            device.forwardMIDICC(event.status + (0x1D << 8) + (0x7F << 16) + (PORT_MIDICC_ANALOGLAB << 24))
        elif event.data2 ==63 :
            device.forwardMIDICC(event.status + (0x1C << 8) + (0x7F << 16) + (PORT_MIDICC_ANALOGLAB << 24))


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
    
    
    def ForwardAnalogLab(self, event) :
        if channels.getChannelName(channels.channelNumber()) in ['Hi Keys', 'Mid Keys'] :
            device.forwardMIDICC(event.status + (event.data1 << 8) + (event.data2 << 16) + (PORT_MIDICC_ANALOGLAB << 24))
        else :            
            self.Plugin(event)
 
 
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
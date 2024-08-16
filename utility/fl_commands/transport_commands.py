# To get access to master transport functions
import transport
import patterns
import ui
from utility.JARVIS import _JARVIS
from utility.fl_commands.actions import Actions
# to access transport.globalTransport() commands FPT_*
import midi

#WINDOW TYPES
wdMixer=0
wdChannelRack=1
wdPlaylist=2
wdPianoRoll=3
wdBrowser=4
wdPlugin=5
wdPluginEffect=6
wdPluginGenerator=7




def dummy(unused_param_value):
    print('Normal dummy')
    
def JogUp(unused_param_value):
    _JARVIS.Debug("JogUp")
    ui.jog(1)

def JogDown(unused_param_value):
    _JARVIS.Debug("JogDown")
    ui.jog(-1)

def start(unused_param_value):
    print('Start')
    transport.start()

def stop(unused_param_value):
    print('Stop')
    transport.stop()
    
def fastforward(unused_param_value):
    transport.fastForward(2)

def rewind(unused_param_value):
    transport.rewind(2)

def toggle_rec(unused_param_value):
    transport.record()
    
def toggle_overdub(unused_param_value) :
    transport.globalTransport(midi.FPT_Overdub,1)

def toggle_metronome(unused_param_value) :
    transport.globalTransport(midi.FPT_Metronome,1)

def TapTempo(unused_param_value) :
    transport.globalTransport(midi.FPT_TapTempo,1)

def toggle_loop_rec(unused_param_value):
    transport.globalTransport(midi.FPT_LoopRecord, 1)

    
def channel_up(unused_param_value):
    Actions.channel_rack_down()
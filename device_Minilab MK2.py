# name=Minilab MK2

import mixer
import device
import general
import ui
import transport
import launchMapPages
import playlist
import channels
import patterns
import arrangement
import midi

AUTO_SWITCH_TO_CONTROLLED_PARAMETER = True

def print_midi_info(event):
    print("handled: {}, timestamp: {}, status: {}, data1: {}, data2: {}, port: {}, midiId: {}".format(event.handled, event.timestamp, event.status, event.data1, event.data2, event.port, event.midiId))

def OnControlChange(event):
    print_midi_info(event)
    track = mixer.trackNumber()
    length = transport.getSongLength(5)
    print(length, transport.getSongPos(5))


    #start
    if event.data1 == 113 and event.data2 == 127:
        transport.start()
        event.handled = True
        return

    #stop
    if event.data1 == 115 and event.data2 == 127:
        transport.stop()
        event.handled =True
        return

    #set track
    if event.data1 == 112 and event.data2 == 63:
        print(track)
        if track > 0:
            mixer.setTrackNumber(track-1)
    if event.data1 == 112 and event.data2 == 65:
        mixer.setTrackNumber(track+1)

    
    #set volume
    if event.data1 == 75 and event.data2 == 63:
        mixer.setTrackVolume(track, mixer.getTrackVolume(track)-0.005)
    if event.data1 == 75 and event.data2 == 65:
        mixer.setTrackVolume(track, mixer.getTrackVolume(track)+0.005)
    

    #set pan
    if event.data1 == 72 and event.data2 <= 63:
        print("reached")
        mixer.setTrackPan(track, mixer.getTrackPan(track)-0.01)
    if event.data1 == 72 and event.data2 >= 65:
        mixer.setTrackPan(track, mixer.getTrackPan(track)+0.01)

    
    #solo
    if event.data1 == 36 and event.data2 > 0:
        mixer.soloTrack(track)

    
    #mute
    if event.data1 == 37 and event.data2 > 0:
        mixer.muteTrack(track)

    #seek
    if event.data1 == 73 and event.data2 == 1:
        transport.setSongPos(transport.getSongPos()+0.06)
        return
    if event.data1 == 73 and event.data2 == 127:
        transport.setSongPos(transport.getSongPos()-0.06)
        return

    if event.data1 == 79 and event.data2 == 17:
        transport.setSongPos(transport.getSongPos()+0.01)
        return
    if event.data1 == 79 and event.data2 == 15:
        transport.setSongPos(transport.getSongPos()-0.01)
        return

    #record
    if event.data1 == 38 and event.data2 > 0:
        transport.record()

    #mode (song or pattern)
    if event.data1 == 39 and event.data2 > 0:
        transport.setLoopMode()
    

    #show mixer
    if event.data1 == 43 and event.data2 > 0:
        transport.globalTransport(68,1)


    #step sequencer
    if event.data1 == 42 and event.data2 > 0:
        transport.globalTransport(65,1)


    #piano roll
    if event.data1 == 41 and event.data2 > 0:
        transport.globalTransport(66,1)


    #reset
    if event.data1 == 40 and event.data2 >0:
        mixer.setTrackPan(track, 0)
        mixer.setTrackVolume(track, 0.8)
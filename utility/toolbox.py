from utility.midistati import *

def checkHandled(event):
    if event.handled == False:
        print('/!\/!\/!\/!\ Event not handled /!\/!\/!\/!')
        print('event status: ', event.status)
        print('event data1: ', event.data1)
        print('event data2: ', event.data2)
        print('event sysex: ', event.sysex)
        print('/!\/!\/!\/!\/!\/!\/!\/!')
            
def printCommandChannel(event):
    stat = event.status
    if stat in MIDI_STATUS_CONTROL_CHANGE:
        print('Control Changed on Channel ', stat-MIDI_STATUS_CONTROL_CHANGE_CHAN1+1)
        print('Control number:', event.data1)
        print('Value:', event.data2)
    else:
        print('This is not a Control Change !')
        print('event status: ', event.status)

def filterNotes(event):
    if (event.status in MIDI_STATUS_NOTE_OFF) or  (event.status in MIDI_STATUS_NOTE_ON):
        event.handled = True
    return event.handled

def filterAftertouch(event):
    if (event.status in MIDI_STATUS_POLYPHONIC_AFTERTOUCH):
        event.handled = True
    return event.handled

def filterPitchBends(event):
    if (event.status in MIDI_STATUS_PITCH_BEND):
        event.handled = True
    return event.handled

def printHandled():
    print("############## Event Handled #############")
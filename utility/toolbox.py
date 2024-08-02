from backend.dictionaries import *

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
    if stat in ControlModes['CC']:
        print('Control Changed on Channel ', stat-ControlModes['CC'][0]+1)
        print('Control number:', event.data1)
        print('Value:', event.data2)
    else:
        print('This is not a Control Change !')
        print('event status: ', event.status)

def filterNotes(event):
    if (event.status in ControlModes['NOTE_OFF']) or  (event.status in ControlModes['NOTE_ON']):
        event.handled = True
    return event.handled

def filterAftertouch(event):
    if (event.status in ControlModes['PAD_AFTERTOUCH']):
        event.handled = True
    return event.handled

def filterPitchBends(event):
    if (event.status in ControlModes['PITCHBEND']):
        event.handled = True
    return event.handled

def printHandled():
    print("############## Event Handled #############")
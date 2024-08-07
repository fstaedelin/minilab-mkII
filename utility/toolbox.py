from backend.dictionaries import *
def function_dummy():
    print('Dummy function')

def printCommandChannel(event):
    id = event.midiId
    if id in ControlModes['CC']:
        print('Control Changed on Channel ', id-ControlModes['CC'][0]+1)
        print('Control number:', event.data1)
        print('Value:', event.data2)
        print('Port:', event.port)
    else:
        print('This is not a Control Change !')
        print('event status: ', event.status)

def filterNotes(event):
    filtered = False
    if (event.status in ControlModes['NOTE_OFF']) or  (event.status in ControlModes['NOTE_ON']):
        print('MIDI notes natively handled')
        filtered = True
    return filtered

def filterAftertouch(event):
    if (event.status in ControlModes['PAD_AFTERTOUCH']):
        event.handled = True
    return event.handled

def filterPitchBends(event):
    if (event.status in ControlModes['PITCHBEND']):
        event.handled = True
    return event.handled

def printHandled():
    print('############## Event Handled #############')

def printEvent(event):
        print('event midiId: ' + str(event.midiId))
        print('event status: ' + str(event.status))
        print('event data1: ' + str(event.data1))
        print('event data2: ' + str(event.data2))
        print('event sysex: ' + str(event.sysex))
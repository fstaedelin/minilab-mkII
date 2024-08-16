from utility.mappings.dictionaries import *
from utility.JARVIS import _JARVIS

def function_dummy():
    _JARVIS.Error('Dummy function')

def filterNotes(event):
    filtered = False
    if (event.status in ControlModes['NOTE_OFF']) or  (event.status in ControlModes['NOTE_ON']):
        _JARVIS.Debug('MIDI notes natively handled')
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
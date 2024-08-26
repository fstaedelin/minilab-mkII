from .midicheck import MIDI_CHECK
from .mappings.dictionaries import ControlModes
from .midiutils import statusToChannel

#-----------------------------------------------------------------------------------------
# Set up the logger with the coolest name

class JARVIS(MIDI_CHECK):
    def __init__(self):
        super().__init__("ERROR")
        
    def printCommandChannel(self, event):
        if event.midiId in ControlModes['CC']:
            self.Warning(f"Event status: {event.status}")
            self.Warning(f"Control Changed on Channel {statusToChannel(event.status)}")
            self.Warning(f"Control number: {event.data1}")
            self.Warning(f"Value: {event.data2}")
            self.Warning(f"Port: {event.port}")
        else:
            self.Debug("This is not a Control Change !")
            self.Debug(f"event status: {event.status}")
    
_JARVIS = JARVIS()
_JARVIS.Navigate("TEST_PRESETS")


#_JARVIS.WriteLog()



# Add a test to check if a given value is greater than 100.
# This test returns True if the value exceeds 100, otherwise False.
        
is_more_100 = _JARVIS.AddTest(
    test_fn=lambda x: x > 100,
    name=">100"
)

# Add a test to check if a given value is greater than 150.
# This test returns True if the value exceeds 150, otherwise False.
is_more_150 = _JARVIS.AddTest(
    test_fn=lambda x: x > 150,
    name=">150"
)
_JARVIS.Navigate("parent")

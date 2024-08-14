from utility.midi_check.MIDI_CHECK.mc import MIDI_CHECK as MC

#-----------------------------------------------------------------------------------------
# Set up the logger with the coolest name
_JARVIS = MC("DEBUG")

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

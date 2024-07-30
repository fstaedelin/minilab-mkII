from controlModes import *
# The midi channel you want to send your info through
MIDI_SELECTED_CHANNEL = 1
MIDI_CHANNEL_INDEX = MIDI_SELECTED_CHANNEL-1

###########################################
#############    MODES   #############
###########################################
MODE_SYSEX = 0
MODE_CONTROL_ABSOLUTE = 1
MODE_CONTROL_SWITCH = 2
MODE_CONTROL_RELATIVE = 3
MODE_PITCHBEND = 4
MODE_MIDINOTE = 5
MODE_DEFAULT = 1  # DEFAULT MODE IS CONTROL ABS


###########################################
#############    KNOBS   ##################
###########################################

# number of knob-type controls 
numberOfKnobs = 20

class Knob:

    def __init__(self, name, mode=MODE_SYSEX, chn=MIDI_SELECTED_CHANNEL, CCV=2):
        self.setName(name)
        self.setMode(mode)
        self.setChannel(chn)
        self.setCC(CCV)
        

    def setName(self, name):
        self.name = name

    def setMode(self, mod):
        self.mode = mod

    def setChannel(self, chn):
        self.channel = chn

    def setCC(self, CCV):
        self.CC = CCV

    def printKnob(self):
        print(self.name)
        self.mode.printMode()
        print("Channel : ", self.channel, ", CC : ", self.CC)

KnobNames=["K1SWITCH", "K1SHIFT"]
for i in range(8):
    KnobNames.append("K"+str(i+1))
KnobNames.append("K9SWITCH")
KnobNames.append("K9SHIFT")
for i in range(9):
    KnobNames.append("K"+str(i+9))

class KnobMap:
    def __init__(self):
        self.KnobList = []
        for i in range(numberOfKnobs):
            name = KnobNames[i]
            self.KnobList.append(Knob(name, modeControlAbs, MIDI_SELECTED_CHANNEL, i))
        
    def offsetKnobsCC(self, offset):
        for i in range(numberOfKnobs):
            self.KnobList[i] = Knob(self.KnobList[i].name, self.KnobList[i].mode, self.KnobList[i].channel, i+offset)
    
    def printKnobMap(self):
        for i in range(numberOfKnobs):
             self.KnobList[i].printKnob()

###########################################
#############    PADS   ##################
###########################################

# number of pad-type controls 
numberOfPads = 16

class Pad:

    def __init__(self, name="Generic Pad", mode=modeControlAbs, chn=MIDI_SELECTED_CHANNEL, CCV=1):
        self.setName(name)
        self.setMode(mode)
        self.setChannel(chn)
        self.setCC(CCV)
        

    def setName(self, name):
        self.name = name

    def setMode(self, mod):
        self.mode = mod

    def setChannel(self, chn):
        self.channel = chn

    def setCC(self, CCV):
        self.CC = CCV

    def printPad(self):
        print(self.name)
        self.mode.printMode()
        print("Channel : ", self.channel, ", CC : ", self.CC)


PadNames=[]
for i in range(8):
    PadNames.append("P"+str(i+1))
for i in range(8):
    PadNames.append("P"+str(i+9))

class PadMap:
    def __init__(self):
        self.PadList = []
        for i in range(numberOfPads):
            name = PadNames[i]
            self.PadList.append(Pad(name, modeControlAbs, MIDI_SELECTED_CHANNEL, i+numberOfKnobs+1))

    def offsetPadsCC(self, offset):
        for i in range(numberOfPads):
            self.PadList[i] = Pad(self.PadList[i].name, self.PadList[i].mode, self.PadList[i].channel, i+offset)

    def printPadMap(self):
        for i in range(numberOfPads):
            self.PadList[i].printPad()


# create transport knob and pad mapping
transportKnobs = KnobMap()
transportPads = PadMap()
transportPads.offsetPadsCC(numberOfKnobs)
transportKnobs.printKnobMap()
transportPads.printPadMap()


# create FPC knob and pad mapping and offset it
FPCKnobs = KnobMap()
FPCKnobs.offsetKnobsCC(numberOfKnobs+numberOfPads)
FPCPads = PadMap()
FPCPads.offsetPadsCC(2*(numberOfKnobs)+numberOfPads)
FPCKnobs.printKnobMap()
FPCPads.printPadMap()

# create Keyboard knob and pad mapping and offset it
KeyboardKnobs = KnobMap()
KeyboardKnobs.offsetKnobsCC(2*(numberOfKnobs+numberOfPads))
KeyboardPads = PadMap()
KeyboardPads.offsetPadsCC(3*numberOfKnobs+2*numberOfPads)
KeyboardKnobs.printKnobMap()
KeyboardPads.printPadMap()
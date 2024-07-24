
## Keyboard Channel
KB_CHN = 2

###########################################
#############    MODES   #############
###########################################
MODE_CONTROL = 0
MODE_SWITCHEDCONTROL = 1
MODE_PITCHBEND = 2
MODE_MIDINOTE = 3
MODE_DEFAULT = 4  # DEFAULT MODE IS CONTROL ABS

#############    CONTROL MODE OPTIONS   #############
OPTION_CONTROL_ABS = 0
OPTION_CONTROL_REL1 = 1
OPTION_CONTROL_REL2 = 2
OPTION_CONTROL_REL3 = 3

#############    SWITCHED CONTROL MODE OPTIONS   #############
OPTION_SWITCHEDCONTROL_TOGGLE = 0
OPTION_SWITCHEDCONTROL_GATE = 1

##### Mode class with mode type, option and values
class Mode:
    def __init__(self, modeType=MODE_CONTROL, opt=OPTION_CONTROL_ABS, minV=0, maxV=127):
        self.setModeType(modeType)
        self.setOption(opt)
        self.setMinMax(minV, maxV)

    def setModeType(self, modType):
        self.modeType = modType

    def setOption(self, opt):
        self.option = opt

    def setChn(self, chn):
        self.channel = chn

    def setMinMax(self, minV, maxV):
        self.minVal = minV
        self.maxVal = maxV
    
    def printMode(self):
        print("Mode Control : ", self.modeType, ", Option : ", self.option, ", MIN/MAX : ", self.minVal, "/", self.maxVal)

#### Some classic control modes
modeControlAbs = Mode()
modeControlRel2 = Mode(MODE_CONTROL, OPTION_CONTROL_ABS, 0, 127)
modeSwitchedGate = Mode(MODE_SWITCHEDCONTROL, OPTION_SWITCHEDCONTROL_GATE, 0, 1)
modeSwitchedGate = Mode(MODE_SWITCHEDCONTROL, OPTION_SWITCHEDCONTROL_TOGGLE, 0, 1)

###########################################
#############    KNOBS   ##################
###########################################

# number of knob-type controls 
numberOfKnobs = 19

class Knob:

    def __init__(self, name, mode=modeControlAbs, chn=KB_CHN, CCV=1):
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
        for i in range(numberOfKnobs+1):
            name = KnobNames[i]
            self.KnobList.append(Knob(name, modeControlAbs, KB_CHN, i))

    def offsetKnobsCC(self, offset):
        for i in range(numberOfKnobs+1):
            self.KnobList[i] = Knob(self.KnobList[i].name, self.KnobList[i].mode, self.KnobList[i].channel, i+offset)
    
    def printKnobMap(self):
        for i in range(numberOfKnobs+1):
             self.KnobList[i].printKnob()

###########################################
#############    PADS   ##################
###########################################

# number of pad-type controls 
numberOfPads = 16

class Pad:

    def __init__(self, name="Generic Pad", mode=modeControlAbs, chn=KB_CHN, CCV=1):
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
            self.PadList.append(Pad(name, modeControlAbs, KB_CHN, i+numberOfKnobs+1))

    def offsetPadsCC(self, offset):
        for i in range(numberOfPads):
            self.PadList[i] = Pad(self.PadList[i].name, self.PadList[i].mode, self.PadList[i].channel, i+offset)

    def printPadMap(self):
        for i in range(numberOfPads):
            self.PadList[i].printPad()


# create transport knob and pad mapping
transportKnobs = KnobMap()
transportPads = PadMap()

# create FPC knob and pad mapping and offset it
FPCKnobs = KnobMap()
FPCKnobs.offsetKnobsCC(1+numberOfKnobs+numberOfPads)
FPCPads = PadMap()
FPCPads.offsetPadsCC(2*(1+numberOfKnobs)+numberOfPads)

# create Keyboard knob and pad mapping and offset it
KeyboardKnobs = KnobMap()
KeyboardKnobs.offsetKnobsCC(2*(1+numberOfKnobs+numberOfPads))
KeyboardPads = PadMap()
KeyboardPads.offsetPadsCC(3*(1+numberOfKnobs)+2*numberOfPads)
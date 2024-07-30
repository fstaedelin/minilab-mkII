### Minimal list of control types:
# MMC / SYSEX
# CONTROL->SWITCH->TOGGLE
# CONTROL->ABSOLUTE
# CONTROL->RELATIVE
# PITCHBEND
# MIDI ON/OFF(/AFTERTOUCH)


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

##### Mode class with mode type, option and values
class Mode:
    def __init__(self, modeType=MODE_CONTROL_ABSOLUTE, minV=0, maxV=127):
        self.setModeType(modeType)
        self.setMinMax(minV, maxV)

    def setModeType(self, modType):
        self.modeType = modType

    def setChn(self, chn):
        self.channel = chn

    def setMinMax(self, minV, maxV):
        self.minVal = minV
        self.maxVal = maxV
    
    def printMode(self):
        print("Mode Control : ", self.modeType, ", MIN/MAX : ", self.minVal, "/", self.maxVal)
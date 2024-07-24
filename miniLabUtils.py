# MATH
def rescale(min, max, value):
	targetSize=max-min
	value=value*targetSize/127.
	return value+min

# PRINT EVENT
def printEvent(event):
	print("INCOMING EVENT :")
	print("MIDIID : ", event.midiId, "PORT : ", event.port, "PROGNUM : ", event.progNum, "CONTROLNUM : ", event.controlNum)
	print("SYSEX : ", event.sysex, "DATA 1 : ", event.data1, "DATA 2 : ", event.data2)
	print("-----------------------")
	return 0

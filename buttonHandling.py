# BUTTONS SETUPS
import ui
import channels as chn

def Relative_Knob_2(event, func1, func2):
	event.handled = True
	if event.data2 > 120:
		func1()
	elif event.data2 > 0:
		func2()

def Relative_Knob_2_val(event, func, val1, val2):
	event.handled = True
	if event.data2 > 120:
		func(val1)
	elif event.data2 > 0:
		func(val2)

def PressButton(event, func):
	event.handled = True
	func()

def PressButtonVal(event, func, val):
	event.handled = True
	func(val)

def PressButtonVal(event, func, val):
	event.handled = True
	func(val)

def showAndKnob(event, window, func, val):
	chnIdx = chn.selectedChannel()
	event.handled = True
	ui.setFocused(window)
	func(chnIdx, val)
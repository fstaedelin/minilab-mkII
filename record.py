import mixer as mxr
import playlist as pys
import transport as tnp

import mapping as midiConst
import FelixTemplate as idx

###### Record ARM/UNARM tools for instruments
def unArm(trk):
	if mxr.isTrackArmed(trk):
		mxr.armTrack(trk)

def forceArm(trk):
	if ~mxr.isTrackArmed(trk):
		mxr.armTrack(trk)

def unArmRecord(recordEntry):
	if recordEntry == midiConst.record_FPC:
		for trk in idx.FPC_trk: unArm(trk)
	elif recordEntry == midiConst.record_bass:
		unArm(idx.bass_trk)
	elif recordEntry == midiConst.record_sax:
		unArm(idx.sax_trk)
	elif recordEntry == midiConst.record_vocals:
		unArm(idx.vocals_trk)
	elif recordEntry == midiConst.record_in_4:
		unArm(idx.in_4_trk)
	elif recordEntry == midiConst.record_in_5:
		unArm(idx.in_5_trk)

def forceArmRecord(recordEntry):
	if recordEntry == midiConst.record_FPC:
		for trk in idx.FPC_trk: forceArm(trk)
	elif recordEntry == midiConst.record_bass:
		forceArm(idx.bass_trk)
	elif recordEntry == midiConst.record_sax:
		forceArm(idx.sax_trk)
	elif recordEntry == midiConst.record_vocals:
		forceArm(idx.vocals_trk)
	elif recordEntry == midiConst.record_in_4:
		forceArm(idx.in_4_trk)
	elif recordEntry == midiConst.record_in_5:
		forceArm(idx.in_5_trk)
				

def armOnly(recordEntry):
	for rec in midiConst.record_All:
		if rec == recordEntry:
			forceArmRecord(rec)
		else:
			unArmRecord(rec)

####### MIDI instruments

def forceSongMode():
	if tnp.getLoopMode() == 0:
			tnp.setLoopMode()

def loopThroughKeyboards():
	print(tnp.isRecording())
	
	if tnp.isRecording() == 0:
		forceSongMode()
		tnp.record()

def recordMIDI(playlistEntry):
	# Selects adapted track
	pys.selectTrack(playlistEntry)
	# Puts into song mode
	if tnp.getLoopMode() == 0:
		tnp.setLoopMode()
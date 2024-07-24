def OldOnMidi(event):
	if event.midiId == midi.MIDI_CONTROLCHANGE:
		if event.data1 == mkIIMap.next_window: btn.PressButton(event, ui.nextWindow)
		if event.data1 == mkIIMap.mute_channel: btn.PressButtonVal(event, chn.muteChannel, chn.selectedChannel())
		elif event.data1 == mkIIMap.prev_next: btn.Relative_Knob_2(event, ui.previous, ui.next)
		elif event.data1 == mkIIMap.right_left: btn.Relative_Knob_2(event, ui.left, ui.right)
		elif event.data1 == mkIIMap.up_down: btn.Relative_Knob_2(event, ui.down, ui.up)
		elif event.data1 == mkIIMap.channel_master: btn.showAndKnob(event, flidx.wdChannelRack, chn.setChannelVolume, rescale(0.0, 1.0, event.data2))
		elif event.data1 == mkIIMap.channel_pan: btn.showAndKnob(event, flidx.wdChannelRack, chn.setChannelPan, rescale(-1.0, 1.0, event.data2))
		elif event.data1 == mkIIMap.record_bass: mxr.armTrack(flidx.bass_trk)
		elif event.data1 == mkIIMap.record_sax: mxr.armTrack(flidx.sax_trk)
		elif event.data1 == mkIIMap.record_vocals: mxr.armTrack(flidx.vocals_trk)
		elif event.data1 == mkIIMap.record_in_4: mxr.armTrack(flidx.in_4_trk)
		elif event.data1 == mkIIMap.record_in_5: mxr.armTrack(flidx.in_5_trk)
		elif event.data1 == mkIIMap.record_FPC: rec.recordMIDI(flidx.FPC_pys) ; print('Knob ', event.data1, 'turned. Value : ', event.data2)
		elif event.data1 == mkIIMap.record_mid_keys: rec.recordMIDI(flidx.Mid_Keys_pys) ; print('Knob ', event.data1, 'turned. Value : ', event.data2)
		elif event.data1 == mkIIMap.record_hi_keys: rec.recordMIDI(flidx.Hi_Keys_pys) ; print('Knob ', event.data1, 'turned. Value : ', event.data2)
		
		else: print('Knob ', event.data1, 'turned. Value : ', event.data2)

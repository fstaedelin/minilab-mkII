# This class is a dispatcher. It will send the MIDI event to the appropriate function

# MIDI event dispatcher transforms the MIDI event into a value through a transform function provided at construction
# time. This value is then used as a key into a lookup table that provides a dispatcher and filter function. If the
# filter function returns true, then the event is sent to the dispatcher function.

from utility.mappings.dictionaries import ControlModes
from utility.mappings.MiniLabMk2Mapping import MiniLabMapping

from utility.JARVIS import _JARVIS

class MidiEventDispatcher:


    def __init__(self, transform_fn):
        self._transform_fn = transform_fn
        # Table contains a mapping of status code -> (callback_fn, filter_fn)
        self._dispatch_map = {}


    def NewHandler(self, key, callback_fn, filter_fn =None):
        #This function will create a new link between a key and a function

        # param key: the result value of transform_fn(event) to match against.
        # param callback_fn: function that is called with the event in the event the transformed event matches.
        # param filter_fn: function that takes an event and returns true if the event should be dispatched. If false
        # is returned, then the event is dropped and never passed to callback_fn. Not specifying means that callback_fn
        # is always called if transform_fn matches the key.

        
        def _default_true_fn(_): return True
        if filter_fn is None:
            filter_fn = _default_true_fn
        self._dispatch_map[key] = (callback_fn, filter_fn)
        return self


    def NewHandlerForKeys(self, keys, callback_fn, filter_fn=None):
        # Same function but for a group of controls
        
        for k in keys:
            self.NewHandler(k, callback_fn, filter_fn=filter_fn)
        return self
    
    def NewCCHandlersFromMapping(self, mapping: MiniLabMapping, filter_fn=None):
        # Same function but linking pads
        for controller in mapping._controls() :
            if controller.controlMode in ControlModes['CC']:
                _JARVIS.Debug(f"Creating CC handle for {str(controller.name)}")
                _JARVIS.Navigate(controller.name)
                _JARVIS.Debug(f"Control Mode: {str(controller.controlMode)}")
                _JARVIS.Debug(f"Assigned to key: {str(controller.controlData1)}")
                _JARVIS.Navigate("parent")
                self.NewHandler(controller.controlData1, controller.callback_fn, filter_fn)
        return self
    
    def NewSYSEXHandlersFromMapping(self, mapping:MiniLabMapping):
        for controller in mapping.pads:
            if controller.controlMode == ControlModes['SYSEX']:
                self.NewHandler(controller.control_data, controller.callback_fn)
        return self
    

    def Dispatch(self, event):
        # This function will dispatch the event
        key = self._transform_fn(event)
        processed = False
        if key in self._dispatch_map:
            callback_fn, filter_fn = self._dispatch_map[key]
            if filter_fn(event):
                callback_fn(event)
                processed = True
        else:
            _JARVIS.Warning("Unassigned key")
        return processed
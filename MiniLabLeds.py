import device
from mapping.dictionaries import MATRIX_IDS_PAD

from utility.lightcommands import send_to_device, SET_COLOR_COMMAND 
# MIT License
# Copyright (c) 2020 Ray Juang

# This class organize the LED functions usefull for visual returns.
# The class sets up a LED map depending on the controller

class MiniLabmk2Led:

    def SetPadLights(self, matrix_values):
        """ Set the pad lights given a matrix of color values to set the pad with.
        :param matrix_values: 8x2 array of arrays containing the LED color values.
        """
        led_map = {}
        for r in range(2):
            for c in range(8):
                led_map[MATRIX_IDS_PAD[r][c]] = matrix_values[r][c]
        self.SetLights(led_map)
    
    def SetAllPadLights(self, color):
        """ Set the pad lights given a matrix of color values to set the pad with.
        :param matrix_values: 8x2 array of arrays containing the LED color values.
        """
        led_map = {}
        for r in range(2):
            for c in range(8):
                led_map[MATRIX_IDS_PAD[r][c]] = color
        self.SetLights(led_map)

    
    def SetLights(self, led_mapping):
        """ Given a map of LED ids to color value, construct and send a command with all the led mapping.
        :param led_mapping: table of ID_PAD | color
        """
        
        data = bytes([])
        for led_id, led_value in led_mapping.items():
            data += bytes([led_id, led_value])
            send_to_device(SET_COLOR_COMMAND + data)
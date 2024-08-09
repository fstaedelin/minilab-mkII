from GPT_minimal_clean import Logger
global logger
logger = Logger("INFO")

class Event:
    def __init__(self, event_id):
        self.id = event_id
        self.handled = False

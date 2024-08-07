from logger_3 import Logger
# Define Event class for better structure
class Event:
    def __init__(self, event_id):
        self.id = event_id
        self.handled = False

# Function to test if it works OK when nested:
def FirstEventHandler(event):
    if event.handled:
        logger.debug("Event handled before FirstEventHandler")
    else:
        if event.id > 200:
            event.handled = True
        addEventCheck(event, "Event handled by FirstEventHandler", "Event not handled by FirstEventHandler")


def SecondEventHandler(event):
    if event.handled:
        logger.debug("Event handled before FirstEventHandler")
    else:
        if event.id < 100:
            event.handled = True
        addEventCheck(event, "Event handled by SecondEventHandler", "Event not handled by SecondEventHandler")

def addEventCheck(event, okmessage, warningMessage):
    #print("   Enter addEventCheck")
    logger.add_test(
        val=event,
        test_fn=lambda event: event.handled,
        result_key=True,
        callback_true=lambda: logger.log(okmessage, "SUCCESS"),
        callback_false=lambda: logger.log(warningMessage, "WARNING")
    )
    #print("   Exit addEventCheck")
    
def addFinalCheck(event):
    logger.add_test(
        val=event,
        test_fn=lambda event: event.handled,
        result_key=True,
        callback_true=lambda: logger.log("Event was handled", "SUCCESS"),
        callback_false=lambda: logger.log("NOT HANDLED :( ", "ERROR")
    )
    

# Usage example:
logger = Logger()
logger.set_levels("WARNING")


# Setting initial context and logging messages
logger.debug("Initializing")
logger.set_context(-1)
logger.debug("Doing some stuff")

# Create an event
event1 = Event(130)

# Create a nested context
logger.set_context(-1)
FirstEventHandler(event1)
logger.set_context(+1)
logger.debug("Doing some more stuff")
logger.set_context(-1)
SecondEventHandler(event1)

# Move back to the parent context
logger.set_context(+1)

addFinalCheck(event1)
# Run tests

logger.set_context(+1)
#logger.draw_tree()
# Trigger a warning which will print all debug and warning messages for the context and nested ones
#logger.trigger_warning("Testing warning mechanism.")
	

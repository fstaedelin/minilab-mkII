from logger3 import Logger

# Usage example:
logger = Logger()
logger.set_levels("DEBUG")

class Event:
    def __init__(self, event_id):
        self.id = event_id
        self.handled = False

def FirstEventHandler(event):
    if event.handled:
        logger.debug("Event handled before FirstEventHandler")
    else:
        if event.id > 200:
            event.handled = True
        addEventCheck(event, "Event handled by FirstEventHandler", "Event not handled by FirstEventHandler")

def SecondEventHandler(event):
    if event.handled:
        logger.debug("Event handled before SecondEventHandler")
    else:
        if event.id < 100:
            event.handled = True
        addEventCheck(event, "Event handled by SecondEventHandler", "Event not handled by SecondEventHandler")

def addEventCheck(event, okmessage, warningMessage):
    logger.add_test(
        val=event,
        test_fn=lambda event: event.handled,
        result_key=True,
        callback_true=lambda: logger.log(okmessage, "SUCCESS"),
        callback_false=lambda: logger.log(warningMessage, "WARNING")
    )

def addFinalCheck(event):
    logger.add_test(
        val=event,
        test_fn=lambda event: event.handled,
        result_key=True,
        callback_true=lambda: logger.log("Event was handled", "SUCCESS"),
        callback_false=testfunc,
        triggered=True
    )

def testfunc():
    logger.trigger("NOT HANDLED :( ", "ERROR")
    context = logger.get_current_context()
    #print(context)


event1 = Event(69)



logger.debug("Initializing")
logger.set_context(-1)
logger.debug("Doing some stuff")
logger.set_context(-1)
FirstEventHandler(event1)
logger.set_context(1)
logger.debug("Doing some more stuff")

logger.set_context(-1)
SecondEventHandler(event1)

logger.set_context(-1)

logger.add_test(
    val=event1,
    test_fn=lambda event: event.id,
    result_key=69,
    callback_true=lambda: logger.trigger("69 hehehe", "ERROR"),
    callback_false=lambda: logger.debug("not 69 :("),
    triggered=True,
)

logger.set_context(1)

logger.set_context(1)

addFinalCheck(event1)
logger.set_context(1)

#logger.draw_tree()
from logger_func import *

logger._print("GOING TO INITIALIZATION")
logger.Navigate("INIT")
logger._print_contexts()
logger._print("LOGGING")
logger.log("Initializing ...", "DEBUG")
logger._print_contexts()


logger._print("GOING TO ROOT")
logger.Navigate("parent")
logger._print_contexts()
##### Trying to creat a new level

logger._print("GOING TO PROCESING")
logger.Navigate("PROCESSING")
logger._print_contexts()

logger._print("CREATING DEBUG EVENT")
logger.log("processing ...", "DEBUG")

## UNTIL HERE ALL IS GOOD
logger._print("GOING TO PROCESSING1")
logger.Navigate("PROCESSING1")
logger.warning("Not like this !")


#
logger._print("GOING TO PROCESING2")
logger.Navigate("parent")
logger.Navigate("PROCESSING2")
logger.error("Even worse....")
logger._print_contexts()
#logger.Navigate("parent")
#
#
#logger._print_contexts()
#

#logger.Navigate("parent")


#logger.set_context(-1)
#logger.debug("Doing some stuff")
#
#event1 = Event(69)
#
#logger.set_context(-1)
#FirstEventHandler(event1)
#logger.set_context(1)
#logger.debug("Doing some more stuff")
#
#logger.set_context(-1)
#SecondEventHandler(event1)
#
#logger.set_context(-1)
#
#logger.add_test(
#    val=event1,
#    test_fn=lambda event: event.id,
#    result_key=69,
#    callback_true=lambda: logger.trigger("69 hehehe", "ERROR"),
#    callback_false=lambda: logger.debug("not 69 :("),
#    triggered=True,
#)
#
#logger.set_context(1)
#
#logger.set_context(1)
#
#addFinalCheck(event1)
#logger.set_context(1)
#
#logger.draw_tree()
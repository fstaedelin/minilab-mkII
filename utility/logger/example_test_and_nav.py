from logger_func2 import *

event1 = Event(230, False)

logger.debug("GOING TO INITIALIZATION")
logger.Navigate("INIT")
logger.debug("Initializing ...")
#logger._print_contexts()
event1 = Event(125, False)
logger.debug("ADDING AND TRIGGERING HANDLING TESTS")
test_handled = logger.add_test(
    test_fn=lambda x: x,
    name = "Event handled"
)
logger.trigger(test_handled, event1.handled)

logger.Navigate("parent")

logger.Navigate("Processor")
logger.debug("ADDING ID_TESTS")
## Need to initiate and trigger tests in same context for now

ID_SUP_100 = logger.add_test(
    test_fn=is_more_100["test_fn"],
    name = "Event id >100"
)
ID_SUP_150 = logger.add_test(
    test_fn=is_more_150["test_fn"],
    name = "Event id >150"    
)

logger.debug("TRIGGERING ID_TESTS")
logger.trigger(ID_SUP_100, event1.id)
logger.trigger(ID_SUP_150, event1.id)


logger.Navigate("Parent")

logger.debug("NAVIGATING TO PROCESSOR")

logger.warning("event changed !!")

event1 = Event(1110, False)


logger.Navigate("parent")

### debug
logger.debug("TRIGGERING ID_TESTS again")
logger.trigger(ID_SUP_100, event1.id)
logger.trigger(ID_SUP_150, event1.id)


logger.Navigate("mapping")
logger.Navigate("testing")
event1.handled = True

logger.Navigate("parent")
logger.Navigate("parent")

logger.trigger(test_handled, event1.handled)

logger.draw_tree()

print("------------------------------")
logger._write_log()
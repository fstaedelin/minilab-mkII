from logger_func import *

event1 = Event(230)

logger.debug("GOING TO INITIALIZATION")
logger.Navigate("INIT")


logger.debug("INITIALIZING")
logger.debug("Initializing ...")
#logger._print_contexts()
event1 = Event(200)

logger.debug("ADDING ID_TESTS")
#logger._print_contexts()
is_more_100 = logger.add_test(
    test_fn=lambda x: True if x > 100 else False,
    result_key=True,
    callback_false=logger.test_callback(
        message = "ID is lower than 100",
        level = "WARNING",
        passed = False,
        name = ">100"),
    callback_true=logger.test_callback(
        message = "ID is Higher than 100",
        level = "SUCCESS",
        passed = True,
        name = ">100")
)
#logger._print_contexts()
is_more_150 = logger.add_test(
    test_fn=lambda x: True if x > 150 else False,
    result_key=True,
    callback_true=logger.test_callback(
        message = "ID is more than 150",
        level = "SUCCESS",
        passed = True,
        name = ">150"),
    callback_false=logger.test_callback(
        message = "ID is less than 150 !",
        level = "WARNING",
        passed = False,
        name = ">150"),
)



logger._print("TRIGGERING ID_TESTS")
logger.trigger(is_more_100, event1.id)
logger.trigger(is_more_150, event1.id)


event1 = Event(10)
logger.trigger(is_more_100, event1.id)
logger.trigger(is_more_150, event1.id)
logger.draw_tree()
#logger.draw_tree()
logger.Navigate("parent")

#logger._print_contexts()


#logger.Navigate(1)
#logger.debug("Doing some more stuff")
#
#logger.Navigate(-1)
#SecondEventHandler(event1)
#
#logger.Navigate(-1)
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
#logger.Navigate(1)
#
#logger.Navigate(1)
#
#addFinalCheck(event1)
#logger.Navigate(1)
#
#logger.draw_tree()
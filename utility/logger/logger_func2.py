from GPT_minimal_clean import Logger
global logger
logger = Logger("INFO")

class Event:
    def __init__(self, event_id, handled):
        self.id = event_id
        self.handled = False

is_more_100 = logger.add_test(
    test_fn=lambda x: True if x > 100 else False,
    name = ">100")

#logger._print_contexts()
is_more_150 = logger.add_test(
    test_fn=lambda x: True if x > 150 else False,
    name = ">150"
)
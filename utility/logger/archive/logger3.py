class Logger:
    def __init__(self, level="WARNING"):
        self.level = level  # Set the default logging level
        self.levels = {"TRIGGABLE": 5, "SUCCESS": 0, "DEBUG": 10, "WARNING": 20, "ERROR": 30}  # Define logging levels with priorities
        self.current_context = ["root"]  # Track the current context path as a list
        self.contexts = {"root": {"children": {}, "TESTS": {}}}  # Initialize the root context
        self._set_new_context()  # Set up the initial context
        self.active_contexts = set()  # Track active contexts
        self.triggered = False  # Track if a warning has been triggered
        self.trigger_level = self.levels["TRIGGABLE"]  # Set the trigger level
        self.err_lvl = self.levels["DEBUG"]
        self.active_contexts = self.get_current_context()
    
    def _autoname(self, name="children"):
        RESERVED = ["children", "TESTS"] + list(self.levels.keys())
        if name in RESERVED:
            return f"{name}_{len(self.current_context)}"
        return name

    def _set_new_context(self, name="children", parent="children"):
        if self.contexts == {"root": {"children": {}, "TESTS": {}}}:
            for key in self.levels:
                self.contexts["root"][key] = {}
        #print(self.get_current_context())
        new_context_name = self._autoname(name)
        new_context = {key: {} for key in list(self.levels.keys())}
        new_context["children"] = {}
        new_context["TESTS"] = {}
        current_context = self.get_current_context()
        current_context["children"][new_context_name] = new_context

    def set_levels(self, level, trigger_lvl="TRIGGABLE"):
        if level in self.levels:
            self.level = level  # Update the logging level if it's valid
        else:
            raise ValueError("Invalid log level")  # Raise an error for invalid levels
        if trigger_lvl in self.levels:
            self.trigger_level = trigger_lvl  # Update the trigger level if it's valid
        else:
            raise ValueError("Invalid log level")  # Raise an error for invalid levels

    def get_current_context(self):
        context = self.contexts["root"]
        for part in self.current_context[1:]:
            context = context["children"].get(part, context)
        return context

    def set_context(self, direction=0, name="children"):
        if direction == 1:
            # Move to the parent context
            if len(self.current_context) > 1:
                self.current_context.pop()
        elif direction == -1:
            # Create a new nested context and move into it
            if name not in self.get_current_context()["children"]:
                self._set_new_context(name)
            self.current_context.append(name)
        else:
            raise ValueError("Invalid context direction. Use +1 for parent and -1 for nested context.")

    def log(self, message, level):
        context = self.get_current_context()
        formatted_message = self._format_message(level, message)
        if level in context:
            context[level][formatted_message] = True
            if self.levels[level] >= self.levels[self.trigger_level]:
                context["TRIGGABLE"][formatted_message] = True
            #if self.levels[level] >= self.levels[self.level]:
                #print(formatted_message)
        return formatted_message

    def debug(self, message):
        self.log(message, "DEBUG")  # Log a debug message

    def success(self, message):
        self.log(message, "SUCCESS")  # Log a success message

    def warning(self, message):
        self.log(message, "WARNING")  # Log a warning message

    def error(self, message):
        self.log(message, "ERROR")  # Log an error message

    def add_test(self, val, test_fn, result_key, callback_true, callback_false, triggered=False):
        context = self.get_current_context()
        newTest = {
            "val": val,
            "test_fn": test_fn,
            "result_key": result_key,
            "callback_true": callback_true,
            "callback_false": callback_false,
        }
        test_name = self._autoname("test")
        context["TESTS"][test_name] = newTest
        if triggered:
            self._run_trigd_test(newTest)
        else:
            self._force_run_test(newTest)

    def _force_run_test(self, test):
        result = test["test_fn"](test["val"])
        if result == test["result_key"]:
            test["callback_true"]()
            return True
        else:
            test["callback_false"]()
            return False

    def _run_trigd_test(self, test):
        
        if "triggered" in test:
            result = test["test_fn"](test["val"])
            if result == test["result_key"]:
                test["callback_true"]()
            else:
                test["callback_false"]()
            test["triggered"] = True

    def trigger(self, message, level):
        print("trigger")
        self.triggering_event_message = self.log(message, level)
        self.scan_next(self.current_context.copy(), self.contexts["root"])

    def scan_next(self, context_path, context):
        if "TESTS" in context and context["TESTS"]:
            for test in context["TESTS"].values():
                self._run_trigd_test(test)
        if context_path:
            next_destination = context_path.pop(0)
            if next_destination in context["children"]:
                self.scan_next(context_path, context["children"][next_destination])

    def draw_tree(self):
        def draw_context_tree(context, indent=""):
            for level in ["SUCCESS", "DEBUG", "WARNING", "ERROR"]:
                if context[level]:
                    for message in context[level]:
                        print(f"{indent}{message}")
            for child_name, child_context in context["children"].items():
                draw_context_tree(child_context, indent + "    ")

        draw_context_tree(self.contexts["root"], "    ")

    def _format_message(self, level, message):
        indent = '|   ' * (len(self.current_context) - 1) if level != "SUCCESS" else ""
        flag = {
            "DEBUG": '|-->',
            "ERROR": "|/!\\",
            "WARNING": "|/!\\",
            "SUCCESS": 'C' + '====' * (len(self.current_context) - 1) + "==3"
        }.get(level, '')
        lvl = {
            "DEBUG": "DBG|",
            "ERROR": "|/!\\",
            "WARNING": "WNG!",
            "SUCCESS": ":O  "
        }.get(level, '')
        return f"{lvl}{indent}{flag}|{message}"
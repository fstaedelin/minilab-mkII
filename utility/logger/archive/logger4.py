class Logger:
    def __init__(self, level="WARNING", trigger_level = "TRIGGABLE"):
        self.print_lvl = -1
        self._printIn("__init__")
        self.level = level  # Set the default logging level
        self.trigger_level = trigger_level  # Set the trigger level
        
        self.log_levels = {"TRIGGABLE": 5, "SUCCESS": 0, "DEBUG": 10, "WARNING": 20, "ERROR": 30}  # Define logging levels with priorities
        
        self.current_context = {"root":{}}  # Track the current context path as a list
        self.contexts = {"root":{}}  # Initialize the root context
        self._set_new_context()  # Set up the initial context
        self.active_contexts = set()  # Track active contexts
        self.triggered = False  # Track if a warning has been triggered
        self._printOut("__init__")

    def _autoname(self, name="children"):
        self._printIn("_autoname")
        RESERVED = ["children"]
        for lvl in self.log_levels:
            RESERVED.append(lvl)
        
        if name in self.current_context:
            name = f"{name}_{len(self.current_context[name]) + 1}"
        
        self._printOut("_autoname")
        return name

    def _set_new_context(self, name="children", parent=None):
        self._printIn("_set_new_context")
        current_context = self.contexts
        for part in self.current_context:
            current_context = current_context[part]

        if name not in current_context:
            current_context[name] = {}
        if parent:
            current_context[name][parent] = {}
        
        self.current_context[name] = current_context[name]
        self._printOut("_set_new_context")

    def set_levels(self, level, trigger_lvl="TRIGGABLE"):
        self._printIn("set_levels")
        if level in self.log_levels:
            self.level = level
        else:
            raise ValueError("Invalid log level")  # Raise an error for invalid levels
        if trigger_lvl in self.log_levels:
            self.trigger_level = trigger_lvl  # Update the trigger level if it's valid
        else:
            raise ValueError("Invalid log level")  # Raise an error for invalid levels
        self._printOut("set_levels")

    def get_current_context(self):
        self._printIn("get_current_context")
        context = self.contexts["root"]
        print(self.current_context)
        for part in self.current_context:
            context = context.get(part, context)
        print("get_current_context: ", context)
        self._printOut("get_current_context")
        return context

    def set_context(self, direction=0, name="children"):
        self._printIn("set_context")
        if direction == +1:
            if len(self.current_context) > 1:
                self.current_context.pop()
        elif direction == -1:
            if name not in self.current_context:
                self._set_new_context(name)
            else:
                self.current_context = self.current_context[name]
        else:
            raise ValueError("Invalid context direction. Use +1 for parent and -1 for nested context.")
        self._printOut("set_context")

    def log(self, message, level):
        self._printIn("log")
        context = self.get_current_context()
        formatted_message = self._format_message(level, message)
        if level not in context:
            self._set_new_context(level)
        if level in context and formatted_message not in context[level]:
            context[level] = formatted_message
            if self.log_levels[level] >= self.log_levels[self.trigger_level]:
                context["TRIGGABLE"] = (formatted_message)
            if self.log_levels[level] >= self.log_levels[self.level]:
                print("printing ", level)
                print(formatted_message)
        self._printOut("log")
        return formatted_message

    def debug(self, message):
        self._printIn("debug")
        self.log(message, "DEBUG")
        self._printOut("debug")

    def success(self, message):
        self._printIn("success")
        self.log(message, "SUCCESS")
        self._printOut("success")

    def warning(self, message):
        self._printIn("warning")
        self.log(message, "WARNING")
        self._printOut("warning")

    def error(self, message):
        self._printIn("error")
        self.log(message, "ERROR")
        self._printOut("error")

    def add_test(self, val, test_fn, result_key, callback_true, callback_false, triggered=False):
        self._printIn("add_test")
        context = self.get_current_context()
        newTest = {
            "val": val,
            "test_fn": test_fn,
            "result_key": result_key,
            "callback_true": callback_true,
            "callback_false": callback_false,
        }
        
        context["TESTS"][self._autoname("test")] = (newTest)
        
        if triggered:
            newTest["triggered"] = True
            self._run_trigd_test(context["TESTS"])
        else:
            self._force_run_test(context["TESTS"])
        self._printOut("add_test")

    def _force_run_test(self, test):
        self._printIn("_force_run_test")
        result = test["test_fn"](test["val"])
        if result == test["result_key"]:
            test["callback_true"]()
        else:
            test["callback_false"]()
        self._printOut("_force_run_test")
        return result

    def _run_trigd_test(self, test):
        self._printIn("_run_trigd_test")
        if "triggered" in test:
            result = test["test_fn"](test["val"])
            if result == test["result_key"]:
                test["callback_true"]()
            else:
                test["callback_false"]()
            test["triggered"] = True
        self._printOut("_run_trigd_test")

    def trigger(self, message, level):
        self._printIn("trigger")
        context = self.get_current_context()
        self.triggering_event_message = self.log(message, level)
        deep_context = context["TESTS"]
        self._printOut("trigger")

    def find_parent_keys(self, d, target_key, parent_key=None):
        self._printIn("find_parent_keys")
        for k, v in d.items():
            if k == target_key:
                if isinstance(v, list):
                    self.find_parent_keys(d, "TESTS", k)
                else:
                    yield parent_key
            if isinstance(v, dict):
                for res in self.find_parent_keys(v, target_key, k):
                    yield res
        self._printOut("find_parent_keys")

    def find_triggering_path(self):
        self._printIn("find_triggering_path")
        context = self.get_current_context
        result = self.find_parent_keys(context)
        self._printOut("find_triggering_path")
        return result

    def scan_next(self, context_path, context):  
        self._printIn("scan_next")
        i = 0
        while context_path and i < 100:
            i += 1
            next_destination = context_path[0]
            if "TESTS" in context and context["TESTS"]:
                for test in context["TESTS"]:
                    self._force_run_test(test)
            if "children" in context and next_destination in context["children"]:
                context = context["children"]
                if len(context_path) != 0:
                    context_path.pop(0)
                    self.scan_next(context_path, context)
            if next_destination in context:
                context = context[next_destination]
                if len(context_path) != 0:
                    context_path.pop(0)
                    self.scan_next(context_path, context)
        self._printOut("scan_next")

    def _rerun_parent_tests(self):
        self._printIn("_rerun_parent_tests")
        context_path = self.current_context.copy()
        context_path.pop(0)
        i = -1
        context = self.contexts["root"]["children"]
        while context_path and i < 100:
            i += 1
            for next_destination in context_path:
                if next_destination in context:
                    if "TESTS" in context and context["TESTS"]:
                        for test in context["TESTS"]:
                            self._force_run_test(test)
                    if context[next_destination]["TESTS"]:
                        context = context[next_destination]
                        context_path.pop(0)
                    else:
                        context = context[context_path[1]]
                        context_path.pop(0)
        self._printOut("_rerun_parent_tests")

    def draw_tree(self):
        self._printIn("draw_tree")
        def draw_context_tree(context, indent=""):
            for level in ["SUCCESS", "DEBUG", "WARNING", "ERROR"]:
                #if self.levels[level] >= self.err_lvl:
                    if context[level]:
                        for message in context[level]:
                                print(message)
            for child_name, child_context in context["children"].items():
                draw_context_tree(child_context, indent + "    ")

        draw_context_tree(self.contexts["root"], "    ")
        self._printOut("draw_tree")

    def _format_message(self, level, message):
        self._printIn("_format_message")
        indent = '|   ' * (len(self.current_context) - 1) if level != "SUCCESS" else ""
        flag = {
            "DEBUG": '|-->',
            "ERROR": "|/!\\",
            "WARNING": "|/!\\",
            "SUCCESS": 'C' + '====' * (len(self.current_context) - 1) + "==3"
        }.get(level, '')
        lvl = {
            "DEBUG": "DBG|",
            "ERROR": "ERR|",
            "WARNING": "WRN|",
            "SUCCESS": "SCS|"
        }.get(level, '')
        formatted_message = f"{indent}{flag}{lvl} {message}"
        self._printOut("_format_message")
        return formatted_message
    
    def _printIn(self, fn_name):
        self.print_lvl+=1
        print(self.print_lvl*("  "), "In : ", fn_name)
    
    def _printOut(self, fn_name):
        print(self.print_lvl*("  "), "Out: ", fn_name)
        self.print_lvl-=1
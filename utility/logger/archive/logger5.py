class Logger:
    def __init__(self, level="WARNING"):
        self.print_lvl = -1
        #self._printIn("__init__")
        self.level = level  # Set the default logging level
        self.levels = {"INFO": 0, "DEBUG": 10, "WARNING": 20, "ERROR": 30}  # Define logging levels with priorities
        self.contexts = {}  # Initialize the root context
        self.current_context = {}  # Initialize an empty set which will be updated by _set_new_context
        self.current_path = []
        #self._print_contexts()
        #self._printOut("__init__")

    def _autoname(self, name="children", parent = ""):
        ##self._printIn("_autoname")
        # if there is no name, return empty string
        if name:
            context = self.get_current_context()
            if parent in context:
                self._print("parent in context")
                #self._print_contexts()
                context = context[parent]
                #self._print_contexts()
                if name in context:
                    name = f"{name}_{len(context[name]) + 1}"
            # if the parent is not in the context, 
            # nor the parent nor the child name will change !  
        ##self._printOut("_autoname")
        return name

    def _set_new_context(self, name="children", parent=None):
        #self._printIn("_set_new_context")
        name = self._autoname(name, parent)
        parent = self._autoname(parent)
                           
        if parent == None and self.current_path:
            self._print("No parent. Current path is ", self.current_path)
            
            # Start with the root dictionary
            context = self.contexts
            print(context)
            if len(self.current_path)>0:
                context[self.current_path[-1]][name] = {}
            else:
                context[name] = {}
            self.contexts.update(context)
            self._print_contexts()
            #self.current_context = self.get_current_context()
        elif parent == None:
            current_context = self.contexts.copy()
            current_context[name] = {}
            self.contexts.update(current_context)
            self.current_context = self.get_current_context()
            
        else:
            self._print("parents found")
            self.current_context[parent] = {name: {}}
            self.contexts[parent] = {name: {}}
        
        #update the whole contexts
        #self._print_contexts()
        #self._printOut("_set_new_context")

    def set_levels(self, level):
        #self._printIn("set_levels")
        if level in self.levels:
            self.level = level  # Update the logging level if it's valid
        else:
            raise ValueError("Invalid log level")  # Raise an error for invalid levels
        #self._printOut("set_levels")

    def get_current_context(self):
        context = self.contexts.copy()
        for part in self.current_path:
            context = context.get(part, context)
        return context

    def Navigate(self, destination="children"):
        #self._printIn("Navigate")
        #self._print("destination", destination)
        if destination == "parent":
            # Move to the parent context
            if len(self.current_path) > 0:
                self.current_path.pop()
                self.current_context = self.get_current_context()
            else:
                self._print(self.current_path)
                self._print(len(self.current_path))
                print("Cannot Navigate to parent, root has no parents")
        else:
            # If the destination doesn't exists
            if destination not in self.current_context:
                # Create a new nested context
                self._print("Creating destination", destination)
                self._set_new_context(destination)
            self.current_path.append(destination)
            self.current_context = self.current_context[destination]
            # Move to the existing child context
    
        #self._print_contexts()
        #self._printOut("Navigate")

    def log(self, message, level):
        #self._printIn("log")
        #self._print_contexts()
        # Set the new level context if inexistent:
        if level not in self.current_context:
            self._print("Level not there yet", level)
            self._print_contexts()
            self._set_new_context(level)

        # Go to the desired level, format and record message
        self._print("before navigating to ", level)
        self._print_contexts()
        self.Navigate(level)
        #self._print("Inside level")
        #self._print_contexts()
        msg_number = len(self.current_context)
        formatted_message = self._format_message(level, message)
        self.current_context[msg_number] = formatted_message
        #self._print_contexts()
        self.Navigate("parent")# Get back
            
        #self._printOut("log")
        return formatted_message

    def debug(self, message):
        #self._printIn("debug")
        self.log(message, "DEBUG")  # Log a debug message
        #self._printOut("debug")

    def warning(self, message):
        #self._printIn("warning")
        self.log(message, "WARNING")  # Log a warning message
        #self._printOut("warning")

    def error(self, message):
        #self._printIn("error")
        self.log(message, "ERROR")  # Log an error message
        #self._printOut("error")

    def add_test(self, val, test_fn, result_key, callback_true, callback_false, triggered=False):
        #self._printIn("add_test")
        context = self.get_current_context()
        
        newTest = {
            "val": val,
            "test_fn": test_fn,
            "result_key": result_key,
            "callback_true": callback_true,
            "callback_false": callback_false,
        }
        
        context["TESTS"][self._autoname("test")] = newTest
        
        if triggered:
            newTest["triggered"] = True
            test = self._run_trigd_test(context["TESTS"])
        else:
            test = self._force_run_test(context["TESTS"])
        #self._printOut("add_test")
        

    def _force_run_test(self, test):
        #self._printIn("_force_run_test")
        result = test["test_fn"](test["val"])
        if result == test["result_key"]:
            test["callback_true"]()
            #self._printOut("_force_run_test")
            return True
        else:
            test["callback_false"]()
            #self._printOut("_force_run_test")
            return False

    def _run_trigd_test(self, test):
        #self._printIn("_run_trigd_test")
        if "triggered" in test:
            result = test["test_fn"](test["val"])
            if result == test["result_key"]:
                test["callback_true"]()
            else:
                test["callback_false"]()
            test["triggered"] = True
        #self._printOut("_run_trigd_test")

    def trigger(self, message, level):
        #self._printIn("trigger")
        self.triggering_event_message = self.log(message, level)
        print(self._format_message(level, "End of " + level.lower() + " message"))
        #self._printOut("trigger")
    
    def find_parent_keys(self, d, target_key, parent_key=None):
        #self._printIn("find_parent_keys")
        for k, v in d.items():
            if k == target_key:
                if isinstance(v, list):
                    self.find_parent_keys(d, "TESTS", k)
                else:
                    yield parent_key
            if isinstance(v, dict):
                for res in self.find_parent_keys(v, target_key, k):
                    yield res
        #self._printOut("find_parent_keys")

    def find_triggering_path(self):
        #self._printIn("find_triggering_path")
        context = self.get_current_context()
        return self.find_parent_keys(context, "triggered")
        #self._printOut("find_triggering_path")

    def scan_next(self, context_path, context):  
        #self._printIn("scan_next")
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
        #self._printOut("scan_next")

    def _rerun_parent_tests(self):
        #self._printIn("_rerun_parent_tests")
        context_path = self.current_context.copy()
        context_path.pop(0)
        i = 0
        context = self.contexts["root"]["children"]
        while context_path and i < 100:
            i += 1
            for next_destination in context_path:
                if next_destination in context:
                    if "TESTS" in context and context["TESTS"]:
                        for test in context["TESTS"]:
                            self._force_run_test(test)
                    context = context[next_destination]
                    context_path.pop(0)
                else:
                    context = context[context_path[1]]
                    context_path.pop(0)
        #self._printOut("_rerun_parent_tests")

    def draw_tree(self):
        #self._printIn("draw_tree")
        def draw_context_tree(context, indent=""):
            for level in ["DEBUG", "WARNING", "ERROR"]:
                if self.levels[level] >= self.err_lvl:
                    if level in context:
                        for message in context[level]:
                            print(message)

            for child_name, child_context in context["children"].items():
                draw_context_tree(child_context, indent + "    ")

        draw_context_tree(self.contexts["root"], "    ")
        #self._printOut("draw_tree")
        
    def _format_message(self, level, message):
        #self._printIn("_format_message")
        indent = '|   ' * (len(self.current_context) - 1)
        flag = {
            "DEBUG": '|-->',
            "ERROR": "|/!\\",
            "WARNING": "|/!\\",
        }.get(level, '')
        lvl = {
            "DEBUG": "DBG|",
            "ERROR": "|/!\\",
            "WARNING": "WNG!",
        }.get(level, '')
        formatted_message = f"{lvl}{indent}{flag}|{message}"
        #self._printOut("_format_message")
        return formatted_message
    
    def _printIn(self, fn_name):
        self.print_lvl+=1
        print(self.print_lvl*("  "), "In : ", fn_name)
    
    def _printOut(self, fn_name):
        print(self.print_lvl*("  "), "Out: ", fn_name)
        self.print_lvl-=1
    
    def _print(self, name, val=""):
        print((self.print_lvl+1)*("  "), name, ":  ", val)
    
    def _print_contexts(self):
        self._print("----------------------------------------------------------")
        self._print("self.contexts              ", self.contexts)
        self._print("self.current_path          ", self.current_path)
        self._print("self.current_context       ", self.current_context)
        self._print("self.get_current_context   ", self.get_current_context())
        self._print("----------------------------------------------------------")
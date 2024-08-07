class Logger:
    def __init__(self, level="WARNING"):
        self.level = level  # Set the default logging level
        self.levels = {"SUCCESS": 00, "DEBUG": 10, "WARNING": 20, "ERROR": 30}  # Define logging levels with priorities
        self.current_context = ["root"]  # Track the current context path as a list
        #self.contexts = {"root": {"DEBUG": [], "WARNING": [], "ERROR": [], "TESTS": [], "children": {}}}
        self.contexts = {"root": {"children": {}}}
        self._set_new_context()
        self.active_contexts = set()  # Track active contexts
        self.triggered = False
        self.trigger_level = level

    def _set_new_context(self):
        # Create a new nested context and move into it
        # get current context
        current_context = self.get_current_context()
        #print(current_context)
        # set new context name
        # if we are in root ...
        #print(list(self.levels.keys())[0])
        #for i in self.current_context:
        #    print(i)
        if list(self.levels.keys())[0] not in self.current_context:
            #print("Initializing root")
            for key in list(self.levels.keys()) + ["TESTS"]:
                #print(key)
                current_context[key] = []
            current_context["children"] = {}
            self.current_context.append("children")
        else:
            new_context_name = f"context_{len(current_context['children']) + 1}"
            # set it up, then add all logger levels
            current_context["children"][new_context_name] = {}
            for key in list(self.levels.keys())+ ["TESTS"]:
                current_context["children"][new_context_name][key] = []
            current_context["children"][new_context_name]["children"] = {}
            self.current_context.append(new_context_name)
        #self.draw_tree()
        
        
    def set_levels(self, level, trigger_lvl="ERROR"):
        if level in self.levels:
            self.level = level  # Update the logging level if it's valid
        else:
            raise ValueError("Invalid log level")  # Raise an error for invalid levels
        if trigger_lvl in self.levels:
            self.trigger_level = trigger_lvl  # Update the logging level if it's valid
        else:
            raise ValueError("Invalid log level")  # Raise an error for invalid levels

    def get_current_context(self):
        # Navigate through the context tree to get the current context dictionary
        context = self.contexts["root"]
        for part in self.current_context[1:]:
            context = context["children"].get(part, context)
        return context
    
    def draw_tree(self):
        def draw_context_tree(context, indent=""):
            for level in ["SUCCESS", "DEBUG", "WARNING", "ERROR"]:
                if context[level]:
                    print(f"{indent}{level}:")
                    for message in context[level]:
                        print(f"{indent}  - {message}")

            for child_name, child_context in context["children"].items():
                print(f"{indent}└── {child_name}/")
                draw_context_tree(child_context, indent + "    ")

        # Start drawing from the root context
        print("Root/")
        draw_context_tree(self.contexts["root"], "    ")

    def set_context(self, direction):
        if direction == +1:
            # Move to the parent context
            if len(self.current_context) > 1:
                self.current_context.pop()
        elif direction == -1:
            self._set_new_context()
            # Create a new nested context and move into it
            #current_context = self.get_current_context()
            #new_context_name = f"context_{len(current_context['children']) + 1}"
            #current_context["children"][new_context_name] = {
            #    "DEBUG": [], "WARNING": [], "ERROR": [], "TESTS": [], "children": {}
            #}
            #self.current_context.append(new_context_name)
            
        else:
            raise ValueError("Invalid context direction. Use +1 for parent and -1 for nested context.")

    def log(self, message, level):
        #print("Enter log with level: " + level)
        context = self.get_current_context()
        if level in context and self._format_message(level, message) not in context[level]:# and not self.triggered:
            context[level].append(self._format_message(level, message))
            # Print the message immediately if the level is at or above the current level
            if self.levels[level] >= self.levels[self.level]:
                print(self._format_message(level, message))

    def debug(self, message):
        self.log(message, "SUCCESS")  # Log a debug message


    def debug(self, message):
        self.log(message, "DEBUG")  # Log a debug message

    def warning(self, message):
        self.log(message, "WARNING")  # Log a warning message

    def error(self, message):
        self.log(message, "ERROR")  # Log an error message

    def add_test(self, val, test_fn, result_key, callback_true, callback_false, setup_message = ""):
        ##print("       Enter add_test")
        #setup_message = "SETTING TEST UP" + setup_message
        context = self.get_current_context()
        #print("adding test")
        #self.debug(setup_message)
        context["TESTS"].append({
            "val": val,
            "test_fn": test_fn,
            "result_key": result_key,
            "callback_true": callback_true,
            "callback_false": callback_false,
            "triggered": False
        })
        # if context in self.active_contexts:
        self.run_untrigd_test(context["TESTS"][-1]) # run last test
        #print("        Exit add_test")
            
    def run_untrigd_test(self, test):
        #print("            Enter run_untrigd_test")
        if test["triggered"] == False :
            #print('            test triggered')
            result = test["test_fn"](test["val"])  # Execute the test function with the value
            if result == test["result_key"]:
                test["callback_true"]()  # Call the true callback if the test passes
            else:
                test["callback_false"]()  # Call the false callback if the test fails
            test["triggered"] = True
        #else: print("            test ignored")
        #print("            Exit run_untrigd_test")
    
    def run_untrigd_tests(self):
        #print("                    Enter run_untrigd_testS")
        def run_context_tests(context, path):
            #print(path)
            #self.current_context = self.get_current_context()
            if tuple(path) not in self.active_contexts:
                #print(path, "Inactive")
                for test in context["TESTS"]:
                    self.active_contexts.add(tuple(path))  # Mark the context as active if it is not already
                    self.run_untrigd_test(test)
                    self.active_contexts.remove(tuple(path))  # Mark the context as active if it is not already
            #else:
            #    print(path, "Active")

            for child_name, child_context in context["children"].items():
                run_context_tests(child_context, path + [child_name])

        run_context_tests(self.contexts["root"], ["root"])
        #print("                   Exit run_untrigd_testS")
        
    def trigger(self, message, level):
        #print("               Enter trigger")
        #print("               Triggered by ", level, " ", message)
        if not self.triggered:
            #print("Triggering ", level, " ", message )
            self.run_untrigd_tests()
            self.log(message, level)
            #self._printActive()
            print(self._format_message(level,"End of "+level.lower() +" Message"))
            self.triggered = True
        #else: print("               Ignoring ", level, " ", message)

        #print("               Exit trigger")

    def _printActive(self):
        for context_tuple in sorted(self.active_contexts, key=len):
            context_dict = self.contexts["root"]
            for part in context_tuple[1:]:
                context_dict = context_dict["children"][part]
                for level in ["DEBUG", "WARNING"]:
                    for message in context_dict[level]:
                        print(message)
        
    def _activate_parent_contexts(self):
        # Start from the current context and traverse up to the root, activating each context
        def activate_parents(context_path):
            if context_path:
                self.active_contexts.add(tuple(context_path))
                # Remove the last element to move to the parent context
                parent_context_path = context_path[:-1]
                activate_parents(parent_context_path)
        # Get the current context path
        current_context_path = self.current_context.copy()
        # Recursively activate parent contexts
        activate_parents(current_context_path)

    def _printFullLog(self):
        print('###' * (len(self.current_context)*13))
        print('###' * (len(self.current_context)*3) + "   FULL DEBUG LOG   " + '###' * (len(self.current_context)*3)+ '#')
        print('###' * (len(self.current_context)*13))
        # Print all messages in order from the top
        for msg in self._getActiveMessages():
            print(msg)

    def _getActiveMessages(self):
        # Collect all messages from active contexts with indentation
        active_messages = []
        
        for context_tuple in sorted(self.active_contexts, key=len):
            context_dict = self.contexts["root"]
            for part in context_tuple[1:]:
                context_dict = context_dict["children"][part]
            for level in ["SUCCESS", "DEBUG", "WARNING", "ERROR"]:
                for message in context_dict[level]:
                    active_messages.append(message)
                    
        return active_messages
                        
    # Utility method to format messages with indentation
    def _format_message(self, level, message):
        indent = '|   ' * (len(self.current_context) - 1)
        if level == "DEBUG":
            flag = '|-->'
            lvl = f"DBG|"
        elif level == "ERROR":
            flag = "|/!\\"
            indent = flag * (len(self.current_context) - 1)
            lvl = flag
        elif level == "WARNING":
            flag = "|/!\\"
            lvl = f"WNG!"
        elif level == "SUCCESS":
            indent = 'C' + '====' * (len(self.current_context) - 1)
            flag = "==3"
            lvl = f"YES!"
        formatted_msg = f"{lvl}{indent}{flag}|{message}"            
        return formatted_msg   

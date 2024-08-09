class Logger:
    def __init__(self, level="WARNING"):
        self.print_lvl = -1
        self.level = level  # Set the default logging level
        self.levels = {"INFO": 0, "SUCCESS": 10, "DEBUG": 10, "WARNING": 20, "ERROR": 30}  # Define logging levels with priorities
        self.contexts = {}  # Initialize the root context

        self.current_path = []  # Path to the current context

    def _set_new_context(self, name="children", parent=None):
        # Handle autonaming
        name = self._autoname(name, parent)
        parent = self._autoname(parent)
        
        if not self.current_path:  # If no current path, initialize the root context
            if name not in self.contexts:
                self.contexts[name] = {}

        else:  # Navigate to the current context and add the new context
            context_ref = self.contexts
            for part in self.current_path:
                if part not in context_ref:
                    context_ref[part] = {}
                context_ref = context_ref[part]
            
            if name not in context_ref:
                context_ref[name] = {}
            

    def get_current_context(self):
        # Return the current context based on the current path
        context = self.contexts.copy()
        for part in self.current_path:
            context = context.get(part, context)
        return context

    def Navigate(self, destination="children"):
        # Navigate to a different context
        if destination == "parent":
            if len(self.current_path) > 0:  # Move to the parent context
                self.current_path.pop()
                
            else:
                print("Cannot Navigate to parent, root has no parents")
        else:
            # Create a new context if the destination doesn't exist
            if destination not in self.get_current_context():
                self._set_new_context(destination)
            self.current_path.append(destination)  # Move to the new or existing context

    def log(self, message, level):
        # Log a message at the given level
        if level not in self.get_current_context():
            print(self.current_path)
            print(level, "not in path")
            self._set_new_context(level)

        self.Navigate(level)  # Go to the desired level
        msg_number = len(self.get_current_context())
        formatted_message = self._format_message(level, message)
        self.get_current_context()[msg_number] = formatted_message
        self.Navigate("parent")  # Return to the previous context

        return formatted_message

    def debug(self, message):
        # Log a debug message
        self.log(message, "DEBUG")

    def warning(self, message):
        # Log a warning message
        self.log(message, "WARNING")

    def error(self, message):
        # Log an error message
        self.log(message, "ERROR")

    def _printIn(self, fn_name):
        self.print_lvl += 1
        print(self.print_lvl * "  ", "In : ", fn_name)
    
    def _printOut(self, fn_name):
        print(self.print_lvl * "  ", "Out: ", fn_name)
        self.print_lvl -= 1
    
    def _print(self, name, val=""):
        print('|   ' * (len(self.get_current_context())+1), name, ":  ", val)
    
    def _print_contexts(self):
        # Print the current state of contexts for debugging
        self._print("----------------------------------------------------------")
        self._print("self.contexts              ", self.contexts)
        self._print("self.current_path          ", self.current_path)
        #self._print("self.get_current_context()       ", self.get_current_context())
        self._print("self.get_current_context   ", self.get_current_context())
        self._print("----------------------------------------------------------")
    
    def _format_message(self, level, message, passed = True, name = ""):
        # Format the log message based on its level
        
        if passed == False:
            indent = '|XXX' + '|   ' * (len(self.current_path) - 1)
        else :
            if level == "SUCCESS":
                indent = '====' * (len(self.current_path))
            else:    
                indent = '|   ' * (len(self.current_path))
            
        flag = {
            "SUCCESS": '===3',
            "DEBUG": '|-->',
            "ERROR": "|/!\\",
            "WARNING": "|/!\\",
        }.get(level, '')
        lvl = {
            "SUCCESS": 'C===',
            "DEBUG": "DBG|",
            "ERROR": "|/!\\",
            "WARNING": "WNG!",
        }.get(level, '')
        if name:
            formatted_message = f"{lvl}{indent}{flag}|{name}:{message}"
        else:
            formatted_message = f"{lvl}{indent}{flag}|{message}"
        return formatted_message

    def add_test(self, test_fn, result_key, callback_true=None, callback_false=None, name = "test"):
        # Create a new test dictionary with the provided attributes
        if "TESTS" not in self.get_current_context():
            self._set_new_context("TESTS")
        self.Navigate("TESTS")
        
        name = self._autoname(name)
        newTest = {
            "name": name,
            "test_fn": test_fn,
            "result_key": result_key,
            "callback_true": callback_true,
            "callback_false": callback_false,
            "passed": False,
            "triggered": False,
            "output": {}
        }
        #self._print("On the verge of self.get_current_context()[name] = newTest. name:", name)
        
        self.get_current_context()[name] = newTest

        self.Navigate("parent")  # Return to the previous context
        
        return newTest  # Optionally return the test object if needed elsewhere

    def trigger(self, test, val):
        # If you give the test's name, but then it is not linked
        #if name in self.get_current_context()["TESTS"]:
        #    test = self.get_current_context()["TESTS"][name]
        # but if you do this you can modify the test ?
        if test["name"] in self.get_current_context()["TESTS"]:     
            test["triggered"] = True
            result = test["test_fn"](val)
            if result == test["result_key"]:
                test["passed"] = True
                test["output"][1] = test["callback_true"]
            else:
                test["passed"] = False
                test["output"][0] = test["callback_false"]
            return test
        
            
        else:
            raise ValueError("Test not in current context :/")
        
    
    def test_callback(self, message, level, passed = False, name = ""):
        formatted_message = self._format_message(level, message, passed, name)
        return formatted_message
    
    def _autoname(self, name="children", parent=""):
        # Autoname the context to avoid overwriting existing contexts
        if name:
            context = self.get_current_context()
            if parent in context:
                context = context[parent]
                name = f"{name}_{len(context[name]) + 1}"
            elif name in context:
                name = f"{name}_{len(context[name])}"
        return name
    
    def draw_tree(self):
        def draw_context_tree(context):
            for c in context:
                self.Navigate(c)
                if c in self.levels:  
                    for msg in self.get_current_context():
                        print(self.get_current_context()[msg])
    
                elif c == "TESTS":
                    for test in self.get_current_context():
                        for output in self.get_current_context()[test]["output"]:
                            print(self.get_current_context()[test]["output"][output])
                else:
                    context = self.get_current_context().copy()
                    draw_context_tree(context)
                self.Navigate("parent")
        
                        
        curr_path = self.current_path.copy()
        for c in curr_path:
            self.Navigate("parent")
        self._print("--------------------------------------------------")
        draw_context_tree(self.contexts)
        self._print("--------------------------------------------------")
        for c in curr_path:
            self.Navigate(c)
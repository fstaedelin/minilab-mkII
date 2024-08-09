class Logger:
    def __init__(self, level="WARNING"):
        self.print_lvl = -1
        self.level = level  # Set the default logging level
        self.tests = []
        self.levels = {"INFO": 0, "DEBUG": 10, "FAIL" : 15, "SUCCESS": 15, "WARNING": 20, "ERROR": 30}  # Define logging levels with priorities
        self.msg_log = []
        self.contexts = {}  # Initialize the root context
        self.unnamed_tests = 0
        self.current_path = []  # Path to the current context
        
    def Navigate(self, destination="children"):
        # Navigate to a different context
        if destination == "parent":
            if len(self.current_path) > 0:  # Move to the parent context
                self.current_path.pop()
                
            else:
                print("Cannot Navigate to parent, root has no parents")
        else:
            # Create a new context if the destination doesn't exist
            if destination not in self._get_current_context():
                self._set_new_context(destination)
            self.current_path.append(destination)  # Move to the new or existing context

    def WriteLog(self):
        for entry in self.msg_log:
            print(entry)
            
    def Log(self, message, level):
        # Log a message at the given level
        if level not in self._get_current_context():
            self._set_new_context(level)

        self.Navigate(level)  # Go to the desired level
        msg_number = len(self._get_current_context())
        formatted_message = self._format_message(level, message)
        self._get_current_context()[msg_number] = formatted_message
        self.Navigate("parent")  # Return to the previous context

        return formatted_message

    def Debug(self, message):
        # Log a debug message
        self.Log(message, "DEBUG")

    def Warning(self, message):
        # Log a warning message
        self.Log(message, "WARNING")

    def Error(self, message):
        # Log an error message
        self.Log(message, "ERROR")

    def AddTest(self, 
            test_fn = lambda: False,
            result_key=True, 
            callback_true=None,
            callback_false=None, 
            name = "test"):
        # Create a new test dictionary with the provided attributes
        if "TESTS" not in self._get_current_context():
            self._set_new_context("TESTS")
        self.Navigate("TESTS")
        
        ### set automatic callbacks:
        if callback_false == None:
            callback_false = self.Cb_False(f"Test {name} failed !")
        if callback_true == None:
            callback_true = self.Cb_True(f"Test {name} passed :D")
        # set auto name
        name = self._autonameTests(name)
        
        # define new test and assign it in tree
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
        
        self._get_current_context()[name] = newTest
        
        self.tests.append(newTest)
        self.Navigate("parent")  # Return to the previous context

        return newTest  # Optionally return the test object if needed elsewhere

    def TriggerTest(self, test, val):
        # If you give the test's name, but then it is not linked
        #if name in self.get_current_context()["TESTS"]:
        #    test = self.get_current_context()["TESTS"][name]
        # but if you do this you can modify the test ?
        if ("TESTS" not in self._get_current_context()) or test["name"] not in self._get_current_context()["TESTS"]:
            #test = self.lookup_test_address_in_context(test["name"])
            print("Not in good directory to trigger")
        #if "TESTS" in self.get_current_context():
        #    if test["name"] in self.get_current_context()["TESTS"]:     
        result = test["test_fn"](val) and test["result_key"]
        self._trigger_messages(result, test)
        test["triggered"] = True
        return test

    def Cb_True(self, message, level = "SUCCESS"):
        formatted_message = self._format_message(level, message, ignore = True)
        return formatted_message
    
    def Cb_False(self, message, level = "FAIL"):
        formatted_message = self._format_message(level, message, ignore = True)
        return formatted_message
            

            
    ############## UTILITIES
    def _format_message(self, level, message, name = "",ignore = False):
        # Format the log message based on its level

        if level == "SUCCESS":
            indent = '====' * (len(self.current_path))
        elif level == "FAIL":
            indent = '|XXX' + '|   ' * (len(self.current_path) - 1)
        else:    
            indent = '|   ' * (len(self.current_path))
            
        flag = {
            "SUCCESS": '===3',
            "DEBUG": '|-->',
            "ERROR": "|/!\\",
            "WARNING": "|/!\\",
            "FAIL": "|/X\\"
        }.get(level, '')
        lvl = {
            "SUCCESS": 'C===',
            "DEBUG": "DBG|",
            "ERROR": "|/!\\",
            "WARNING": "WNG!",
            "FAIL": "|/X\\",
        }.get(level, '')
        if name:
            formatted_message = f"{lvl}{indent}{flag}|{name}:{message}"
        else:
            formatted_message = f"{lvl}{indent}{flag}|{message}"
        
        if not ignore:
            self.msg_log.append(formatted_message)
        
        return formatted_message


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
            

    def _get_current_context(self):
        # Return the current context based on the current path
        context = self.contexts.copy()
        for part in self.current_path:
            context = context.get(part, context)
        return context



    def _printIn(self, fn_name):
        self.print_lvl += 1
        print(self.print_lvl * "  ", "In : ", fn_name)
    
    def _printOut(self, fn_name):
        print(self.print_lvl * "  ", "Out: ", fn_name)
        self.print_lvl -= 1
    
    def _print(self, name, val=""):
        print('|   ' * (len(self._get_current_context())+1), name, ":  ", val)
    
    def _print_contexts(self):
        # Print the current state of contexts for debugging
        self._print("----------------------------------------------------------")
        self._print("self.contexts              ", self.contexts)
        self._print("self.current_path          ", self.current_path)
        #self._print("self.get_current_context()       ", self.get_current_context())
        self._print("self.get_current_context   ", self._get_current_context())
        self._print("----------------------------------------------------------")
    
    def _autoname(self, name="children", parent=""):
        # Autoname the context to avoid overwriting existing contexts
        if name:
            context = self._get_current_context()
            if parent in context:
                context = context[parent]
                name = f"{name}_{len(context[name]) + 1}"
            elif name in context:
                name = f"{name}_{len(context[name])}"
        return name
    
    def _autonameTests(self, name="test", parent="TESTS"):
        # Autoname the context to avoid overwriting existing contexts
        context = self._get_current_context()
        if parent in context:
                context = context[parent]
        if name in context:
                name = f"{name}_{self.unnamed_tests+1}"
                self.unnamed_tests +=1
        return name
    
    def _trigger_messages(self, result, test):
        if result:
            self.msg_log.append(self._format_message("SUCCESS", "----------------", ignore = True))
            if test["triggered"] and not test["passed"] :
                self.msg_log.append(test["callback_false"])
            elif test["triggered"]:
                self.msg_log.append(test["callback_true"])
            
            self.msg_log.append(test["callback_true"])
            self.msg_log.append(self._format_message("SUCCESS", "----------------", ignore = True))    
            test["passed"] = True
        else:
            self.msg_log.append(self._format_message("FAIL", "----------------"))
            if test["triggered"] and not test["passed"] :
                self.msg_log.append(test["callback_false"])
            elif test["triggered"]:
                self.msg_log.append(test["callback_true"])
            
            self.msg_log.append(test["callback_false"])
            self.msg_log.append(self._format_message("FAIL", "----------------", ignore = True))
            test["passed"] = False
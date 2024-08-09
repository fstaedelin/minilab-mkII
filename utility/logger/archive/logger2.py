class Logger:
    def __init__(self, level="WARNING"):
        self.level = level  # Set the default logging level
        self.levels = {"TRIGGABLE": 5, "SUCCESS": 0, "DEBUG": 10, "WARNING": 20, "ERROR": 30}  # Define logging levels with priorities
        self.current_context = {"root":{}}  # Track the current context path as a list
        self.contexts = {"root":{}}  # Initialize the root context
        self._set_new_context()  # Set up the initial context
        self.active_contexts = set()  # Track active contexts
        self.triggered = False  # Track if a warning has been triggered
        self.trigger_level = "TRIGGABLE"  # Set the trigger level
        self.err_lvl = self.levels["DEBUG"]
    
    def _autoname(self, name = "children"):
        ### ERR CODE 0 IF REPERTORY IS MASTER ONE AND ALREADY EXISTS
        ### 1 if tried to pass a reserved name
        print("     IN _AUTONAME")
        print("             ", self.current_context)
        RESERVED = ["children"]
        for lvl in self.levels:
            RESERVED = RESERVED + [lvl]
        #print("RESERVED NAMES :", RESERVED)
        
        if name in self.current_context:
            print(name, "already in context, giving another name and putting aside")
            name =  f"{name}_{len(self.current_context[name]) + 1}"
            print("renamed ", name)
        
        return name
            
            
        
    def _set_new_context(self, name = "children" ,parent = "children"):
        RESERVED = ["children"]
        for lvl in self.levels:
            RESERVED = RESERVED + [lvl]
        # First time
        if self.contexts == {"root":{}}:
            for k in RESERVED:
                self.contexts[k] = {}
        current_context = self.contexts.copy()
        new_context_name = self._autoname(name)
        new_context = {key: {} for key in list(self.levels.keys())}
        new_context[parent] = {}
        current_context[parent][new_context_name] = new_context
        self.contexts.update(current_context)

        
            
            
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
        # Navigate through the context tree to get the current context dictionary
        context = self.contexts["root"]
        print(self.current_context)
        for part in self.current_context:
            print(part)
            context = context.get(part, context)
        print("get_current_context: ", context)
        return context


    def set_context(self, direction = 0, name="children"):
        if direction == +1:
            # Move to the parent context
            if len(self.current_context) > 1:
                self.current_context.pop()
        elif direction == -1:
            # Create a new nested context and move into it
            if name not in self.current_context:
                print(name, " setting new directory up")
                self._set_new_context(name)
            else: 
                print(name, " already in children, moving there")
                self.current_context = self.current_context[name]
        else:
            raise ValueError("Invalid context direction. Use +1 for parent and -1 for nested context.")

    def log(self, message, level):
        # Log a message at a given level in the current context
        context = self.get_current_context()
        formatted_message = self._format_message(level, message)
        if level in context and formatted_message not in context[level]:
            context[level] = formatted_message
            # Print the message immediately if the level is at or above the current level
            #print("self.level = ", self.levels[self.level])
            #print("level = ", self.levels[level])
            #print("trigger_level = ", self.levels[self.trigger_level])
            if self.levels[level] >= self.levels[self.trigger_level]:
                print("Storing in Triggable")
                #print(formatted_message)
                context["TRIGGABLE"] = (formatted_message)
            
            if self.levels[level] >= self.levels[self.level]:
                print("printing ", level)
                print(formatted_message)
            
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
        # Add a test to the current context
        print("Add_test")
        context = self.get_current_context()
        print("Context :    ", context)
        #print("add_test context: ", context)
        
        # set up the new test
        newTest = {
            "val": val,
            "test_fn": test_fn,
            "result_key": result_key,
            "callback_true": callback_true,
            "callback_false": callback_false,
        }
        
        context["TESTS"][self._autoname("test")] = (newTest)
        
        # Run the last added test immediately
        # if it fails and is triggered, trigger it
        print("Adding test")
        print("Triggered", triggered)
        if triggered:
            print("TRIGGGGEREED")
            newTest["triggered"] = True
            
            print(context["TESTS"])
            test = self._run_trigd_test(context["TESTS"])
        else:
            test = self._force_run_test(context["TESTS"])
        print("Test_result", test)
        
        

    def _force_run_test(self, test):
        # Run a test regardless of its triggered state
        result = test["test_fn"](test["val"])
        if result == test["result_key"]:
            test["callback_true"]()
            return True
        else:
            test["callback_false"]()
            return False

    
    def _run_trigd_test(self, test):
        # Run a test only if it hasn't been triggered yet
        if "triggered" in test:
            result = test["test_fn"](test["val"])
            if result == test["result_key"]:
                test["callback_true"]()
            else:
                test["callback_false"]()
            test["triggered"] = True

    def trigger(self, message, level):
        # Trigger a warning or error, activating all contexts and printing all messages
        #if not self.triggered:
            print("In trigger function !")
            context = self.get_current_context()
            print("get_current_context")
            print(context)
            #if context["TESTS"][-1].triggered == True:
            
            ## get the message
            self.triggering_event_message = self.log(message, level)
            
            deep_context = context["TESTS"]
            #path = list(self.find_parent_keys(deep_context, "triggered"))
            #print("path is :")
            #print(path)
            
            #self.triggered = True
            ##self.draw_tree()
            #print(self.current_context.copy())
            #context_path = self.current_context.copy()
            #context = self.contexts["root"]["children"]
            #self.scan_next(context_path,context)
            print(self._format_message(level, "End of " + level.lower() + " message"))
    
    ## Given a dictionnary, recursively finds the path to specified key
    def find_parent_keys(self, d, target_key, parent_key=None):
        print("find_parent_keys")
        for k, v in d.items():
            print("         key :", k)
            print("         value :", v)
            if k == target_key:
                print("key is target key")
                print(parent_key)
                # if it is a list, it must be a TEST list right ?
                if isinstance(v, list):
                    #for res in self.find_parent_keys(v, target_key, k)
                    print("parent key is None: ", parent_key, ". You must be in a list ?")
                    self.find_parent_keys(d, "TESTS", k)
                else:
                    yield parent_key
            if isinstance(v, dict):
                print("value is a dict")
                for res in self.find_parent_keys(v, target_key, k):
                    print(res)
                    yield res
    
    def find_triggering_path(self):
        context = self.get_current_context
        return self.find_parent_keys(context, )
        
    def scan_next(self, context_path, context):  
        i=0
        while context_path and i <100:
            i+=1
            print(i)
            next_destination = context_path[0]
            print("new iteration on context path:")
            #print(context_path[:])
            print(next_destination)
            #print(type(context))
            #print(context)
            
            if "TESTS" in context and context["TESTS"]:
                print("Current test list is not empty !")
                print("RUNNING TESTS")
                #print(context["TESTS"])
                for test in context["TESTS"]:
                    print(test)
                    self._force_run_test(test)
            else:
                print("no tests in context")
            

                    
            if "children" in context and next_destination in context["children"]:
                print("children not in context or next_destination not in context[children]")
                context = context["children"]
                if len(context_path) != 0:
                    context_path.pop(0)
                    self.scan_next(context_path, context)
                #print(context)
            else:
                print("Nothing done ! ")
                if len(context_path) != 0:
                    context_path.pop(0)
                    self.scan_next(context_path, context)
                    
            
            if next_destination in context:
                print("next destination in entry")
                context = context[next_destination]
                if len(context_path) != 0:
                    context_path.pop(0)
                    self.scan_next(context_path, context)
                #print(context)
            else:
                print("next destinationnot in context")
                if len(context_path) != 0:
                    context_path.pop(0)
                    self.scan_next(context_path, context)
            
                
    
    def _rerun_parent_tests(self):
        # Traverse up the context tree and re-run any tests found along the way
        context_path = self.current_context.copy()
        context_path.pop(0)
        #print(context_path)
        i = -1;
        context = self.contexts["root"]["children"]
        while context_path and i <100:
            i+=1
            print(i)
            for next_destination in context_path:
                print("new iteration on context path:")
                #print(context_path[:])
                print(next_destination)
                #print(type(context))
                #print(context)
                if next_destination in context:
                    print("part in context, moving to ",next_destination )
                    #print(next_destination)
                    if "TESTS" in context and context["TESTS"]:
                        print("Current test list is not empty !")
                        print("RUNNING TESTS")
                        for test in context["TESTS"]:
                            self._force_run_test(test)
                        #print("tests ran")
                        #print("poppping path: ", context_path)

                        #context = context["TESTS"]
                        #print("path popped: ", context_path)
                    #else:
                    #    print("Current test list is empty !")
                    #    context_path.pop(0)
                    if context[next_destination]["TESTS"]:
                            print("Tests in next destination")
                            #print("TESTS in context")
                            #print("Printing context[\"TESTS\"]")
                            #print(context["TESTS"])
                            #print("-----")
                    else:
                        print("no luck")
#                        print(context)
                    
                    print("going to destination and delteing")
                    context = context[next_destination]#["children"]
                    context_path.pop(0)
                else:
                    print("going to destination and delteing")
                    context = context[context_path[1]]#["children"]
                    context_path.pop(0)
                        
                #elif "TESTS" in context:
                #    print("Current test list is not empty !")
                #    print("RUNNING TESTS")
                #    for test in context["TESTS"]:
                #        self._force_run_test(test)
                #    #print("tests ran")
                #    #print("poppping path: ", context_path)
#
                #    #context = context["TESTS"]
                #    #print("path popped: ", context_path)
                #    context = context[next_destination]#["children"]
                #    context_path.pop(0)
                #    print("test")
                #    #context_path.pop(0)

            
                        
                #else:
                #    print("Ya stuck !!")
                
            
    def draw_tree(self):
        # Utility method to draw the context tree
        def draw_context_tree(context, indent=""):
            for level in ["SUCCESS", "DEBUG", "WARNING", "ERROR"]:
                if self.levels[level] >= self.err_lvl:
                    if context[level]:
                        for message in context[level]:
                                print(message)

            for child_name, child_context in context["children"].items():
                #print(f"{indent}└── {child_name}/")
                draw_context_tree(child_context, indent + "    ")

        # Start drawing from the root context
        #print("Root/")
        draw_context_tree(self.contexts["root"], "    ")
        
#    def _get_active_messages(self):
#        # Collect all messages from active contexts with indentation
#        active_messages = []
#        for context_tuple in sorted(self.active_contexts, key=len):
#            context_dict = self.contexts["root"]
#            for part in context_tuple[1:]:
#                context_dict = context_dict["children"][part]
#            for level in ["SUCCESS", "DEBUG", "WARNING", "ERROR"]:
#                for message in context_dict[level]:
#                    active_messages.append(message)
#                    print(message)
#        return active_messages

    def _format_message(self, level, message):
        # Utility method to format messages with indentation
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


# Usage example:
global logger
logger = Logger()
logger.set_levels("WARNING")


# Define Event class for better structure
class Event:
    def __init__(self, event_id):
        self.id = event_id
        self.handled = False

# Function to test if it works OK when nested:
def FirstEventHandler(event):
    if event.handled:
        logger.debug("Event handled before FirstEventHandler")
    else:
        if event.id > 200:
            event.handled = True
        addEventCheck(event, "Event handled by FirstEventHandler", "Event not handled by FirstEventHandler")


def SecondEventHandler(event):
    if event.handled:
        logger.debug("Event handled before FirstEventHandler")
    else:
        if event.id < 100:
            event.handled = True
        addEventCheck(event, "Event handled by SecondEventHandler", "Event not handled by SecondEventHandler")

def addEventCheck(event, okmessage, warningMessage):
    global logger
    #print("   Enter addEventCheck")
    logger.add_test(
        val=event,
        test_fn=lambda event: event.handled,
        result_key=True,
        callback_true=lambda: logger.log(okmessage, "SUCCESS"),
        callback_false=lambda: logger.log(warningMessage, "WARNING")
    )
    #print("   Exit addEventCheck")
    
def addFinalCheck(event):
    global logger
    logger.add_test(
        val=event,
        test_fn=lambda event: event.handled,
        result_key=True,
        callback_true=lambda: logger.log("Event was handled", "SUCCESS"),
        callback_false=testfunc(),
        triggered = True
    )

def testfunc():
    global logger
    logger.trigger("NOT HANDLED :( ", "ERROR"),
    context = logger.get_current_context()
    print(context)




# Setting initial context and logging messages
logger.debug("Initializing")
logger.set_context(-1)
logger.debug("Doing some stuff")

# Create an event
event1 = Event(69)

# Create a nested context
logger.set_context(-1)
FirstEventHandler(event1)
logger.set_context(+1)
logger.debug("Doing some more stuff")

logger.set_context(-1)
SecondEventHandler(event1)

logger.set_context(-1)
logger.add_test(
        val=event1,
        test_fn=lambda event: event.id,
        result_key=69,
        callback_true=lambda: logger.trigger("69 hehehe", "ERROR"),
        callback_false=lambda: logger.debug("not 69 :("),
        triggered=True,
    )
logger.set_context(+1)

# Move back to the parent context
logger.set_context(+1)

addFinalCheck(event1)
# Run tests

logger.set_context(+1)
#logger.draw_tree()
# Trigger a warning which will print all debug and warning messages for the context and nested ones
#logger.trigger_warning("Testing warning mechanism.")
	

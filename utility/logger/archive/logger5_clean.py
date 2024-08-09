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

logger = Logger("DEBUG")
logger._print("GOING TO INITIALIZATION")
logger.Navigate("INIT")
logger._print_contexts()
logger._print("LOGGING")
logger.log("Initializing ...", "DEBUG")
logger._print_contexts()


logger._print("GOING TO ROOT")
logger.Navigate("parent")
logger._print_contexts()
##### Trying to creat a new level

logger._print("GOING TO PROCESING")
logger.Navigate("PROCESSING")
logger._print_contexts()

logger._print("CREATING DEBUG EVENT")
logger.log("processing ...", "DEBUG")
logger._print_contexts()
## UNTIL HERE ALL IS GOOD

logger._print("GOING TO PROCESSING1")
logger._print_contexts()
logger.Navigate("PROCESSING1")
logger._print_contexts()
#
logger._print("   Setup the warning")
logger.warning("Not like this !")
logger._print_contexts()

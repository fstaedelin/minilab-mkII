class Logger:
    def __init__(self, level="WARNING"):
        self.print_lvl = -1
        self.level = level  # Set the default logging level
        self.levels = {"INFO": 0, "DEBUG": 10, "WARNING": 20, "ERROR": 30}  # Define logging levels with priorities
        self.contexts = {}  # Initialize the root context
        self.current_context = {}  # Current context, updated by _set_new_context
        self.current_path = []  # Path to the current context

    def _autoname(self, name="children", parent=""):
        # Autoname the context to avoid overwriting existing contexts
        if name:
            context = self.get_current_context()
            if parent in context:
                context = context[parent]
                if name in context:
                    name = f"{name}_{len(context[name]) + 1}"
        return name

    def _set_new_context(self, name="children", parent=None):
        # Handle autonaming
        name = self._autoname(name, parent)
        parent = self._autoname(parent)
        
        if not self.current_path:  # If no current path, initialize the root context
            if name not in self.contexts:
                self.contexts[name] = {}
            self.current_context = self.contexts[name]
        else:  # Navigate to the current context and add the new context
            context_ref = self.contexts
            for part in self.current_path:
                if part not in context_ref:
                    context_ref[part] = {}
                context_ref = context_ref[part]
            
            if name not in context_ref:
                context_ref[name] = {}
            self.current_context = context_ref[name]

    def set_levels(self, level):
        # Update the logging level if valid
        if level in self.levels:
            self.level = level
        else:
            raise ValueError("Invalid log level")

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
                self.current_context = self.get_current_context()
            else:
                print("Cannot Navigate to parent, root has no parents")
        else:
            # Create a new context if the destination doesn't exist
            if destination not in self.current_context:
                self._set_new_context(destination)
            self.current_path.append(destination)  # Move to the new or existing context

    def log(self, message, level):
        # Log a message at the given level
        if level not in self.current_context:
            self._set_new_context(level)

        self.Navigate(level)  # Go to the desired level
        msg_number = len(self.current_context)
        formatted_message = self._format_message(level, message)
        self.current_context[msg_number] = formatted_message
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
        print((self.print_lvl + 1) * "  ", name, ":  ", val)
    
    def _print_contexts(self):
        # Print the current state of contexts for debugging
        self._print("----------------------------------------------------------")
        self._print("self.contexts              ", self.contexts)
        self._print("self.current_path          ", self.current_path)
        self._print("self.current_context       ", self.current_context)
        self._print("self.get_current_context   ", self.get_current_context())
        self._print("----------------------------------------------------------")
    
    def _format_message(self, level, message):
        # Format the log message based on its level
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
        return formatted_message

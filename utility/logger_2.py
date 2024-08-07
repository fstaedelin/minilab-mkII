class Logger:
    def __init__(self, level="WARNING"):
        self.level = level  # Set the default logging level
        self.levels = {"DEBUG": 10, "WARNING": 20, "ERROR": 30}  # Define logging levels with priorities
        self.contexts = {"root": {"DEBUG": [], "WARNING": [], "ERROR": [], "TESTS": [], "children": {}}}
        self.current_context = ["root"]  # Track the current context path as a list
        self.active_contexts = set()  # Track active contexts

    def set_level(self, level):
        if level in self.levels:
            self.level = level  # Update the logging level if it's valid
        else:
            raise ValueError("Invalid log level")  # Raise an error for invalid levels

    def get_current_context(self):
        # Navigate through the context tree to get the current context dictionary
        context = self.contexts["root"]
        for part in self.current_context[1:]:
            context = context["children"].get(part, context)
        return context

    def set_context(self, direction):
        if direction == +1:
            # Move to the parent context
            if len(self.current_context) > 1:
                self.current_context.pop()
        elif direction == -1:
            # Create a new nested context and move into it
            current_context = self.get_current_context()
            new_context_name = f"context_{len(current_context['children']) + 1}"
            current_context["children"][new_context_name] = {
                "DEBUG": [], "WARNING": [], "ERROR": [], "TESTS": [], "children": {}
            }
            self.current_context.append(new_context_name)
        else:
            raise ValueError("Invalid context direction. Use +1 for parent and -1 for nested context.")

    def log(self, message, level):
        context = self.get_current_context()
        if level in context:
            context[level].append(message)
            # Print the message immediately if the level is at or above the current level
            if self.levels[level] >= self.levels[self.level]:
                print(f"{'|   ' * (len(self.current_context) - 1)}|-- {level}: {message}")

    def debug(self, message):
        self.log(message, "DEBUG")  # Log a debug message

    def warning(self, message):
        self.log(message, "WARNING")  # Log a warning message

    def error(self, message):
        self.log(message, "ERROR")  # Log an error message

    def add_test(self, val, test_fn, result_key, callback_true, callback_false):
        context = self.get_current_context()
        context["TESTS"].append({
            "val": val,
            "test_fn": test_fn,
            "result_key": result_key,
            "callback_true": callback_true,
            "callback_false": callback_false
        })

    def run_tests(self):
        def run_context_tests(context, path):
            for test in context["TESTS"]:
                result = test["test_fn"](test["val"])  # Execute the test function with the value
                if result == test["result_key"]:
                    test["callback_true"]()  # Call the true callback if the test passes
                    self.active_contexts.add(tuple(path))  # Mark the context as active
                else:
                    test["callback_false"]()  # Call the false callback if the test fails

            for child_name, child_context in context["children"].items():
                run_context_tests(child_context, path + [child_name])

        run_context_tests(self.contexts["root"], ["root"])

    def trigger_warning(self, warning_message):
        # Define a function to activate all relevant contexts and store them in self.active_contexts
        def activate_contexts(context, path):
            self.active_contexts.add(tuple(path))
            for child_name, child_context in context["children"].items():
                activate_contexts(child_context, path + [child_name])

        # Activate the context for the current path
        context_path = self.current_context.copy()
        activate_contexts(self.contexts["root"], context_path)

        # Print all messages from active contexts with indentation
        first_debug_printed = False
        for context_tuple in sorted(self.active_contexts, key=len):
            context_dict = self.contexts["root"]
            for part in context_tuple[1:]:
                context_dict = context_dict["children"][part]
            for level in ["DEBUG", "WARNING", "ERROR"]:
                for message in context_dict[level]:
                    if level == "DEBUG" and not first_debug_printed:
                        print(self._format_message("WARNING", warning_message))
                        first_debug_printed = True
                    print(self._format_message(level, message))

        # Print the main warning message with indentation
        print(self._format_message("WARNING", warning_message))
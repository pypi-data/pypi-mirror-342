class MyHandlerClass:
    def __init__(self):
        self.handled_value = None

    def method_handler(self, value_to_set):
        self.handled_value = value_to_set
        return f"set_{value_to_set}"

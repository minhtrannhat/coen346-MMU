class Commands:
    def __init__(self, list_commands):
        self.list = list_commands
        self.index = 0

    def next_cmd(self):
        self.index = (self.index + 1) % len(self.list)
        # this code basically loops through the array. When index +1 will be equal to self.list , the modulo will return 0, basically referencing back to the first value of the list
        # it was written in the assignement to constantly loop through the array

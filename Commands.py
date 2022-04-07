import logging


class Commands:
    def __init__(self, list_commands):
        self.list = list_commands
        self.index = 0

    def next_cmd(self):
        logger = logging.getLogger(__name__)
        self.index = (self.index + 1) % len(self.list)
        logger.debug(f"Current index in command list: {self.index}")

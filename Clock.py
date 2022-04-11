from time import sleep
from threading import Thread
import logging


class clock(Thread):
    def __init__(self):
        super(clock, self).__init__()
        self.isFinished: bool = False
        self.time: int = 0

    def setFinished(self, isFinished: bool):
        self.isFinished = isFinished

    def run(self):
        logger = logging.getLogger(f"{__name__} thread")
        while not self.isFinished:
            sleep(0.1)
            self.time = self.time + 50
            logger.debug(f"Current time is {self.time}")


myClock = clock()

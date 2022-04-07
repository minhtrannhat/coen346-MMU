from Page import Page
from Clock import myClock
import logging

logger = logging.getLogger(f"{__name__} thread")


class MainMemory:
    def __init__(self, maximumNumberOfPages, K_VALUE, timeOut):
        self.mainMemory: list[Page] = []
        self.maximumNumberOfPages: int = maximumNumberOfPages
        self.K_VALUE = K_VALUE
        self.timeOut = timeOut

    def full(self):
        return len(self.mainMemory) == self.maximumNumberOfPages

    def addToMainMemory(self, id: int, value: int):
        self.mainMemory.append(Page(id, value, myClock.time, self.K_VALUE))

    def getVariable(self, id):
        for page in self.mainMemory:
            if page.ID == id:
                logger.debug(
                    f"Found page with ID {page.ID} that contains value of {page.value}"
                )
                return page.value
        return -1

    def release(self, id):
        for page in self.mainMemory:
            if page.ID == id:
                self.mainMemory.remove(page)
                logger.debug(f"Released {page} from main memory")
                return

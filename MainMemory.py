from collections import defaultdict
from Page import Page
from Clock import myClock
import logging

logger = logging.getLogger(f"{__name__} thread")


class MainMemory:
    def __init__(self, maximumNumberOfPages, K_VALUE, timeOut):
        self.mainMemory: list[Page] = []
        self.maximumNumberOfPages: int = maximumNumberOfPages
        self.access_memory_value: dict = defaultdict(lambda: 0)
        self.increment: int = 0
        self.K_VALUE = K_VALUE
        self.timeOut = timeOut

    def full(self):
        logger.debug("Main memory is currently full")
        return len(self.mainMemory) == self.maximumNumberOfPages

    def addToMainMemory(self, id: int, value: int):
        for i in range(len(self.mainMemory)):
            if self.mainMemory[i].ID == id:
                self.mainMemory[i].value = value
                self.increment += 1
                self.access_memory_value[id] = self.increment
                return

        if not self.full():
            self.mainMemory.append(Page(id, value, myClock.time, self.K_VALUE))
            self.increment += 1
            self.access_memory_value[id] = self.increment

    def getVariable(self, id):
        for page in self.mainMemory:
            if page.ID == id:
                self.increment += 1
                self.access_memory_value[id] = self.increment
                logger.debug(
                    f"Found page with ID {page.ID} that contains value of {page.value}"
                )
                return page.value
        return -1

    def release(self, id):
        for page in self.mainMemory:
            if page.ID == id:
                self.mainMemory.remove(page)
                self.increment += 1
                self.access_memory_value[id] = self.increment
                logger.debug(f"Released {page} from main memory")
                return

    def set_page(self, index, page):
        page = page.strip().split()
        s = list(page)
        print(s)
        self.mainMemory[index] = s
        self.increment += 1
        self.access_memory_value[index] = self.increment

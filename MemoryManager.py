from threading import Thread, Lock
import logging
from Commands import Commands
from DiskSpace import Diskspace
from Page import Page
from Clock import myClock
from Parser import K_VALUE, timeOut
from MainMemory import MainMemory
from heapq import heapify, heappush

logger = logging.getLogger(f"{__name__} thread")


class MemoryManager(Thread):
    def __init__(self, commands, diskSpace, mainMemory):
        super(MemoryManager, self).__init__()
        self.isFinished = False
        self.mainMemory: MainMemory = mainMemory
        self.commands: Commands = commands
        self.diskSpace: Diskspace = diskSpace

        # Semaphores
        self.lock = Lock()

    def setFinished(self, isFinished: bool):
        self.isFinished = isFinished

    def run(self):
        logger.debug("Starting Memory Manager Thread")
        while not self.isFinished:
            continue
        logger.debug("Exiting Memory Manager Thread")

    def store(self, id, value):
        currentTime: int = myClock.time
        if not self.mainMemory.full():
            self.mainMemory.addToMainMemory(id, value)
            logger.debug(
                f"Storing to main memory a page with id: {id} and {value}"
            )
        else:
            self.diskSpace.write(Page(id, value, currentTime, K_VALUE))
            logger.debug(
                f"Storing to disk space a page with id: {id} and {value}"
            )

    def lookUp(self, id):
        if self.mainMemory.getVariable(id) == -1:
            logger.debug(
                "Page fault occured, swapping from disk space to virtual memory"
            )
            return self.swap(id)
        return self.mainMemory.getVariable(id)

    def release(self, id):
        self.mainMemory.release(id)

    # When a page replacement is needed, the page to be replaced is chosen as follows:
    #
    # Of all the pages that have LAST(p)-HIST(p)[1] > time-out, chose the one
    # with the minimum value of HIST(p)[k].
    #
    # In case of a tie between two pages (both satisfy LAST(p)-HIST(p)[1]>time-out
    # out and they have the same value for HIST(p)[k]), OR none of the pages
    # satisfies LAST(p)-HIST(p)[1]>time-out, chose the page with the smallest value of HIST(p)[1]
    def swap(self, id):
        currentTime: int = myClock.time

        minHeapOfPages: list[Page] = []

        for page in self.mainMemory.mainMemory:
            if page.LAST - page.HIST[0] > timeOut:
                heappush(minHeapOfPages, page)

        heapify(minHeapOfPages)

        if (not minHeapOfPages) or (
            minHeapOfPages[0].HIST[K_VALUE - 1]
            == minHeapOfPages[1].HIST[K_VALUE - 1]
        ):
            tempList = sorted(
                self.mainMemory.mainMemory, key=lambda x: x.HIST[0]
            )
            pageChosenToSwap: Page = tempList[0]
            logger.debug(f"The page chosen to swap is {pageChosenToSwap}")

        else:
            logger.debug(
                f"Min heap of the pages with page._LAST - page._HIST[0] > timeOut is {minHeapOfPages}"
            )
            pageChosenToSwap: Page = minHeapOfPages[0]
            logger.debug(f"The page chosen to swap is {pageChosenToSwap}")

        indexOfPageToSwap = self.mainMemory.mainMemory.index(pageChosenToSwap)

        # move the page from main memory into disk space
        tempID, tempValue = self.diskSpace.change(
            pageChosenToSwap, indexOfPageToSwap
        )

        # move the page from diskspace into memory
        if self.diskSpace.read(tempID) != -1:
            self.mainMemory.mainMemory[indexOfPageToSwap] = Page(
                tempID, tempValue, currentTime, K_VALUE
            )

        logger.info(
            f"Clock: {currentTime}, Memory Manager Swap: Variable {id} with Variable {id}"
        )

    def api(self, commands, process_number):
        logger = logging.getLogger(f"{__name__} thread")

        currentTime: int = myClock.time

        with self.lock:
            if len(commands) > 2:
                com = commands[0]
                com1 = commands[1]
                com2 = commands[2]
                id = com1

                if com == "Store":
                    self.status = True
                    self.store(com1, com2)
                    logger.info(
                        f"Clock: {currentTime}, Process {process_number}: {com}: Variable {id}, Value: {com2}"
                    )
                    self.status = False
            else:
                com = commands[0]
                com1 = commands[1]
                id = com1

                if com == "Release":
                    self.release(com1)
                    logger.info(
                        f"Clock: {currentTime}, Process {process_number}: {com}: Variable: {id}"
                    )

                elif com == "Lookup":
                    myClock.add_time(10)
                    self.lookUp(com1)
                    logger.info(
                        f"Clock: {currentTime}, Process {process_number}: {com}: Variable {id}, Value: {self.mainMemory.getVariable(id)}"
                    )

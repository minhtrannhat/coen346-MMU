from DiskSpace import Diskspace
from MainMemory import MainMemory
from Scheduler import Scheduler
from MemoryManager import MemoryManager
from Parser import extract_data
from Clock import myClock
from Commands import Commands
import logging


def main():
    # setup logging to output.txt
    logging.basicConfig(
        filename="output.txt",
        filemode="w",
        force=True,
        level=logging.DEBUG,
        format="{message}",
        style="{",
    )

    logger = logging.getLogger(__name__)

    listOfThreads = []

    (
        listOfProcesses,
        maximumNumberOfPages,
        numberOfCores,
        listOfCommands,
        K_VALUE,
        timeOut,
    ) = extract_data()

    commands = Commands(listOfCommands)
    mainMemory = MainMemory(maximumNumberOfPages, K_VALUE, timeOut)
    diskSpace = Diskspace()

    memoryManager = MemoryManager(commands, diskSpace, mainMemory)

    # start the clock
    myClock.start()

    # start the MMU
    memoryManager.start()

    # initialise and start the Scheduler
    scheduler = Scheduler(
        numberOfCores,
        memoryManager,
        commands,
        listOfProcesses,
        listOfThreads,
    )
    scheduler.start()

    listOfThreads.append(memoryManager)
    listOfThreads.append(scheduler)

    scheduler.process_thread()

    for thread in listOfThreads:
        thread.setFinished(True)
        thread.join()

    myClock.join()

    logger.debug(f"Memory: {memoryManager.mainMemory}")


if __name__ == "__main__":
    main()

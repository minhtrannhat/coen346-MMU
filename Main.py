from DiskSpace import Diskspace
from MainMemory import MainMemory
from Scheduler import Scheduler
from MemoryManager import MemoryManager
from Parser import extract_data
from Clock import myClock
from Commands import Commands
from os import remove
import logging


def main():
    # setup logging to output.txt
    logging.basicConfig(
        filename="output.txt",
        filemode="w",
        force=True,
        level=logging.INFO,
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
    listOfThreads.append(myClock)

    scheduler.process_thread()

    for thread in listOfThreads:
        thread.setFinished(True)
        thread.join()

    remove("vm.txt")

    logger.debug(f"Memory: {memoryManager.mainMemory}")

    print("Simulation Complete")


if __name__ == "__main__":
    main()
